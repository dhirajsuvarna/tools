from playwright.sync_api import sync_playwright 

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto("https://m.myhcl.com/WFH/DigitalAct.aspx")
    print(page.title())
    browser.close()