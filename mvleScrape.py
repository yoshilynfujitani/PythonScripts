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

    course_id_elements = soup.find_all(attrs={"data-course-id": True})
    course_ids = set([element['data-course-id']
                     for element in course_id_elements])

    for course_id in course_ids:
        page.goto("https://mvle4.mmsu.edu.ph/course/view.php?id="+course_id)
        print("been to " + course_id)

        page.is_visible("div#page-content")

        topics = page.inner_html("ul.topics")
        inSoup = BeautifulSoup(topics, "html.parser")

        head = page.inner_html("header#page-header")
        headSoup = BeautifulSoup(head, "html.parser")

        course_code = headSoup.find("h1", {"class": "h2"})
        course_titles = inSoup.find_all(
            "h3", {"data-for": "section_title"})
        course_desc = inSoup.find_all("div", {"class": "activity-item"})

        # Open a text file in write mode ('w')
        with open('output.txt', 'a') as file:
            file.write(course_code.text)
            for x in range(len(course_titles)):
                # Remove leading and trailing whitespace
                title = course_titles[x].text.strip()
                file.write(title + '\n')

                if x < len(course_desc) and course_desc[x] is not None:
                    # Remove leading and trailing whitespace
                    description = course_desc[x].text.strip()
                    # Replace multiple spaces and newlines with a single space
                    description = ' '.join(description.split())
                    file.write(description + '\n')
                    file.write("\n")
                else:
                    file.write("Section does not have a course description\n")
