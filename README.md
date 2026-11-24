# maggilish.com

App-style website for Maggilish: Maggie, licensed esthetician at The Gentlemen's Barbershop in Modesto, CA. Skin, brows, lashes and makeup. All genders welcome.

One design for everyone (the earlier "For her / For him" split was retired in November 2026). `/men/` and `/login/` now redirect to the home page.

- `index.html`: hero, full service menu with prices, Meet Maggie, "Your visit", care tips, shop teaser.
- `book/`: booking buttons and a price summary. `tips/`: Meet Maggie and care tips. `shop/`: Borboleta lash and brow care (affiliate).
- Phone: bottom tab bar with a raised Book button. Computer (1200px+): espresso side menu and a right-hand panel.

## Editing
All content lives in `tools/build.py`: `CONTACT` (booking link, socials), `MENU` (services and prices, from Maggie's Public Service Menu PDF), `CARE_TIPS`, `VISIT`, `BORBOLETA`. Edit, then run:

```
python3 tools/build.py
```

Styles: `assets/site.css`. Bump `V` in `build.py` after CSS changes so browsers reload it.

## Booking
Set `CONTACT['booking_url']` to Maggie's Setmore page and rebuild. Until then every Book button opens Instagram (@maggilish).

## Borboleta affiliate shop
Set `BORBOLETA['url']` to Maggie's assigned referral link and add products as `(name, image, link)` using Borboleta's approved images and exact product names. Program rules to keep:
- The commission disclosure stays right next to the shop link (already built in).
- Appearance claims only ("longer-looking lashes"); never say a serum grows lashes.
- No competing lash or brow serums anywhere on the site.
- Any usage directions must match Borboleta's exactly.

## Brand
Neutral palette from the brand guide: Porcelain `#F5EEE6`, Espresso `#251816`, Cocoa `#7D4D39`, Mink `#A69A94`, Champagne gold `#B8955A`.
Logo is solid gold per Maggie's request (Nov 15, 2026), no two-tone: `assets/brand/*-gold.svg` on dark grounds, `*-gold-deep.svg` on light grounds. MAGGILISH wordmark: Nimbus Roman Regular, all caps, about +0.14 em tracking.

## Photos
All photos are Maggie's own (studio shoot plus images she sent Nov 15, 2026). Stock and concept-product images were removed.

## Hosting
GitHub Pages from `main` (root) with the custom domain in `CNAME`.
