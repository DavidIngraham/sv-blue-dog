"""Georeferenced endpoint imagery with the exact model course overlay.

Refresh imagery explicitly; normal publication uses the archived response extent
and pixels, so builds are reproducible and do not depend on a live map service.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from math import cos, log, pi, radians, tan
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from tools.boat_analysis.environment.course import LocalFrame
from tools.boat_analysis.environment.routing import build, rounding_paths
from tools.boat_analysis.model.runtime import ROOT

SERVICE = 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer'
ARCHIVE = ROOT/'tools/publishing/data/course-imagery'
VIEWS = {
    'bingen': ('eastGate', 'Bingen: start and finish', 'Buoy 39'),
    'stevenson': ('westGate', 'Stevenson: port rounding', 'Buoy 16'),
}


def mercator(lon, lat):
    """WGS84 degrees to EPSG:3857 metres, matching the imagery service."""
    radius = 6378137.0
    return radius*radians(lon), radius*log(tan(pi/4+radians(lat)/2))


def image_xy(lon, lat, extent, width, height):
    x,y = mercator(lon,lat)
    return ((x-extent['xmin'])/(extent['xmax']-extent['xmin'])*width,
            (extent['ymax']-y)/(extent['ymax']-extent['ymin'])*height)


def refresh():
    values, *_ = build()
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    with urlopen(SERVICE+'?f=json', timeout=45) as response:
        service = json.load(response)
    records = {}
    for name,(gate,_,_) in VIEWS.items():
        x,y = mercator(*values[gate][:2])
        params = dict(bbox=f'{x-4000},{y-2500},{x+4000},{y+2500}', bboxSR=3857,
                      imageSR=3857, size='1600,1000', format='jpg', f='json')
        request = SERVICE+'/export?'+urlencode(params)
        with urlopen(request, timeout=60) as response:
            record = json.load(response)
        if 'error' in record or 'extent' not in record:
            raise ValueError(record)
        with urlopen(record['href'], timeout=60) as response:
            pixels = response.read()
        filename = name+'.jpg'
        (ARCHIVE/filename).write_bytes(pixels)
        records[name] = dict(request=request, image=filename, sha256=hashlib.sha256(pixels).hexdigest(),
                             extent=record['extent'], width=record['width'], height=record['height'])
    (ARCHIVE/'manifest.json').write_text(json.dumps(dict(
        service=SERVICE, attribution=service['copyrightText'],
        retrievedAt=datetime.now(timezone.utc).isoformat(),
        imageryDate='Mosaic acquisition dates vary; retrieval date is not acquisition date.',
        views=records), indent=2)+'\n')


def render(preview=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from PIL import Image
    import numpy as np
    manifest = json.loads((ARCHIVE/'manifest.json').read_text())
    values, water, _, gates, route = build()
    paths = rounding_paths(water,gates,route,values['routing'][4])
    frame = LocalFrame()
    results = []
    for name,(gate,title,marker) in VIEWS.items():
        record = manifest['views'][name]
        source = ARCHIVE/record['image']
        if hashlib.sha256(source.read_bytes()).hexdigest()!=record['sha256']:
            raise ValueError('Imagery checksum differs from manifest')
        extent=record['extent']; width=record['width']; height=record['height']
        if extent['spatialReference'].get('latestWkid',extent['spatialReference'].get('wkid'))!=3857:
            raise ValueError('Imagery must use EPSG:3857')
        def xy(lon,lat): return image_xy(lon,lat,extent,width,height)
        def projected(line): return np.array([xy(*frame.unproject(x,y)) for x,y in line.coords])
        with plt.rc_context({'svg.fonttype':'none','svg.hashsalt':'blue-dog-course-satellite'}):
            fig,ax=plt.subplots(figsize=(12,8.8))
            fig.subplots_adjust(left=.015,right=.985,top=.91,bottom=.11)
            ax.imshow(Image.open(source),extent=(0,width,height,0))
            for path in paths:
                ax.plot(*projected(path).T,color='black',linewidth=4,alpha=.7)
            for index,path in enumerate(paths):
                points=projected(path)
                ax.plot(*points.T,color='#ffb347' if index==0 else '#4ff1e0',linewidth=2.2,
                        linestyle='-' if index==0 else '--')
            keys = ['eastGate'] if name=='bingen' else ['westGate','turnGate','returnGate']
            for key in keys:
                points=projected(gates[key]);ax.plot(*points.T,color='#ff69e2',linewidth=3)
            x,y=xy(*values[gate][:2]);ax.scatter([x],[y],color='#fff',edgecolor='#111',s=55,zorder=8)
            ax.annotate(marker,(x,y),xytext=(18,25),textcoords='offset points',color='white',
                        bbox=dict(facecolor='#152d3b',alpha=.9,pad=4),arrowprops=dict(arrowstyle='-',color='white'))
            center=gates[gate].interpolate(.5,normalized=True);gx,gy=xy(*frame.unproject(center.x,center.y))
            ax.annotate('Start / finish gate' if name=='bingen' else 'North → west → south checkpoints',
                        (gx,gy),xytext=(25,-45),textcoords='offset points',color='white',
                        bbox=dict(facecolor='#152d3b',alpha=.9,pad=4),arrowprops=dict(arrowstyle='-',color='#ff69e2'))
            ax.text(.02,.97,'WASHINGTON SHORE',transform=ax.transAxes,va='top',color='white',fontsize=10,
                    bbox=dict(facecolor='#152d3b',alpha=.8,pad=4))
            ax.text(.02,.03,'OREGON SHORE',transform=ax.transAxes,color='white',fontsize=10,
                    bbox=dict(facecolor='#152d3b',alpha=.8,pad=4))
            ax.text(.98,.97,'N ↑',transform=ax.transAxes,ha='right',va='top',color='white',fontsize=14)
            bar=1000/cos(radians(values[gate][1]))/(extent['xmax']-extent['xmin'])*width
            ax.plot([width-300,width-300+bar],[height-65,height-65],color='black',linewidth=6)
            ax.plot([width-300,width-300+bar],[height-65,height-65],color='white',linewidth=3)
            ax.text(width-300,height-85,'1 km at marker latitude',color='white',fontsize=9,
                    bbox=dict(facecolor='#152d3b',alpha=.8,pad=3))
            ax.set(xlim=(0,width),ylim=(height,0));ax.set_axis_off()
            fig.suptitle(title,fontsize=20,fontweight='bold',color='#183047')
            fig.text(.02,.075,'Orange solid: outbound · Cyan dashed: rounding / return · Magenta: proposed gates',fontsize=10)
            fig.text(.02,.05,'Satellite / aerial context · Scored course excludes shore launch and retrieval · Not a navigation chart',fontsize=9)
            fig.text(.98,.023,manifest['attribution'],ha='right',fontsize=8)
            target=ROOT/f'docs/figures/course-{name}-satellite.svg'
            fig.savefig(target,metadata={'Date':None,'Description':manifest['imageryDate']})
            if preview is not None:
                preview.mkdir(parents=True,exist_ok=True)
                fig.savefig(preview/(name+".png"),dpi=130)
            plt.close(fig);results.append(target)
    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-imagery',action='store_true')
    args=parser.parse_args()
    if args.refresh_imagery: refresh()
    print(*render(),sep='\n')
