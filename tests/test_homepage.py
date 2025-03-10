import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

def test_page_load(browser):
    page = browser.new_page()
    page.goto("https://mostar.api.demo.ch.melon.market/")

    assert "Demo" in page.title()
    page.wait_for_selector("body")

    page.close()

def test_check_text(browser):
    page = browser.new_page()
    page.goto("https://mostar.api.demo.ch.melon.market/")

    assert "Mostar" in page.locator("body").inner_text()

    page.close()

def test_check_images(browser):
    page = browser.new_page()
    page.goto("https://mostar.api.demo.ch.melon.market/")

    images = page.locator("img")
    assert images.count() > 0, "Nema slika na stranici!"

    page.close()

def test_navigation(browser):
    page = browser.new_page()
    page.goto("https://mostar.api.demo.ch.melon.market/")

    link = page.locator("a[href='#wohnen']").nth(0)
    if link.count() > 0:
        link.click()
        page.wait_for_timeout(2000)  
        assert "#wohnen" in page.url or page.locator("#wohnen").is_visible()
    else:
        pytest.skip("Navigacijski link #wohnen ne postoji.")

    page.close()



def test_buttons_exist(browser):
    page = browser.new_page()
    page.goto("https://mostar.api.demo.ch.melon.market/")

    buttons = page.locator("button")
    assert buttons.count() > 0, "Nema dugmadi na stranici!"

    page.close()
