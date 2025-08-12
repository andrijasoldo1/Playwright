import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://mostar.demo.melon.market/form/application/new/1ddf2594f820438da52a921dd2f5725d/6th-1bd928a4f8fc0b0bf546/67c10f4b-9986-4f94-a90e-4cc6c5e83f6d")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
