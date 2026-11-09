#!/usr/bin/env python3
"""Package existing DevKit v19 source edits, preserving non-editable originals."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,sys,json
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scripts'))
import dat_codec,gi_codec
archive=root/'install/DevKit_v19.14.41.rar'
manifest=json.loads((root/'original-file-sha256.json').read_text('utf-8'))['files']
output=root/'dist/DevKit_v19.14.41_FROM_SOURCE_MIXED.zip';output.parent.mkdir(exist_ok=True)
with ZipFile(archive) as old,ZipFile(output,'w',ZIP_DEFLATED) as out:
 for path in old.namelist():
  if path.endswith('/'):continue
  raw=old.read(path)
  relative=path.split('Mods/Tweaks/DevKit/')[-1]
  candidate=root/'source'/(relative+'.json')
  if candidate.is_file():
   obj=json.loads(candidate.read_text('utf-8'))
   raw=dat_codec.encode(obj) if relative.endswith('.dat') else gi_codec.encode(obj)
  original=manifest[path]['sha256']
  if hashlib.sha256(raw).hexdigest()!=original:print('CHANGED',path)
  out.writestr(path,raw)
print('Built',output)
