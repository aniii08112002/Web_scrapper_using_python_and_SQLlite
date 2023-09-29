import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")

HEADERS = {
    # Define your headers here
}

def scrap(url):
    """Scrap The Page from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    password = "igvw vlqg rldr yvuf"
    username = 'anirudhloveshismotheralot@gmail.com'
    receiver = 'anirudhsharmakr76@gmail.com'

    with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) as file:
        file.login(username, password)
        file.sendmail(username, receiver, message)
    print("Email was sent")

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == "__main__":
    while True:
        scraped = scrap(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)

            if not row:
                store(extracted)
                send_email(message="Hey, new Event found")

        # Uncomment the line below to add a delay between iterations
        # time.sleep(2)
