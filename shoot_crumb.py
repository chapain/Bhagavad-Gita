# -*- coding: utf-8 -*-
"""Shoot the running head (breadcrumb) across views and themes."""
import sys
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8000/index.html"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/user/downloads"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for theme in ("light", "dark"):
        dark = theme == "dark"
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(700)
        pg.evaluate(f"setTheme({str(dark).lower()}, false)")
        for js, name in [("showThemes(1)", "themes"),
                         ("showRead(1,'mula')", "read"),
                         ("showVerses(1,0)", "verses")]:
            pg.evaluate(js)
            pg.wait_for_timeout(600)
            pg.screenshot(path=f"{OUT}/crumb_{name}_{theme}.png",
                          clip={"x": 0, "y": 150, "width": 1280, "height": 420})
        # hover a crumb link to catch the saffron hover language
        pg.evaluate("showThemes(1)")
        pg.wait_for_timeout(500)
        pg.locator(".way-crumb .wc-link").nth(1).hover()
        pg.wait_for_timeout(300)
        pg.screenshot(path=f"{OUT}/crumb_hover_{theme}.png",
                      clip={"x": 0, "y": 150, "width": 1280, "height": 300})
        pg.close()
    # mobile Nepali trail
    pg = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(700)
    pg.evaluate("setLang('ne'); showVerses(1,0)")
    pg.wait_for_timeout(600)
    pg.screenshot(path=f"{OUT}/crumb_mobile_ne.png", clip={"x": 0, "y": 100, "width": 390, "height": 400})
    pg.close()
    b.close()
print("crumb shots written")
