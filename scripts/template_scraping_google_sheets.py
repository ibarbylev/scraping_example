from bs4 import BeautifulSoup
import csv
import requests

html = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vRjLopXtqOeWP7LULsZp7Z1jK-NbWrpt4SqCikP0_C3rb3L4Z3tqNeFiVkVriLwTIdrZVlJ-AqP6j9g/pubhtml').text
soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table")
index = 0

data = []
for table in tables:
    with open(str(index) + ".csv", "w") as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        data.append([[td.text for td in row.find_all("td")] for row in table.find_all("tr")])
        wr.writerows(data)

data = data[0][1:]
print(data)

# extract only first column
urls = [d[0] for d in data]
print(urls)

