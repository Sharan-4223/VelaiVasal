"""Phone-sized (390x780) viewport screenshots used in the pitch deck."""
from playwright.sync_api import sync_playwright
URL, OUT = "http://127.0.0.1:8000/", "/tmp/w/"
TA = ("என்னுடைய மிகப்பெரிய பலம் குழுவாக வேலை செய்வது. எடுத்துக்காட்டாக, கல்லூரி திட்டத்தில் நான் கடின உழைப்புடன் "
      "ஒரு பிரச்சனையைத் தீர்த்தேன். அதனால் எங்கள் குழு நேரத்தில் வேலையை முடித்தது.")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 780}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_selector("[data-testid=roles]")
    for sid, lvl in [("excel", 3), ("sql", 0), ("stats", 1), ("viz", 1), ("comm", 2)]:
        pg.click(f"[data-testid=rate-{sid}-{lvl}]")
    pg.click("[data-testid=build]"); pg.wait_for_selector("[data-testid=path]")
    pg.evaluate("document.querySelectorAll('main > section > .card')[0].style.display='none'")
    pg.evaluate("document.querySelector('main h2').style.display='none'; document.querySelector('.roles').style.display='none'")
    pg.wait_for_timeout(300); pg.screenshot(path=OUT + "ph1.png")

    pg.reload(); pg.wait_for_selector("[data-testid=roles]")
    pg.click("[data-testid=tab-interview]"); pg.wait_for_selector("[data-testid=question]")
    pg.locator("[data-testid=qtabs] button").nth(2).click()
    pg.click("[data-testid=sample]"); pg.click("[data-testid=score]"); pg.wait_for_selector("[data-testid=result]")
    pg.evaluate("document.querySelector('.roles').style.display='none'; document.querySelector('main h2').style.display='none'; document.querySelector('[data-testid=qtabs]').style.display='none'")
    pg.evaluate("document.querySelector('textarea').rows=3")
    pg.wait_for_timeout(300); pg.screenshot(path=OUT + "ph2.png")

    pg.click("[data-testid=lang-ta]"); pg.wait_for_timeout(600)
    pg.reload(); pg.click("[data-testid=lang-ta]"); pg.click("[data-testid=tab-interview]"); pg.wait_for_selector("[data-testid=question]")
    pg.locator("[data-testid=qtabs] button").nth(1).click()
    pg.fill("[data-testid=answer]", TA); pg.click("[data-testid=score]"); pg.wait_for_selector("[data-testid=result]")
    pg.evaluate("document.querySelector('.roles').style.display='none'; document.querySelector('main h2').style.display='none'; document.querySelector('[data-testid=qtabs]').style.display='none'")
    pg.evaluate("document.querySelector('textarea').rows=3")
    pg.wait_for_timeout(300); pg.screenshot(path=OUT + "ph3.png")
    b.close()
