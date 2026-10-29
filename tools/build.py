#!/usr/bin/env python3
"""Builds the static Maggilish site. Edit content here, then run:  python3 tools/build.py
Outputs index.html, men/index.html, book/, tips/, shop/ at the repo root (GitHub Pages)."""
import os, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------ settings
SITE='https://maggilish.com'
# Fill these in when Maggie confirms them; buttons only appear once they are set.
CONTACT={'instagram':'', 'phone':'', 'email':'', 'booking_url':''}

# ------------------------------------------------------------------ icons
I={
 'home':'<path d="M3 11 12 4l9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
 'grid':'<rect x="4" y="4" width="7" height="7" rx="2"/><rect x="13" y="4" width="7" height="7" rx="2"/><rect x="4" y="13" width="7" height="7" rx="2"/><rect x="13" y="13" width="7" height="7" rx="2"/>',
 'cal':'<rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
 'tips':'<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
 'bag':'<path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
 'clock':'<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'eye':'<path d="M2.5 12S6 6 12 6s9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6z"/><circle cx="12" cy="12" r="2.5"/>',
 'brow':'<path d="M3 13c4-5 11-6 18-2"/><path d="M5 17c3-1.5 7-1.8 11-.6"/>',
 'spark':'<path d="M12 3l1.6 6.4L20 11l-6.4 1.6L12 19l-1.6-6.4L4 11l6.4-1.6z"/>',
 'leaf':'<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15z"/><path d="M5 19l8-8"/>',
 'drop':'<path d="M12 3C8.5 8 6 11 6 14.5a6 6 0 0 0 12 0C18 11 15.5 8 12 3z"/>',
 'face':'<circle cx="12" cy="12" r="8.5"/><path d="M9 10h.01M15 10h.01M9 15c1.7 1.3 4.3 1.3 6 0"/>',
 'plus':'<path d="M12 5v14M5 12h14"/>',
 'chat':'<path d="M4 5h16v11h-9l-5 4v-4H4z"/>',
 'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>',
 'insta':'<rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.6"/><path d="M16.6 7.4h.01"/>',
}
def ic(n,s=22): return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" style="width:{s}px;height:{s}px">{I[n]}</svg>'

# ------------------------------------------------------------------ content
# Times are drafts until Maggie confirms them. Prices are intentionally not shown yet.
SERV={
 'her':[('eye','Lashes','Lash lift &amp; tint','45 min','A natural curl and a deeper tint that lasts for weeks. No extensions, no mascara needed.','img/her-lashlift.webp'),
        ('brow','Brows','Brow shaping &amp; tint','30 min','Shaped to your face and tinted for fuller, defined brows.','img/her-brows.webp'),
        ('spark','Combo','Lash lift + brow shape','75 min','The full eye refresh in one visit.',None),
        ('leaf','Waxing','Facial waxing','15 min','Lip and chin, gentle and quick.',None),
        ('drop','Facials','Signature facial',None,'Facials are coming soon.','img/facial.webp')],
 'his':[('brow','Brows','Brow clean-up','15 min','Tidy and natural, never over-shaped.','img/his-brows.webp'),
        ('spark','Tint','Brow tint','15 min','Fills in sparse or light brows without looking done.',None),
        ('eye','Lashes','Lash tint','20 min','Darker lashes, no mascara, nobody can tell.',None),
        ('leaf','Waxing','Facial waxing','15 min','Brow, ear and nose, quick and clean.',None),
        ('face','Facials','Men&#8217;s facial',None,'Men&#8217;s facials are coming soon.','img/his-studio.webp')],
}
HERO={'her':dict(img='img/her-hero.webp',h='Lifted lashes.<br><em>Defined brows.</em>',p='Lash lifts and brow shaping with Maggie in Modesto. Facials coming soon.',greet='Hello, welcome in'),
      'his':dict(img='img/his-hero.webp',h='Clean brows.<br><em>No guesswork.</em>',p='Brow clean-ups, tints and waxing, explained plainly. Men&#8217;s facials coming soon.',greet='Welcome in')}
TIPQ={'her':['How long does a lash lift last?','Can I wear mascara after a lash lift?','How do I prep for a brow wax?'],
      'his':['How do I clean up my brows without overdoing it?','How do I stop razor bumps?','Will a lash tint look obvious?']}

# ------------------------------------------------------------------ shell
NAV=[('home','Home','/'),('grid','Services','/#services'),('cal','Book','/book/'),('tips','Tips','/tips/'),('bag','Shop','/shop/')]
SOON={'Book','Tips','Shop'}
def contact_buttons(cls='btn ghost'):
    out=''
    if CONTACT['booking_url']: out+=f'<a class="btn" href="{CONTACT["booking_url"]}">{ic("cal",18)}Book online</a>'
    if CONTACT['instagram']: out+=f'<a class="{cls}" href="https://instagram.com/{CONTACT["instagram"]}">{ic("insta",18)}Message on Instagram</a>'
    if CONTACT['phone']: out+=f'<a class="{cls}" href="sms:{CONTACT["phone"]}">{ic("chat",18)}Text Maggie</a>'
    return out
def toggle():
    return ('<div class="toggle" role="group" aria-label="Show services for">'
            '<button type="button" data-side="her" aria-pressed="true">For her</button>'
            '<button type="button" data-side="his" aria-pressed="false">For him</button></div>')
def page(path,title,desc,body,active,side='her',force=None,rail=''):
    depth=path.count('/')
    nav_side=''.join(f'<a href="{u}"{" aria-current=page" if l==active else ""}>{ic(i,20)}{l}{"<span class=soon>Soon</span>" if l in SOON else ""}</a>' for i,l,u in NAV)
    tabs=''
    for i,l,u in NAV:
        cur=' aria-current="page"' if l==active else ''
        if l=='Book': tabs+=f'<a class="book" href="{u}"{cur}><span class="b">{ic(i,24)}</span>{l}</a>'
        else: tabs+=f'<a href="{u}"{cur}>{ic(i,23)}{l}</a>'
    help_=('<div class="card help for-{s}"><img src="/assets/brand/emblem-{t}.webp" alt="" width="42" height="37">'
           '<h3>Booking opens soon</h3><p class="mute">Online booking is on the way.</p></div>')
    helpbox=''.join(help_.format(t=t,s=s) for s,t in (('her','light'),('his','dark')))
    canon=SITE+'/'+(path.replace('index.html','') if path!='index.html' else '')
    demo_entry = "<script>/* Demo entry screen only; not a security boundary. */(function(){try{if(sessionStorage.getItem('maggilish-demo-access')==='yes')return;}catch(e){}window.location.replace('/login/');})();</script>" if path == 'index.html' else ''
    html=f'''<!doctype html>
<html lang="en" data-side="{side}"{f' data-force="{force}"' if force else ''}>
<head>
{demo_entry}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="{'#151311' if side=='his' else '#F5EEE6'}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/assets/img/og.jpg">
<link rel="icon" href="/assets/brand/favicon-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Maggilish">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=20261029.2">
<script>(function(){{try{{var s=localStorage.getItem('maggilish-side');var f=document.documentElement.getAttribute('data-force');if(!f&&s)document.documentElement.setAttribute('data-side',s);}}catch(e){{}}}})();</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="app">
<aside class="side" aria-label="Main menu">
<a class="logo" href="/"><img class="for-her" src="/assets/brand/script-light.webp" alt="Maggilish" width="200" height="74"><img class="for-his" src="/assets/brand/script-dark.webp" alt="Maggilish" width="200" height="74"></a>
<nav>{nav_side}</nav>
{helpbox}
</aside>
<div class="content">
<header class="top">
<a class="logo" href="/" aria-label="Maggilish home"><img class="for-her" src="/assets/brand/script-light.webp" alt="Maggilish" width="103" height="38"><img class="for-his" src="/assets/brand/script-dark.webp" alt="Maggilish" width="103" height="38"></a>
<div class="hello rail-hide">Maggilish · Personal beauty, thoughtful care</div>
<div class="actions">{toggle()}</div>
</header>
<main id="main">{body}
<footer class="foot">
<img class="for-her" src="/assets/brand/logo-light.webp" alt="Maggilish, your glow, her passion" width="120" height="118">
<img class="for-his" src="/assets/brand/logo-dark.webp" alt="Maggilish, your glow, her passion" width="120" height="118">
<nav aria-label="Footer"><a href="/#services">Services</a><a href="/book/">Book</a><a href="/tips/">Tips</a><a href="/shop/">Shop</a><a href="/men/">For him</a></nav>
<p>Lashes &amp; brows · Modesto, California</p><p>&#169; 2026 Maggilish</p>
</footer>
</main>
</div>
</div>
<nav class="tabbar" aria-label="Main menu">{tabs}</nav>
<script src="/assets/site.js?v=20261029.2" defer></script>
</body>
</html>'''
    out=os.path.join(ROOT,path); os.makedirs(os.path.dirname(out),exist_ok=True)
    open(out,'w').write(html)

# ------------------------------------------------------------------ home
def svc_card(s,side):
    i,c,n,d,desc,img=s
    ph=f'<div class="ph" style="background-image:url(/assets/{img})" role="img" aria-label="{n}"></div>' if img else f'<div class="ph">{ic(i,38)}</div>'
    if d is None:
        return (f'<article class="card svc">{ph}<span class="soon">Coming soon</span><div class="body"><h3>{n}</h3><p class="mute">{desc}</p>'
                f'<div class="meta"><span class="lab" style="font-size:10px">{c}</span><span class="t">Opening soon</span></div></div></article>')
    return (f'<article class="card svc">{ph}<div class="body"><h3>{n}</h3><p class="mute">{desc}</p>'
            f'<div class="meta"><span class="t">{ic("clock",14)}{d}</span><a class="plus" href="/book/" aria-label="Book {n}">{ic("plus",16)}</a></div></div></article>')
def side_block(side):
    h=HERO[side]; S=SERV[side]
    cats=''.join(f'<a href="#services"><span class="c">{ic(s[0],24)}</span>{s[1]}</a>' for s in S)
    cards=''.join(svc_card(s,side) for s in S)
    tips=''.join(f'<li><span class="q">{q}</span>{ic("arrow",18)}</li>' for q in TIPQ[side])
    feat_img='img/studio.webp' if side=='her' else 'img/his-studio.webp'
    return f'''<div class="for-{side}">
<section class="hero" style="background-image:url(/assets/{h['img']})" aria-label="Welcome">
<div class="in"><span class="lab">Maggilish · Modesto</span><h2 style="margin-top:8px">{h['h']}</h2><p class="mute">{h['p']}</p>
<a class="btn" href="/book/">Book a visit {ic('arrow',16)}</a></div></section>
<nav class="cats" aria-label="Service categories">{cats}</nav>
<div class="sec-h" id="services"><h2>Services</h2><a href="/book/">Book {ic('arrow',14)}</a></div>
<div class="svc-grid">{cards}</div>
<div class="sec-h"><h2>How a visit <em>works</em></h2></div>
<div class="steps">
<div class="card step"><span class="n">1</span><div><h3>Pick your service</h3><p class="mute">{'Lashes, brows or both. Not sure? Maggie will help you choose.' if side=='her' else 'Brows, tint or waxing. Not sure? Maggie will tell you straight.'}</p></div></div>
<div class="card step"><span class="n">2</span><div><h3>Book a time</h3><p class="mute">Online booking opens soon, so you can pick a time in under a minute.</p></div></div>
<div class="card step"><span class="n">3</span><div><h3>{'Relax and glow' if side=='her' else 'In and out'}</h3><p class="mute">{'Leave with aftercare tips so your results last.' if side=='her' else 'Quick, clean and natural. Nobody will know; they will just notice.'}</p></div></div>
</div>
<div class="sec-h"><h2>Tips</h2><span class="soon">Coming soon</span></div>
<div class="card tips-teaser"><p class="mute" style="font-size:14px">Quick answers from Maggie to everyday {'lash, brow and skin' if side=='her' else 'brow and skin'} questions, like:</p><ul>{tips}</ul></div>
<div class="sec-h"><h2>{'Maggilish <em>Skin</em>' if side=='her' else 'Maggilish <em>Men</em>'}</h2><span class="soon">Coming soon</span></div>
<a class="feature" href="/shop/" style="background-image:url(/assets/img/product-{'her-group' if side=='her' else 'his-group'}.webp);background-position:center 40%">
<div class="in"><span class="lab">Our own line is on the way</span><h2>{'A gentle routine,<br><em>made for your skin.</em>' if side=='her' else 'A five-minute routine,<br><em>made for men.</em>'}</h2><p>Concept preview. Products are in development.</p></div></a>
<div class="sec-h"></div>
<section class="promise"><img src="/assets/brand/emblem-{'light' if side=='her' else 'dark'}.webp" alt="" width="74" height="64" loading="lazy">
<h2>Healthy skin first. <em>Beautiful skin follows.</em></h2>
<p class="mute">Care before the sale, education with respect, and elegance that makes you feel welcome{', for him too' if side=='his' else ''}.</p></section>
<div class="sec-h"></div>
<a class="feature" href="/book/" style="background-image:url(/assets/{feat_img})"><div class="in"><span class="lab">The studio</span><h2>{'Calm, warm and <em>all about you.</em>' if side=='her' else 'Quiet, clean and <em>no fuss.</em>'}</h2><p>Booking opens soon.</p></div></a>
</div>'''
def rail():
    return f'''<aside class="rail rail-only" aria-label="Quick info">
<div class="card" style="padding:20px"><span class="lab">Book</span><h3 style="font-size:24px;margin-top:6px">Online booking <em>opens soon</em></h3>
<p class="mute" style="font-size:13.5px;margin-top:8px">Lash lifts, brows and waxing first. Facials follow once Maggie&#8217;s license is in place.</p>
<div style="display:grid;gap:8px;margin-top:14px">{contact_buttons() or '<span class="soon" style="justify-self:start">Coming soon</span>'}</div></div>
<div class="card" style="padding:20px"><span class="lab">Tips</span>
<ul style="list-style:none;margin-top:6px">{''.join(f'<li class="for-{s}" style="padding:10px 0;border-top:1px solid var(--line);font-family:var(--serif);font-size:17px;line-height:1.2">{q}</li>' for s in ('her','his') for q in TIPQ[s])}</ul>
<span class="soon" style="margin-top:10px">Coming soon</span></div>
</aside>'''
def home(path,side,force=None):
    body=f'''<div class="greet"><p class="mute for-her" style="font-size:13px">{HERO['her']['greet']}</p><p class="mute for-his" style="font-size:13px">{HERO['his']['greet']}</p><h1>What can I do for you?</h1></div>
<div class="home-grid"><div>{side_block('her')}{side_block('his')}</div>{rail()}</div>'''
    title='Maggilish · Lash lifts &amp; brows in Modesto' if side=='her' else 'Maggilish for Men · Brow clean-ups in Modesto'
    desc=('Lash lifts, lash tints and brow shaping with Maggie in Modesto, California. Facials coming soon.' if side=='her'
          else 'Brow clean-ups, brow and lash tints and facial waxing for men in Modesto, California. Men&#8217;s facials coming soon.')
    page(path,title,desc,body,'Home',side,force)

# ------------------------------------------------------------------ coming-soon pages
def coming(path,active,lab,h_her,h_his,p,img_her,img_his,extra):
    body=f'''<section class="cs">
<div class="cs-hero for-her" style="background-image:url(/assets/{img_her})"><div class="in"><span class="soon">Coming soon</span><h1>{h_her}</h1><p>{p}</p></div></div>
<div class="cs-hero for-his" style="background-image:url(/assets/{img_his})"><div class="in"><span class="soon">Coming soon</span><h1>{h_his}</h1><p>{p}</p></div></div>
{extra}</section>'''
    page(path,f'{lab} · Maggilish',p,body,active)
def svc_list(side):
    return '<div class="cs-list for-%s">'%side+''.join(f'<div class="card"><span class="c">{ic(s[0],22)}</span><div><h3>{s[2]}</h3><p class="mute">{s[3]+" · " if s[3] else ""}{s[4]}</p></div>{"<span class=soon style=margin-left:auto>Soon</span>" if s[3] is None else ""}</div>' for s in SERV[side])+'</div>'
def tip_list(side):
    return '<div class="cs-list for-%s">'%side+''.join(f'<div class="card"><span class="c">{ic("tips",22)}</span><div><h3 class="serif" style="font-family:var(--serif);font-size:19px">{q}</h3><p class="mute">Answer coming soon</p></div></div>' for q in TIPQ[side])+'</div>'
PRODUCTS={'her':[('her-hero','Barrier Cream'),('her-duo','Hydrating Serum'),('her-trio','Gentle Cleanser')],
          'his':[('his-hero','Recovery Balm'),('his-trio','Clarifying Wash'),('his-group','The full routine')]}
def prod_grid(side):
    return '<div class="prod-grid for-%s">'%side+''.join(f'<div class="card prod"><div class="ph" style="background-image:url(/assets/img/product-{k}.webp)" role="img" aria-label="{n} concept"></div><span class="soon">Coming soon</span><h3>{n}</h3><p class="mute">Price TBA</p></div>' for k,n in PRODUCTS[side])+'</div>'

def build():
    home('index.html','her')
    home('men/index.html','his',force='his')
    cb=contact_buttons()
    coming('book/index.html','Book','Book','Online booking <em>opens soon.</em>','Online booking <em>opens soon.</em>',
           'Pick a service and a time in under a minute. Lashes and brows first; facials follow soon.',
           'img/her-lashlift.webp','img/his-brows.webp',
           (f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">{cb}</div>' if cb else '')+
           '<div class="sec-h"><h2>What you can book</h2></div>'+svc_list('her')+svc_list('his'))
    coming('tips/index.html','Tips','Tips','Quick answers, <em>coming soon.</em>','Quick answers, <em>coming soon.</em>',
           'Short, useful answers from Maggie to everyday questions. Searchable, one minute or less.',
           'img/her-brows.webp','img/his-hero.webp',
           '<div class="sec-h"><h2>First answers</h2></div>'+tip_list('her')+tip_list('his'))
    coming('shop/index.html','Shop','Shop','Maggilish Skin <em>is on the way.</em>','Maggilish Men <em>is on the way.</em>',
           'Our own line is in development. Concept previews below; products, prices and launch date to come.',
           'img/product-her-group.webp','img/product-his-group.webp',
           prod_grid('her')+prod_grid('his')+'<p class="note mute">Images are concept renders, not final products.</p>')
    # extras
    open(os.path.join(ROOT,'CNAME'),'w').write('maggilish.com\n')
    open(os.path.join(ROOT,'.nojekyll'),'w').write('')
    open(os.path.join(ROOT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    urls=['/','/men/','/book/','/tips/','/shop/']
    open(os.path.join(ROOT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{SITE}{u}</loc></url>\n' for u in urls)+'</urlset>\n')
    json.dump({'name':'Maggilish','short_name':'Maggilish','start_url':'/','display':'standalone','background_color':'#F5EEE6','theme_color':'#F5EEE6',
               'icons':[{'src':'/assets/brand/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'/assets/brand/icon-512.png','sizes':'512x512','type':'image/png'}]},
              open(os.path.join(ROOT,'manifest.webmanifest'),'w'),indent=1)
    page('404.html','Page not found · Maggilish','Page not found',
         '<section class="cs"><div class="card" style="padding:28px;text-align:center"><h1 style="font-size:34px">This page <em>isn&#8217;t here.</em></h1><p class="mute" style="margin-top:8px">Let&#8217;s get you back.</p><a class="btn" href="/" style="margin-top:16px">Go home</a></div></section>','')
    print('built')
if __name__=='__main__': build()
