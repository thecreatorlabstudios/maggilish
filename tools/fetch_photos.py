#!/usr/bin/env python3
"""Downloads the photos listed in tools/photos.json into assets/img/*.webp (skips ones already present)."""
import json, os, io, urllib.request
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec=json.load(open(os.path.join(ROOT,'tools','photos.json')))
for name,v in spec.items():
    if name.startswith('_'): continue
    out=os.path.join(ROOT,'assets','img',name+'.webp')
    if os.path.exists(out): continue
    data=urllib.request.urlopen(urllib.request.Request(v['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read()
    im=Image.open(io.BytesIO(data)).convert('RGB')
    w=v.get('width',1600)
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    im.save(out,'WEBP',quality=80,method=6); print('saved',out,im.size)
og=os.path.join(ROOT,'assets','img','og.jpg'); hero=os.path.join(ROOT,'assets','img','her-hero.webp')
if not os.path.exists(og) and os.path.exists(hero):
    im=Image.open(hero).convert('RGB'); W,H=1200,630
    k=max(W/im.width,H/im.height); im=im.resize((round(im.width*k),round(im.height*k)),Image.LANCZOS)
    l=(im.width-W)//2; t=(im.height-H)//2; im=im.crop((l,t,l+W,t+H))
    logo=os.path.join(ROOT,'assets','brand','logo-light.webp')
    if os.path.exists(logo):
        lg=Image.open(logo).convert('RGBA'); lg.thumbnail((300,300)); im.paste(lg,(60,(H-lg.height)//2),lg)
    im.save(og,'JPEG',quality=82,optimize=True); print('saved',og)
