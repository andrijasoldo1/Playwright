import re
import os
import tempfile
import time
from faker import Faker
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def click_enabled_speichern(page):
    speichern_buttons = page.locator("text=Speichern")
    count = speichern_buttons.count()

    for i in range(count):
        button = speichern_buttons.nth(i)
        if button.is_visible() and "btn-disabled" not in button.get_attribute("class"):
            button.click()
            return
    raise Exception("No enabled 'Speichern' button found.")



def test_run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(os.getenv("BASE_URL"))
    page.get_by_role("row", name="00.01.02 Kanzlei A CHF 1'850").locator("span").first.click()
    with page.expect_popup() as page1_info:
        page.get_by_text("Bewerben").click()
    page1 = page1_info.value
    page1.get_by_text("Start").click()
    page1.get_by_text("Speichern und weiter").click()
    page1.get_by_text("Speichern und weiter").click()
    page1.get_by_role("textbox", name="Bitte auswählen").first.click()
    page1.get_by_text("Einpersonen-Haushalt").click()
    page1.get_by_role("listitem", name="Nein").first.click()
    page1.get_by_role("listitem", name="Nein").nth(1).click()
    page1.get_by_role("textbox", name="Bitte auswählen").nth(1).click()
    page1.get_by_text("Umbau/Sanierung").click()
    page1.get_by_role("listitem", name="Mietkautionskonto").click()
    page1.get_by_role("textbox", name="Bitte auswählen").nth(4).click()
    page1.get_by_text("Instagram").click()
    page1.get_by_text("Speichern und weiter").click()
    page1.get_by_text("Speichern und weiter").click()
    page1.locator("i").nth(3).click()
    click_enabled_speichern(page1)
    page1.locator(".text-cut").first.click()
    page1.get_by_text("Andere").click()
    page1.get_by_role("textbox", name="Bitte präzisieren").first.click()
    page1.get_by_role("textbox", name="Bitte präzisieren").first.fill("hrsz")
    page1.get_by_role("textbox", name="Bitte präzisieren").nth(1).click()
    page1.get_by_role("textbox", name="Bitte präzisieren").nth(1).fill("sjer")
    page1.get_by_role("textbox", name="DD.MM.YYYY").first.click()
    page1.get_by_role("cell", name="1", exact=True).click()
    page1.locator("div:nth-child(7) > .mt-16 > div > .mdt-select > .select-wrapper > .search > .mdt-input > .input-wrapper > .text-cut").click()
    page1.get_by_text("verheiratet").click()
    page1.get_by_role("textbox", name="Suche...").first.click()
    page1.get_by_text("Schweiz", exact=True).click()
    page1.locator("div:nth-child(12) > .mt-16 > div > .mdt-select > .select-wrapper > .search > .mdt-input > .input-wrapper > .text-cut").click()
    page1.get_by_text("Solidarhafter", exact=True).click()
    page1.get_by_role("textbox", name="123 45 67").first.click()
    page1.get_by_role("textbox", name="123 45 67").first.fill("333333333")
    page1.get_by_role("textbox", name="123 45 67").nth(1).click()
    page1.get_by_role("textbox", name="123 45 67").nth(1).fill("")
    page1.locator("input[type=\"email\"]").first.click()
    page1.locator("input[type=\"email\"]").first.fill("mail@mail.com")
    page1.locator("input[type=\"email\"]").nth(1).click()
    page1.locator("input[type=\"email\"]").nth(1).fill("mail@mail.com")
    page1.locator("div:nth-child(13) > .mt-16 > .mdt-input > .input-wrapper > .text-cut").click()
    page1.locator("div:nth-child(13) > .mt-16 > .mdt-input > .input-wrapper > .text-cut").fill("9")
    page1.get_by_role("spinbutton").first.click()
    page1.get_by_role("spinbutton").first.fill("74")
    page1.locator("div:nth-child(15) > .mt-16 > .mdt-input > .input-wrapper > .text-cut").click()
    page1.locator("div:nth-child(15) > .mt-16 > .mdt-input > .input-wrapper > .text-cut").fill("jyf")
    page1.get_by_role("textbox", name="Suche...").nth(1).click()
    page1.get_by_text("Schweiz", exact=True).click()
    page1.get_by_role("textbox", name="DD.MM.YYYY").nth(2).click()
    page1.get_by_role("cell", name="1", exact=True).click()
    page1.get_by_role("listitem", name="Ja").first.click()
    page1.get_by_role("listitem", name="Ja").nth(1).click()
    page1.get_by_role("listitem", name="Ja").nth(2).click()
    page1.get_by_role("listitem", name="Ja").nth(3).click()
    page1.locator("div:nth-child(4) > .radio-field > .mdt-radio-list > .radio-list > li:nth-child(2)").click()
    page1.locator("div:nth-child(6) > .radio-field > .mdt-radio-list > .radio-list > li:nth-child(2)").click()
    page1.locator("div:nth-child(3) > .mt-16 > div > .mdt-select > .select-wrapper > .search > .mdt-input > .input-wrapper > .text-cut").click()
    page1.get_by_text("Arbeitslos").click()
    page1.get_by_role("listitem", name="CreditTrust-Zertifikat").click()
    page1.get_by_role("checkbox", name="Hiermit bestätige ich, dass").check()
    click_enabled_speichern(page1)

    page1.locator("div:nth-child(9) > .mt-16 > .mdt-input > .input-wrapper > .text-cut").click()
    page1.locator("div:nth-child(9) > .mt-16 > .mdt-input > .input-wrapper > .text-cut").fill("htybcgrd")
    page1.get_by_text("Speichern", exact=True).click()
    
    
    
    page1.locator("div.btn-next", has_text="Speichern und weiter").click()





    


    
    page1.get_by_text("Zieht der Mietinteressent").click()
    click_enabled_speichern(page1)


    page1.get_by_text("Ich bestätige, alle Fragen").click()
    page1.get_by_text("Speichern").click()



    page1.get_by_text("Ich habe die Datenschutzerklä").click()
    page1.get_by_text("Speichern").click()
    click_enabled_speichern(page1)


    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_run(playwright)