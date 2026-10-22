# maggilish.com

App-style website for Maggilish, a lash and brow studio in Modesto, CA. One site with a side for her and a side for him.

- `index.html` (her, default) and `men/` (his) are the landing pages; the For her / For him switch remembers the visitor's choice.
- `book/`, `tips/` and `shop/` are coming-soon pages.
- Phone: bottom tab bar with a raised Book button. Computer (1200px+): side menu and a right-hand panel.

## Editing
Content lives in `tools/build.py` (services, hero copy, tips questions, contact links). Edit it, then run:

```
python3 tools/build.py
```

Styles: `assets/site.css`. Her/his switch: `assets/site.js`.

## Contact and booking
Set `CONTACT` in `tools/build.py` (Instagram handle, phone, email, booking link) and rebuild. Buttons appear only once a value is set.

## Photos
Stock photos are AI-generated and listed in `tools/photos.json`; the **Fetch photos** workflow downloads them into `assets/img/`. Replace them with Maggie's own work (with client consent) when available. Product images are concept renders, labeled as such.

## Hosting
GitHub Pages from `main` (root) with the custom domain in `CNAME`.
