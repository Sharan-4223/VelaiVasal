"""Drives the compiled app in headless Chromium and saves screenshots."""
import sys
from playwright.sync_api import sync_playwright

URL, OUT = "http://127.0.0.1:8000/", "screenshots/"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 430, "height": 900}, device_scale_factor=2)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(URL); pg.wait_for_selector("[data-testid=roles]")
    pg.screenshot(path=OUT + "01_home_skill_check.png")

    for sid, lvl in [("excel", 3), ("sql", 0), ("stats", 1), ("viz", 1), ("comm", 2)]:
        pg.click(f"[data-testid=rate-{sid}-{lvl}]")
    pg.click("[data-testid=build]"); pg.wait_for_selector("[data-testid=path]")
    pg.locator("[data-testid=path]").scroll_into_view_if_needed()
    pg.screenshot(path=OUT + "02_skill_path.png", full_page=True)
    assert "SQL" in pg.inner_text("[data-testid=path]")

    pg.click("[data-testid=tab-interview]"); pg.wait_for_selector("[data-testid=question]")
    for i in range(3):  # a few attempts so the progress chart has data
        pg.locator("[data-testid=qtabs] button").nth(i).click()
        pg.click("[data-testid=sample]"); pg.click("[data-testid=score]")
        pg.wait_for_selector("[data-testid=result]")
    pg.screenshot(path=OUT + "03_mock_interview_feedback.png", full_page=True)
    assert pg.locator("[data-testid=result]").inner_text().strip()

    pg.click("[data-testid=lang-ta]"); pg.wait_for_timeout(600)
    pg.locator("[data-testid=qtabs] button").nth(0).click()
    pg.screenshot(path=OUT + "04_tamil_interview.png", full_page=True)
    pg.click("[data-testid=tab-path]"); pg.click("[data-testid=lang-hi]"); pg.wait_for_timeout(600)
    pg.screenshot(path=OUT + "05_hindi_skill_path.png", full_page=True)

    d = b.new_page(viewport={"width": 1100, "height": 900})
    d.goto(URL); d.wait_for_selector("[data-testid=roles]")
    for sid, lvl in [("excel", 3), ("sql", 0), ("stats", 1), ("viz", 1), ("comm", 2)]:
        d.click(f"[data-testid=rate-{sid}-{lvl}]")
    d.click("[data-testid=build]"); d.wait_for_selector("[data-testid=path]")
    d.screenshot(path=OUT + "06_desktop_view.png", full_page=True)
    print("console/page errors:", errs or "none")
    b.close()
