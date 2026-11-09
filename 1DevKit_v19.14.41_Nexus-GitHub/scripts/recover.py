#!/usr/bin/env python3
"""Recover editable DAT and supported GI sources from DevKit v19.14.41."""
from zipfile import ZipFile
from pathlib import Path
import json,sys,hashlib
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
import dat_codec,gi_codec
archive=root/'install/DevKit_v19.14.41.rar'
source=root/'source';source.mkdir(exist_ok=True)
records={};unrecovered=[]
with ZipFile(archive) as z:
 for path in z.namelist():
  if path.endswith('/'):continue
  data=z.read(path)
  records[path]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
  relative=path.split('Mods/Tweaks/DevKit/')[-1]
  if relative.endswith('.dat'):
   fmt='cachedata' if relative.endswith('CacheData.dat') else 'blockpar'
   value=dat_codec.decode(data,fmt)
   assert dat_codec.encode(value)==data
   output=source/(relative+'.json')
  elif relative.endswith('.gi'):
   try:
    value=gi_codec.decode(data)
    assert gi_codec.encode(value)==data
   except Exception:
    unrecovered.append(relative)
    continue
   output=source/(relative+'.json')
  else:
   unrecovered.append(relative)
   continue
  output.parent.mkdir(parents=True,exist_ok=True)
  output.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n','utf-8')
(root/'original-file-sha256.json').write_text(json.dumps({'files':records,'not_editable':unrecovered},ensure_ascii=False,indent=2)+'\n','utf-8')
print('Decoded',len(records)-len(unrecovered),'of',len(records),'runtime files')
print('Unrecovered (original bytes remain in installer):',len(unrecovered))
