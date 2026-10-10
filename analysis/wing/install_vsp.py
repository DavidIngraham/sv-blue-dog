"""Install the pinned Windows/Python-3.13 OpenVSP distribution locally."""
import hashlib
from pathlib import Path
import urllib.request
from urllib.error import HTTPError
import zipfile
ROOT=Path(__file__).resolve().parents[2]
VERSION='3.54.0'
ARCHIVE=f'OpenVSP-{VERSION}-win64-Python3.13.zip'
URL=f'https://openvsp.org/zips/current/windows/{ARCHIVE}'
SHA256='45b99571b6bd571e9654f422009633a32fe0a622824b379ffae18c6ef28de6db'

def install():
    cache=ROOT/'.tools';cache.mkdir(exist_ok=True)
    archive=cache/ARCHIVE
    if not archive.exists():
        try:
            urllib.request.urlretrieve(URL,archive)
        except HTTPError as error:
            if error.code != 404:raise
            urllib.request.urlretrieve(URL.replace("/current/", "/old/"),archive)
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=SHA256:
        raise ValueError('OpenVSP archive differs from pinned download; inspect release before updating checksum')
    destination=cache/f'openvsp-{VERSION}'
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            if not (destination/member.filename).resolve().is_relative_to(destination.resolve()):
                raise ValueError('Unsafe archive member')
        z.extractall(destination)
    print(destination)

if __name__=='__main__':install()
