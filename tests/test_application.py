import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

def test_page_load(browser):
    """Testira da li se stranica pravilno učitava"""
    page = browser.new_page()
    page.goto("https://mostar.demo.melon.market/form/application/new?uuids=e34bfbd2-218e-4f36-9e92-e2ae9367fcfc,db50b164-beec-4379-a025-6f5d57aab822,c4e795a5-05dd-4e5f-b073-518321751d6b&lang=en")

    assert "melon" in page.title()  
    page.wait_for_selector("body")  

    page.close()

def test_click_start_application(browser):
    """Klik na dugme 'Start' i provjera da li se stranica mijenja"""
    page = browser.new_page()
    page.goto("https://mostar.demo.melon.market/form/application/new?uuids=e34bfbd2-218e-4f36-9e92-e2ae9367fcfc,db50b164-beec-4379-a025-6f5d57aab822,c4e795a5-05dd-4e5f-b073-518321751d6b&lang=en")

    page.wait_for_selector("#start-application-btn")
    page.click("#start-application-btn")

    page.wait_for_timeout(3000)  
    assert "application" in page.url  

    page.close()

def test_check_links_and_images(browser):
    """Provjera da li postoje slike, linkovi i da su ispravni"""
    page = browser.new_page()
    page.goto("https://mostar.demo.melon.market/form/application/new?uuids=e34bfbd2-218e-4f36-9e92-e2ae9367fcfc,db50b164-beec-4379-a025-6f5d57aab822,c4e795a5-05dd-4e5f-b073-518321751d6b&lang=en")

    page.wait_for_selector("img.logo", timeout=10000)
    logo = page.locator("img.logo")
    logo.scroll_into_view_if_needed()  
    assert logo.is_visible(), "Logo nije vidljiv!"

    page.wait_for_selector("a", timeout=10000)  
    emonitor_link = page.locator("a", has_text="emonitor")
    assert emonitor_link.count() > 0, "Link ka www.emonitor.ch ne postoji!"
    assert emonitor_link.first.is_visible(), "Link ka www.emonitor.ch nije vidljiv!"

    email_link = page.locator("a", has_text="support@emonitor.ch")
    assert email_link.count() > 0, "Email link ne postoji!"
    assert email_link.first.is_visible(), "Email link nije vidljiv!"

    page.close()

def test_privacy_policy_visibility(browser):
    """Provjera da li postoji link za politiku privatnosti"""
    page = browser.new_page()
    page.goto("https://mostar.demo.melon.market/form/application/new?uuids=e34bfbd2-218e-4f36-9e92-e2ae9367fcfc,db50b164-beec-4379-a025-6f5d57aab822,c4e795a5-05dd-4e5f-b073-518321751d6b&lang=en")

    page.wait_for_selector("div.privacy-policy", timeout=10000)
    privacy_policy = page.locator("div.privacy-policy")
    privacy_policy.scroll_into_view_if_needed()  
    assert privacy_policy.is_visible(), "Sekcija politike privatnosti nije vidljiva!"

    page.close()
