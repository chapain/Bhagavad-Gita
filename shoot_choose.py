# -*- coding: utf-8 -*-
"""Shoot the choice page: light/dark, desktop/mobile, rest + hover."""
import sys
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8000/index.html"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/user/downloads"

shots = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for theme in ("light", "dark"):
        dark = theme == "dark"
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(700)
        pg.evaluate(f"setTheme({str(dark).lower()}, false); showChoose(1);")
        pg.wait_for_timeout(700)
        assert pg.evaluate("state.view") == "choose", pg.evaluate("state.view")
        pg.screenshot(path=f"{OUT}/choose_{theme}.png")
        shots.append(f"choose_{theme}.png")
        if theme == "light":
            pg.evaluate("showChapters(1)")
            pg.wait_for_timeout(600)
            pg.screenshot(path=f"{OUT}/chapters_light_ref.png")
            shots.append("chapters_light_ref.png")
            pg.evaluate("showChoose(1)")
            pg.wait_for_timeout(600)
        pg.locator(".opt").nth(1).hover()
        pg.wait_for_timeout(500)
        pg.screenshot(path=f"{OUT}/choose_{theme}_hover.png")
        shots.append(f"choose_{theme}_hover.png")
        for i in range(3):
            box = pg.locator(".opt").nth(i)
            bd = box.evaluate("e=>getComputedStyle(e).borderTopColor")
            chip = box.locator(".chip").evaluate("e=>getComputedStyle(e).backgroundColor")
            print(f"  {theme} door{i} at rest: border={bd} chip={chip}")
        pg.locator(".opt").nth(1).hover()
        pg.wait_for_timeout(400)
        hb = pg.locator(".opt").nth(1).evaluate("e=>getComputedStyle(e).borderTopColor")
        print(f"  {theme} door1 hovered: border={hb}")
        pg.mouse.move(2,2)
        pg.wait_for_timeout(300)
        pg.close()
        pg = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(700)
        pg.evaluate(f"setTheme({str(dark).lower()}, false); setLang('ne'); showChoose(1);")
        pg.wait_for_timeout(700)
        pg.screenshot(path=f"{OUT}/choose_mobile_{theme}.png")
        shots.append(f"choose_mobile_{theme}.png")
        cols = pg.evaluate(
            "getComputedStyle(document.querySelector('.grid.choose')).gridTemplateColumns")
        print(f"  {theme} mobile grid columns: {cols}")
        pg.close()
    b.close()
print("wrote:", ", ".join(shots))
