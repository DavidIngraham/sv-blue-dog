# Run with Windows PowerShell 5.1 while SolidWorks is open.
# Exports the source assembly read-only; never saves the CAD model.
param([string]$Output = '')
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
if (!$Output) { $Output = Join-Path $repo 'docs/figures/testbed-solidworks.png' }
$source = Join-Path $repo 'cad/SV Bluedog.SLDASM'
$interop = 'C:/Program Files/Dassault Systemes/SOLIDWORKS 3DEXPERIENCE R2026x/SOLIDWORKS/api/redist/SolidWorks.Interop.sldworks.dll'
Add-Type -Path $interop
Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies $interop -TypeDefinition @'
using System;
using SolidWorks.Interop.sldworks;
public class BlueDogCadRender {
    public static void Export(object application, string source, string output) {
        ISldWorks sw = (ISldWorks)application;
        IModelDoc2 previous = sw.IActiveDoc2;
        int errors=0, warnings=0;
        IModelDoc2 doc = sw.IGetOpenDocumentByName2(source);
        if(doc==null) doc = sw.OpenDoc6(source,2,3,"",ref errors,ref warnings);
        if(doc==null || errors!=0) throw new Exception("CAD open errors="+errors);
        if(warnings!=0) throw new Exception("Review CAD load warnings="+warnings);
        sw.ActivateDoc3(doc.GetTitle(),false,0,ref errors);
        doc.ClearSelection2(true);
        doc.ShowNamedView2("*Isometric",7);
        doc.ViewZoomtofit2();
        doc.GraphicsRedraw2();
        if(!doc.SaveBMP(output,1800,1500)) throw new Exception("CAD bitmap export failed");
        if(previous!=null) sw.ActivateDoc3(previous.GetTitle(),false,0,ref errors);
    }
}
'@
$app = [Runtime.InteropServices.Marshal]::GetActiveObject('SldWorks.Application')
$bitmap = Join-Path $repo '.tools/testbed-isometric.bmp'
[BlueDogCadRender]::Export($app, $source, $bitmap)
$picture = [Drawing.Image]::FromFile($bitmap)
try { $picture.Save($Output, [Drawing.Imaging.ImageFormat]::Png) } finally { $picture.Dispose() }
Write-Output $Output
