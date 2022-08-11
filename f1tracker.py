import asyncio
from bs4 import BeautifulSoup
from pyppeteer import launch
import smtplib
from time import sleep

changes = []


def mail(changes):
    port = 587
    server = smtplib.SMTP("smtp.gmail.com", port) # currently set to gmail / can be changed how you want
    server.starttls()
    server.login("email_that_sends_mail@test.com", "password_to_said_email")
    sender_email = "" # email of sender
    receiver_email = ""  # email of reciever
    message = """
        Subject: F1 Tracker Update

        The following changes occured:

        """
    for j in changes:
        message += j

    server.sendmail(sender_email, receiver_email, message)
    print("Mail sent")


async def crawl():
    global changes
    list = []
    browser = await launch()
    page = await browser.newPage()
    url = "https://www.f1fantasytracker.com/prices.html"

    await page.goto(url)
    content = await page.content()

    soup = BeautifulSoup(content, features="lxml")
    for i in range(1, 31):

        participant = soup.find(id=f"WeekName{i}").get_text()
        change = soup.find(id=f"WeekChange{i}").get_text()
        if change != "+0.0":
            c = f"{participant}, Change: ${change}m\n"
            list.append(c)
            print(c)

    if list != changes:
        changes = list
        mail(changes)

    await browser.close()


def main():
    while True:
        asyncio.get_event_loop().run_until_complete(crawl())
        sleep(3600)


if __name__ == "__main__":
    main()
