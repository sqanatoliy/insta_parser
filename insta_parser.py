"""
To install Playwright, execute these three commands in sequence:
pip install --upgrade pip
pip install playwright
playwright install
"""
import csv
import re

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to instagram
    page.goto("https://www.instagram.com/")

    # Fill with username
    page.get_by_label("Phone number, username, or email").click()
    page.get_by_label("Phone number, username, or email").fill("example@gmail.com")

    # Fill with password
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("MyVeryStrongPassword")

    # Click Log In
    page.get_by_role("button", name="Log in", exact=True).click()
    page.wait_for_url("https://www.instagram.com/accounts/onetap/?next=%2F")

    page.goto("https://www.instagram.com/")

    # Click text=Not Now
    page.get_by_role("button", name="Not Now").click()
    page.wait_for_url("https://www.instagram.com/")

    # put the link of the profile from which you want to get followers
    link_to_profile_followers = "https://www.instagram.com/put_here_account_id/followers/"
    page.goto(link_to_profile_followers)

    followers = page.locator('div._aano > div > div > div > div > div >div > div:nth-child(2) > div')
    follower_link = 'div._aano > div > div > div > div > div >div > div:nth-child(2) > div > div > div > div > div > a'
    follower_name = "div._aano > div > div > div > div > div >div > div:nth-child(2) > div > div > span > span"

    # Use the while loop where you compare the number of profiles in the DOM
    # with the number of followers indicated in the profile header

    followers_on_page = int(page.locator("li:nth-child(2) > a > span > span").text_content().replace(",", ""))
    if followers_on_page % 12 == 0:
        number_iteration = followers_on_page // 12 - 1
    else:
        number_iteration = followers_on_page // 12
    print(number_iteration)
    base_url = "https://www.instagram.com"
    for _ in range(number_iteration):
        print("iter ", _)
        followers.last.scroll_into_view_if_needed()
        page.wait_for_timeout(3*1000)

    user_info = {}
    for i in range(followers.count()):
        lnk = (base_url + page.locator(follower_link).nth(i).get_attribute("href"))
        name = page.locator(follower_name).nth(i).text_content()
        user_info[name] = lnk

    regex_pattern = r"https://www.instagram.com/([^/]+)/followers/"
    desired_part = ""
    match = re.match(regex_pattern, link_to_profile_followers)
    if match:
        desired_part = match.group(1)

    file_name = f"List of followers for {desired_part}.csv"

    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['Ім`я', 'Посилання на профіль']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in user_info.items():
            writer.writerow({'Ім`я': key, 'Посилання на профіль': value})

    print(user_info)
    page.close()


if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)
