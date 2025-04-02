import os
from faker import Faker
from dotenv import load_dotenv
from playwright.sync_api import Playwright

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def add_adult(page):
    fake = Faker()
    email = fake.unique.email()

    page.get_by_text("Erwachsene Person hinzufügen").click()
    page.locator(".text-cut").first.click()
    page.get_by_text("Herr").click()
    page.get_by_role("textbox", name="Bitte präzisieren").first.fill("Ivo")
    page.get_by_role("textbox", name="Bitte präzisieren").nth(1).fill("Ivic")
    page.get_by_role("textbox", name="DD.MM.YYYY").first.click()
    page.get_by_role("cell", name="1", exact=True).click()
    page.locator("div:nth-child(7) .text-cut").click()
    page.get_by_text("verheiratet").click()
    page.get_by_role("textbox", name="Suche...").first.click()
    page.get_by_text("Schweiz", exact=True).click()
    page.locator("div:nth-child(9) .text-cut").fill("Bla")
    page.locator("div:nth-child(12) .text-cut").click()
    page.get_by_text("Solidarhafter", exact=True).click()
    page.get_by_role("textbox", name="123 45 67").first.fill("333333333")
    page.locator("input[type=\"email\"]").first.fill(email)
    page.locator("input[type=\"email\"]").nth(1).fill(email)
    page.locator("div:nth-child(13) .text-cut").fill("efs")
    page.get_by_role("spinbutton").first.fill("3")
    page.locator("div:nth-child(15) .text-cut").fill("gwawag")
    page.get_by_role("textbox", name="Suche...").nth(1).click()
    page.get_by_text("Schweiz", exact=True).click()
    page.get_by_role("textbox", name="DD.MM.YYYY").nth(2).click()
    page.get_by_role("cell", name="1", exact=True).click()
    page.locator("div:nth-child(3) > .mt-16 > div > .mdt-select > .select-wrapper > .search > .mdt-input > .input-wrapper > .text-cut").click()
    page.get_by_text("Arbeitslos").click()
    page.get_by_role("listitem", name="CreditTrust-Zertifikat").click()
    page.get_by_role("checkbox", name="Hiermit bestätige ich, dass").check()
    page.get_by_text("Speichern", exact=True).click()


def test_run(playwright: Playwright, add_adults_fixture):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL)

    page.get_by_role("row", name="00.01.02 Kanzlei A CHF 1'850").locator("span").first.click()
    with page.expect_popup() as popup_info:
        page.get_by_text("Bewerben").click()
    page1 = popup_info.value

    page1.get_by_text("Start").click()
    page1.get_by_text("Speichern und weiter").click()
    page1.get_by_role("textbox", name="Bitte auswählen").first.click()
    page1.get_by_text("Einpersonen-Haushalt").click()
    page1.get_by_role("listitem", name="Nein").first.click()
    page1.get_by_role("listitem", name="Nein").nth(1).click()
    page1.get_by_role("listitem", name="Nein").nth(2).click()
    page1.get_by_role("textbox", name="Bitte auswählen").nth(1).click()
    page1.get_by_text("Lärm / Immissionen").click()
    page1.locator("div:nth-child(2) > .text-cut").first.click()
    page1.get_by_role("listitem", name="Mietkautionskonto").click()
    page1.get_by_role("listitem", name="Nein").nth(3).click()
    page1.get_by_role("textbox", name="Bitte auswählen").nth(4).click()
    page1.get_by_text("Onlinewerbung").click()
    page1.get_by_text("Speichern und weiter").click()

    add_adults_fixture(page1)

    page1.wait_for_timeout(1000)
    page1.get_by_text("Speichern und weiter", exact=True).wait_for(state="visible", timeout=1000)
    page1.get_by_text("Speichern und weiter", exact=True).click()

    page1.get_by_role("checkbox", name="Zieht der Mietinteressent").check()
    page1.get_by_role("checkbox", name="Ich bestätige, alle Fragen").check()
    page1.get_by_role("checkbox", name="Ich habe die Datenschutzerklä").check()
    page1.get_by_text("Speichern").click()
