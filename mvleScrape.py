from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto("https://mvle4.mmsu.edu.ph/login/index.php")
    page.fill("input#username", "21-020385")
    page.fill("input#password", "EEN9N5")
    page.click("button[type=submit]")
    page.is_visible("div#page-wrapper")

    page.click("li[data-key=mycourses]")
    page.is_visible("div#page-wrapper")

    cards = page.inner_html("div[data-region=card-deck]")
    soup = BeautifulSoup(cards, "html.parser")

    course_id_elements = soup.find_all(attrs={"data-course-id": True})
    course_ids = set([element['data-course-id']
                     for element in course_id_elements])

    for course_id in course_ids:
        page.goto("https://mvle4.mmsu.edu.ph/course/view.php?id="+course_id)
        print("been to " + course_id)

        page.is_visible("div#page-content")

        topics = page.inner_html("ul.topics")
        inSoup = BeautifulSoup(topics, "html.parser")

        course_titles = inSoup.find_all(
            "h3", {"data-for": "section_title"})

        for course_title in course_titles:
            print(course_title.text)
