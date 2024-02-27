from bs4 import BeautifulSoup
import csv
import requests


def run(**kwargs):
    # html = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml').text
    # html = requests.get('https://docs.google.com/spreadsheets/d/1G7gOXj8VDbl2Ns_UfYn0PxF8aNp2ZVHH3oChIaICyaM/edit#gid=0').text
    html = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vRjLopXtqOeWP7LULsZp7Z1jK-NbWrpt4SqCikP0_C3rb3L4Z3tqNeFiVkVriLwTIdrZVlJ-AqP6j9g/pubhtml').text
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    index = 0
    for table in tables:
        with open(str(index) + ".csv", "w") as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerows([[td.text for td in row.find_all("td")] for row in table.find_all("tr")])
