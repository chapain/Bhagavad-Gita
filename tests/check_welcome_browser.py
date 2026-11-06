#!/usr/bin/env python3
"""Focused landing-page checks. Run against a served build with Playwright:

    GITA_CHROMIUM_EXECUTABLE=/path/to/chromium python tests/check_welcome_browser.py http://localhost:8000/

The full browser suite covers the rest of the app; this checks the responsive
first impression in all three languages and both colour schemes.
"""
import os
import shlex
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000/'
labels = {'en': 'Search', 'ne': 'खोज', 'hi': 'खोजें'}
with sync_playwright() as p:
    launch = {}
    if os.environ.get('GITA_CHROMIUM_EXECUTABLE'):
        launch['executable_path'] = os.environ['GITA_CHROMIUM_EXECUTABLE']
        launch['args'] = shlex.split(os.environ.get('GITA_CHROMIUM_ARGS', ''))
    browser = p.chromium.launch(**launch)
    for width in (320, 390, 1440):
        for lang, label in labels.items():
            for dark in (False, True):
                context = browser.new_context(viewport={'width': width, 'height': 844})
                page = context.new_page()
                page.goto(url, wait_until='load')
                page.wait_for_selector('.w-day')
                page.evaluate('([lang, dark]) => { setLang(lang); setTheme(dark, false); }', [lang, dark])
                page.wait_for_selector('.w-day')
                page.evaluate('document.fonts.ready')
                assert page.locator('#tabSearchLbl').text_content() == label, (width, lang, dark)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, lang, dark, 'overflow')
                assert page.locator('.welcome .tool-btn.primary').is_visible()
                assert page.locator('.w-day').is_visible()
                assert page.locator('.w-foot .foot-link').count() == 0
                assert page.locator('.footer-links #footDataLink').is_visible()
                assert page.evaluate("document.querySelector('.footer-links').nextElementSibling.tagName === 'FOOTER'")
                assert page.evaluate("document.querySelector('footer .credit').textContent.includes('Dhruba Chapain')")
                if width < 761:
                    assert page.locator('.w-foot').is_hidden()
                    assert page.evaluate("document.querySelector('.welcome-stage').getBoundingClientRect().top >= document.querySelector('.welcome-copy').getBoundingClientRect().bottom")
                    assert 'Noto Serif Devanagari' in page.locator('.tab-btn').first.evaluate('e => getComputedStyle(e).fontFamily')
                    page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
                    assert page.evaluate("document.querySelector('footer .credit').getBoundingClientRect().bottom <= document.querySelector('.tabbar').getBoundingClientRect().top"), (width, lang, dark, 'footer obscured')
                else:
                    assert page.locator('.w-foot').is_visible()
                    assert page.locator('.tabbar').is_hidden()
                context.close()
                print(f'PASS {width}px {lang} {"dark" if dark else "light"}')
    # Both principal paths remain usable: entering the book and opening the verse.
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    page = context.new_page()
    page.goto(url, wait_until='load')
    page.wait_for_selector('.w-day')
    page.locator('.w-day').focus()
    page.keyboard.press('Enter')
    assert page.locator('#modalBg').evaluate("e => e.classList.contains('open')")
    assert page.locator('.footer-links').evaluate('e => e.inert')
    page.evaluate('App.reader.close()')
    page.locator('.welcome .tool-btn.primary').click()
    assert page.evaluate("state.view === 'sections'")
    context.close()
    browser.close()
    print('PASS keyboard verse and Enter the Gita')
