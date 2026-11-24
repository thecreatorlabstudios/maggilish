#!/usr/bin/env python3
"""Builds the static Maggilish site. Edit content here, then run:  python3 tools/build.py
Outputs index.html, book/, tips/, shop/, 404.html (and a /men/ redirect) at the repo root (GitHub Pages)."""
import os, json, html as _h
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V='20261123.1'   # bump to make browsers reload site.css / site.js

# ------------------------------------------------------------------ settings
SITE='https://maggilish.com'
# Booking and phone/email: buttons only appear once a value is set.
CONTACT={
 'booking_url':'',          # Maggie's Setmore booking page (pending)
 'instagram':'maggilish',
 'facebook':'https://www.facebook.com/profile.php?id=100063951256102',
 'tiktok':'maggilish',
 'phone':'', 'email':'',
}
LOCATION="The Gentlemen&#8217;s Barbershop"
CITY='Modesto, California'

# Borboleta affiliate program. Paste Maggie's assigned referral link into 'url'.
# Products: (name exactly as Borboleta names it, Borboleta-approved image path under /assets/, product link or '' to use 'url').
# Program rules: describe appearance only ("longer-looking lashes", never "grows"), no competing lash/brow serums
# anywhere on the site, use Borboleta's approved images and names unchanged, keep the commission disclosure next to the link.
BORBOLETA={'url':'', 'products':[]}

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
 'fb':'<path d="M14 21v-8h3l.5-4H14V7.5c0-1 .4-1.5 1.5-1.5h2V2.5h-3C11.5 2.5 10 4.3 10 7v2H7v4h3v8"/>',
 'tiktok':'<path d="M14 4v10.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 4c.5 2.6 2.4 4.4 5 4.6"/>',
 'pin':'<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
 'brush':'<path d="M14.5 4.5l5 5-8 8-5-5z"/><path d="M6.5 12.5C4 13 3.5 16 3 20c4-.5 7-1 7.5-3.5"/>',
}
def ic(n,s=22): return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" style="width:{s}px;height:{s}px">{I[n]}</svg>'

# ------------------------------------------------------------------ service menu (from Maggilish_Public_Service_Menu.pdf, Nov 2026)
# (id, icon, short label, eyebrow, title, intro, photo or None, [(name, price, meta, description)], note)
MENU=[
 ('skin','drop','Skin','Your skin. Your schedule.','Face <em>the day.</em>','Chair-based facials, personalized to your skin.','img/lash-treatment.webp',
  [('The Fresh Start','$35','20 min · Cleanse + hydrate','A quick refresh with cleansing, a hydrating mask, moisturizer and SPF.'),
   ('The Glow-Up','$55','35 min · Exfoliate + refresh','Cleansing, suitable exfoliation and a customized mask, finished with moisturizer and SPF.'),
   ('The Main Event','$75','50 min · The full facial','Includes everything in The Glow-Up, plus face and neck massage for a more complete care experience.')],
  'Treatment times shown. Allow time for check-in.'),
 ('enhance','spark','Add-ons','Chosen for your skin.','Make it <em>personal.</em>',None,None,
  [('Pore Focus','+$15','Targeted extractions','Add dedicated time for suitable surface congestion. Includes up to 10 minutes of gentle extractions; not every blemish is suitable for removal. Available with The Glow-Up or The Main Event.'),
   ('A fresh seasonal focus','Ask','Seasonal facial','Ask about the current seasonal facial. Featured products are selected for your skin, with suitable alternatives when needed.')],
  'Any added service and price are agreed on before treatment.'),
 ('brows','brow','Brows','Definition, your way.','Find <em>your shape.</em>','Keep your character. Refine the details.','img/maggie-at-work.webp',
  [('Brow Cleanup','$20','','Maintain an established shape with stray-hair removal and trimming as needed. A neat finish that still looks like you.'),
   ('Signature Brow Shaping','$40','','Consultation, brow mapping and customized shaping, with precise finishing to suit your features and preferred fullness.'),
   ('Brow Definition','$30','','')],
  'Not sure which to choose? Ask Maggie.'),
 ('lashes','eye','Lashes','A more defined everyday.','Lift <em>your look.</em>',None,'img/lash-detail.webp',
  [('Lash Lift','$65','','Enhance the lift and curl of your natural lashes. Includes a consultation, customized lift and aftercare guidance.'),
   ('Brow Lamination','$65','','Redirect brow hairs for a more uniform, styled finish. Includes consultation and aftercare guidance; shaping is separate.'),
   ('Lamination + Shaping','$75','','Pair brow lamination with personalized shaping and cleanup for a coordinated finish.'),
   ('Lash Definition','$30','','')],
  'Lift / lamination: about 45 minutes of service; timing varies.'),
 ('waxing','leaf','Waxing','Small details. Strong finish.','Clean <em>&amp; polished.</em>',None,None,
  [('Upper Lip','$12','','Targeted removal above the lip.'),
   ('Chin','$12','','Focused removal across the chin.'),
   ('Cheeks','$15','','Both cheeks; excludes sideburns.'),
   ('Sideburns','$15','','Both sides, tailored to your preferred outline.'),
   ('Nose','$15','','Visible hair at the outer nostril opening only.'),
   ('Full Face','$45','','Lip, chin, cheeks and sideburns; excludes brows and nose.'),
   ('Full Face + Brow Cleanup','$60','','Full-face waxing plus maintenance of your existing brow shape.')],
  None),
 ('makeup','brush','Makeup','For the moments that matter.','Show up <em>as yourself.</em>',None,'img/makeup-bridal.webp',
  [('Special-Occasion Makeup','$175','','A personalized look with consultation, skin preparation, makeup application and a final check with you.'),
   ('Makeup Preview (Trial)','$100','','A consultation and one complete makeup look, with time to refine the details before your event. Booked and charged separately from event-day makeup.')],
  'Travel available by arrangement; fee varies by distance and is quoted before booking. Bridal inquiries welcome. Makeup appointments require a 60% booking deposit.'),
]
CATS=[m for m in MENU if m[0]!='enhance']

def menu_section(m):
    mid,icon,short,eyebrow,title,intro,img,items,note=m
    rows=''.join(f'<li><div class="mi-h"><h4>{n}</h4><span class="price">{p}</span></div>'
                 +(f'<p class="mi-meta">{meta}</p>' if meta else '')+(f'<p class="mute">{d}</p>' if d else '')+'</li>' for n,p,meta,d in items)
    photo=f'<div class="menu-ph brand-photo"><img src="/assets/{img}" alt="" width="1200" height="800" loading="lazy"></div>' if img else ''
    return (f'<section class="card menu-sec{" has-ph" if img else ""}" id="{mid}" aria-labelledby="{mid}-h">{photo}<div class="menu-body">'
            f'<span class="lab">{eyebrow}</span><h3 id="{mid}-h">{title}</h3>'+(f'<p class="mute menu-intro">{intro}</p>' if intro else '')+
            f'<ul class="menu-list">{rows}</ul>'+(f'<p class="menu-note">{note}</p>' if note else '')+'</div></section>')

def price_list():
    return '<div class="cs-list">'+''.join(
        f'<div class="card"><span class="c">{ic(m[1],22)}</span><div><h3>{m[2]}</h3><p class="mute">'
        +' · '.join(f'{n} {p}' for n,p,_,_ in m[7])+'</p></div></div>' for m in MENU)+'</div>'

# ------------------------------------------------------------------ people & tips
def meet_maggie(full=False):
    return f'''<section class="card meet-maggie" aria-label="Meet Maggie">
<div class="brand-photo"><img src="/assets/img/maggie-headshot.webp" alt="Maggie, licensed esthetician and founder of Maggilish" width="1122" height="1402" loading="lazy"></div>
<div class="meet-copy"><span class="lab">Licensed esthetician · Founder</span><h2>Meet <em>Maggie.</em></h2>
<p class="mute">Maggie is the licensed esthetician behind Maggilish in Modesto. Skin, brows, lashes and makeup, with thoughtful details and individual attention for every client.</p>
<p class="mute">Tell Maggie your goals and preferences. Your service is tailored to your skin, features and comfort, and you leave with relevant aftercare and a clear next step.</p>
{'<p class="signature">Your glow. Her passion.</p>' if full else '<a class="btn ghost" href="/tips/">Meet Maggie &amp; care tips '+ic('arrow',16)+'</a>'}</div></section>'''

CARE_TIPS=[
 ('Before your visit','Arrive with a clean canvas.','Skip mascara and eye makeup before a lash or brow appointment. A clean starting point leaves more time for your service.'),
 ('Make it personal','Bring your inspiration.','Save a photo of the look you like and share what you want to keep about your natural features. Talk it through before your service begins.'),
 ('After your visit','Keep your aftercare close.','Ask Maggie for the care instructions for your specific treatment, including when to use makeup and how to cleanse. Follow the timing you are given.'),
 ('Between appointments','Be gentle with your results.','Avoid tugging or picking at your lashes and brows. If you are unsure about a product or your next appointment, ask before trying something new.')]
VISIT=[('A visit that fits your day.','Facials are performed in the barber chair in a shared space with music and conversation.'),
       ('Care that starts with listening.','Tell Maggie your goals and preferences. Your service is tailored to your skin, features and comfort.'),
       ('A little guidance to take with you.','Leave with relevant aftercare and a clear next step. New to professional care? Questions are welcome.')]

def tips_page():
    cards=''.join(f'<article class="card care-tip"><span class="lab">{label}</span><h3>{title}</h3><p class="mute">{copy}</p></article>' for label,title,copy in CARE_TIPS)
    body=f'''<section class="cs tips-page"><div class="sec-h"><div><span class="lab">Maggilish · Care notes</span><h1>Little tips. <em>Thoughtful care.</em></h1></div></div>
{meet_maggie(True)}
<div class="sec-h"><h2>Before &amp; after <em>your visit</em></h2></div>
<p class="mute tips-intro">A few simple ways to get ready and care for your results. Your appointment-specific instructions always come first.</p>
<div class="care-grid">{cards}</div>
<figure class="care-photo brand-photo"><img src="/assets/img/lash-care.webp" alt="Maggie carefully working on a client's lashes" width="1800" height="1200" loading="lazy"><figcaption>Thoughtful details, from your appointment to your care at home.</figcaption></figure>
<div class="sec-h"><h2>Have a question?</h2></div><p class="mute">Bring it to your visit or send Maggie a message. She can walk you through your service and the aftercare that goes with it.</p>
<div class="btn-row">{contact_buttons()}</div></section>'''
    page('tips/index.html','Meet Maggie &amp; care tips · Maggilish','Meet Maggie, licensed esthetician behind Maggilish in Modesto, and explore simple preparation and aftercare tips.',body,'Tips')

# ------------------------------------------------------------------ shell
NAV=[('home','Home','/'),('grid','Services','/#services'),('cal','Book','/book/'),('tips','Tips','/tips/'),('bag','Shop','/shop/')]
def book_href():
    return CONTACT['booking_url'] or f'https://instagram.com/{CONTACT["instagram"]}'
def contact_buttons(cls='btn ghost'):
    out=''
    if CONTACT['booking_url']: out+=f'<a class="btn" href="{CONTACT["booking_url"]}" rel="noopener">{ic("cal",18)}Book online</a>'
    if CONTACT['instagram']: out+=f'<a class="{cls if CONTACT["booking_url"] else "btn"}" href="https://instagram.com/{CONTACT["instagram"]}" rel="noopener">{ic("insta",18)}Message @{CONTACT["instagram"]}</a>'
    if CONTACT['phone']: out+=f'<a class="{cls}" href="sms:{CONTACT["phone"]}">{ic("chat",18)}Text Maggie</a>'
    if CONTACT['email']: out+=f'<a class="{cls}" href="mailto:{CONTACT["email"]}">{ic("chat",18)}Email Maggie</a>'
    return out
def socials():
    out=[]
    if CONTACT['instagram']: out.append((f'https://www.instagram.com/{CONTACT["instagram"]}/','insta','Instagram'))
    if CONTACT['facebook']: out.append((CONTACT['facebook'],'fb','Facebook'))
    if CONTACT['tiktok']: out.append((f'https://www.tiktok.com/@{CONTACT["tiktok"]}','tiktok','TikTok'))
    return '<div class="socials">'+''.join(f'<a href="{u}" rel="noopener" aria-label="Maggilish on {l}">{ic(i,20)}</a>' for u,i,l in out)+'</div>'

def page(path,title,desc,body,active,rail=''):
    nav_side=''.join(f'<a href="{u}"{" aria-current=page" if l==active else ""}>{ic(i,20)}{l}</a>' for i,l,u in NAV)
    tabs=''
    for i,l,u in NAV:
        cur=' aria-current="page"' if l==active else ''
        if l=='Book': tabs+=f'<a class="book" href="{u}"{cur}><span class="b">{ic(i,24)}</span>{l}</a>'
        else: tabs+=f'<a href="{u}"{cur}>{ic(i,23)}{l}</a>'
    canon=SITE+'/'+(path.replace('index.html','') if path!='index.html' else '')
    html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#F5EEE6">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/assets/img/og.jpg">
<link rel="icon" href="/assets/brand/favicon-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Maggilish">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={V}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="app">
<aside class="side dark" aria-label="Main menu">
<a class="logo" href="/"><img src="/assets/brand/nimbus-wordmark-gold.svg" alt="Maggilish" width="200" height="74"></a>
<nav>{nav_side}</nav>
<div class="help"><img src="/assets/brand/emblem-gold.webp" alt="" width="42" height="37">
<h3>{LOCATION}</h3><p class="mute">{CITY}</p>{socials()}</div>
</aside>
<div class="content">
<header class="top">
<a class="logo" href="/" aria-label="Maggilish home"><img src="/assets/brand/nimbus-wordmark-gold-deep.svg" alt="Maggilish" width="120" height="44"></a>
<div class="hello">Licensed esthetician · Skin, brows, lashes &amp; makeup</div>
<div class="actions"><a class="btn sm" href="{book_href()}" rel="noopener">Book</a></div>
</header>
<main id="main">{body}
</main>
<footer class="foot dark">
<img src="/assets/brand/nimbus-stacked-gold.svg" alt="Maggilish, your glow, her passion" width="140" height="137" loading="lazy">
<nav aria-label="Footer"><a href="/#services">Services</a><a href="/book/">Book</a><a href="/tips/">Tips</a><a href="/shop/">Shop</a></nav>
{socials()}
<p>Licensed esthetician · {LOCATION} · {CITY}</p><p>All genders welcome</p><p>&#169; 2026 Maggilish Brands LLC</p>
</footer>
</div>
</div>
<nav class="tabbar" aria-label="Main menu">{tabs}</nav>
</body>
</html>'''
    out=os.path.join(ROOT,path); os.makedirs(os.path.dirname(out),exist_ok=True)
    open(out,'w').write(html)

# ------------------------------------------------------------------ home
def home():
    cats=''.join(f'<a href="#{m[0]}"><span class="c">{ic(m[1],24)}</span>{m[2]}</a>' for m in CATS)
    menu=''.join(menu_section(m) for m in MENU)
    tips=''.join(f'<li><a href="/tips/"><span class="q">{title}</span>{ic("arrow",18)}</a></li>' for _,title,_ in CARE_TIPS[:3])
    visit=''.join(f'<div class="card step"><span class="n">{i}</span><div><h3>{t}</h3><p class="mute">{d}</p></div></div>' for i,(t,d) in enumerate(VISIT,1))
    body=f'''<div class="greet"><p class="mute" style="font-size:13px">Welcome in</p><h1>What can I do for you?</h1></div>
<div class="home-grid"><div>
<section class="hero" style="background-image:url(/assets/img/maggie-at-work.webp)" aria-label="Welcome">
<div class="in"><span class="lab">Licensed esthetician · Modesto</span><h2 style="margin-top:8px">Personal care.<br><em>At your pace.</em></h2>
<p class="mute">Skin, brows, lashes and makeup with Maggie at {LOCATION}. All genders welcome.</p>
<a class="btn" href="/book/">Book a visit {ic('arrow',16)}</a></div></section>
<nav class="cats" aria-label="Service categories">{cats}</nav>
<div class="sec-h" id="services"><h2>Services <em>&amp; pricing</em></h2><a href="/book/">Book {ic('arrow',14)}</a></div>
<div class="menu">{menu}</div>
<div class="sec-h"><h2>Personal beauty. <em>A familiar face.</em></h2></div>
{meet_maggie()}
<section class="band dark">
<span class="lab">You belong here</span><h2>Good <em>energy.</em></h2>
<p class="mute">Personal attention, in a lively barbershop setting at {LOCATION}.</p>
<div class="steps">{visit}</div>
<div class="btn-row">{contact_buttons()}</div></section>
<div class="sec-h"><h2>Care <em>tips</em></h2><a href="/tips/">Explore tips {ic("arrow",14)}</a></div>
<div class="card tips-teaser"><p class="mute" style="font-size:14px">A little preparation, a gentle routine and room for your questions.</p><ul>{tips}</ul></div>
<div class="sec-h"><h2>Lash &amp; brow <em>care</em></h2><a href="/shop/">Shop {ic("arrow",14)}</a></div>
<a class="feature" href="/shop/" style="background-image:url(/assets/img/lash-care.webp)">
<div class="in"><span class="lab">Maggie&#8217;s picks</span><h2>Aftercare, <em>chosen by Maggie.</em></h2><p>Lash and brow care from Borboleta, the brand Maggie recommends after a lash lift or brow lamination.</p></div></a>
<div class="sec-h"></div>
<section class="promise dark"><img src="/assets/brand/emblem-gold.webp" alt="" width="74" height="64" loading="lazy">
<h2>Healthy skin first. <em>Beautiful skin follows.</em></h2>
<p class="mute">Thoughtful details. Individual attention. A polished finish that feels like you.</p></section>
</div>{rail()}</div>'''
    page('index.html','Maggilish · Licensed esthetician in Modesto · Skin, brows, lashes &amp; makeup',
         'Facials, brow shaping, lash lifts, facial waxing and special-occasion makeup with Maggie, licensed esthetician at The Gentlemen&#8217;s Barbershop in Modesto, California. All genders welcome.',body,'Home')

def rail():
    return f'''<aside class="rail rail-only" aria-label="Quick info">
<div class="card" style="padding:20px"><span class="lab">Book</span><h3 style="font-size:24px;margin-top:6px">Ready when <em>you are.</em></h3>
<p class="mute" style="font-size:13.5px;margin-top:8px">{ic('pin',14)} {LOCATION}, {CITY}</p>
<div style="display:grid;gap:8px;margin-top:14px">{contact_buttons()}</div></div>
<div class="card" style="padding:20px"><div class="brand-photo rail-portrait"><img src="/assets/img/maggie-brand.webp" alt="Maggie with the Maggilish brand mirror" width="1800" height="1200" loading="lazy"></div><span class="lab">Follow along</span>
{socials()}
<a class="btn ghost" href="/tips/" style="margin-top:14px">Meet Maggie &amp; care tips</a></div>
</aside>'''

# ------------------------------------------------------------------ book & shop
def book_page():
    ready=bool(CONTACT['booking_url'])
    body=f'''<section class="cs">
<div class="cs-hero" style="background-image:url(/assets/img/studio-visit.webp)"><div class="in"><span class="lab">{LOCATION} · Modesto</span><h1>Book <em>your visit.</em></h1>
<p>{'Pick a service and a time online in under a minute.' if ready else 'Message Maggie on Instagram to book. Online booking is on the way.'}</p></div></div>
<div class="btn-row">{contact_buttons()}</div>
<p class="mute note">Makeup appointments require a 60% booking deposit. Any added service and price are agreed on before treatment.</p>
<div class="sec-h"><h2>What you can <em>book</em></h2><a href="/#services">Full menu {ic('arrow',14)}</a></div>
{price_list()}</section>'''
    page('book/index.html','Book · Maggilish','Book facials, brows, lash lifts, waxing and makeup with Maggie, licensed esthetician at The Gentlemen&#8217;s Barbershop in Modesto.',body,'Book')

DISCLOSURE=('Maggilish is a Borboleta affiliate. If you buy through these links, Maggilish earns a commission '
            'from your purchase, at no extra cost to you.')
def shop_page():
    b=BORBOLETA; url=b['url']
    cta=(f'<a class="btn" href="{url}" rel="sponsored noopener" target="_blank">{ic("bag",18)}Shop Borboleta</a>' if url
         else '<span class="btn ghost" aria-disabled="true">Shop link coming soon</span>')
    prods=''.join(f'<a class="card prod" href="{u or url}" rel="sponsored noopener" target="_blank"><div class="ph" style="background-image:url(/assets/{img})" role="img" aria-label="{n}"></div><h3>{n}</h3><p class="mute">Shop at Borboleta</p></a>'
                  for n,img,u in b['products'])
    body=f'''<section class="cs">
<div class="cs-hero" style="background-image:url(/assets/img/lash-care.webp)"><div class="in"><span class="lab">Maggie&#8217;s picks</span><h1>Lash &amp; brow care, <em>chosen by Maggie.</em></h1>
<p>Aftercare and lash and brow serums from Borboleta. Great options to explore after a lash lift or brow lamination, for longer-looking lashes and fuller-looking brows.</p></div></div>
<section class="card shop-box"><div><span class="lab">Shop Borboleta</span><h2>Maggie&#8217;s <em>Borboleta picks</em></h2>
<p class="disclosure">{ic('spark',16)}<span>{DISCLOSURE}</span></p></div>
<div class="btn-row">{cta}</div></section>
{f'<div class="prod-grid">{prods}</div><p class="disclosure small">{DISCLOSURE}</p>' if prods else ''}
<p class="mute note">Follow the directions included with your Borboleta product. Questions about your lashes or brows after a service? Ask Maggie at your next visit.</p>
</section>'''
    page('shop/index.html','Shop lash &amp; brow care · Maggilish','Lash and brow care from Borboleta, recommended by Maggie, licensed esthetician in Modesto. Maggilish earns a commission on purchases through these links.',body,'Shop')

def redirect(path,to='/'):
    out=os.path.join(ROOT,path); os.makedirs(os.path.dirname(out),exist_ok=True)
    open(out,'w').write(f'<!doctype html><meta charset="utf-8"><title>Maggilish</title><link rel="canonical" href="{SITE}{to}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={to}"><a href="{to}">Continue to Maggilish</a>\n')

def build():
    home(); book_page(); tips_page(); shop_page()
    redirect('men/index.html'); redirect('login/index.html')
    open(os.path.join(ROOT,'CNAME'),'w').write('maggilish.com\n')
    open(os.path.join(ROOT,'.nojekyll'),'w').write('')
    open(os.path.join(ROOT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    urls=['/','/book/','/tips/','/shop/']
    open(os.path.join(ROOT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{SITE}{u}</loc></url>\n' for u in urls)+'</urlset>\n')
    json.dump({'name':'Maggilish','short_name':'Maggilish','start_url':'/','display':'standalone','background_color':'#F5EEE6','theme_color':'#F5EEE6',
               'icons':[{'src':'/assets/brand/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'/assets/brand/icon-512.png','sizes':'512x512','type':'image/png'}]},
              open(os.path.join(ROOT,'manifest.webmanifest'),'w'),indent=1)
    page('404.html','Page not found · Maggilish','Page not found',
         '<section class="cs"><div class="card" style="padding:28px;text-align:center"><h1 style="font-size:34px">This page <em>isn&#8217;t here.</em></h1><p class="mute" style="margin-top:8px">Let&#8217;s get you back.</p><a class="btn" href="/" style="margin-top:16px">Go home</a></div></section>','')
    print('built')
if __name__=='__main__': build()
