from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto("https://mvle4.mmsu.edu.ph/login/index.php")
    page.fill("input#username", "21-020385")
    page.fill("input#password", "PASSWORD")
    page.click("button[type=submit]")
    page.is_visible("div#page-wrapper")

    page.click("li[data-key=mycourses]")
    page.is_visible("div#page-wrapper")

    cards = page.inner_html("div[data-region=card-deck]")
    soup = BeautifulSoup(cards, "html.parser")
    courses = soup.find_all("span", {"class": "multiline"})

    for course in courses:
        print(course.text)
