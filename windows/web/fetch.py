import requests
from bs4 import BeautifulSoup

def getVegFamily(vegname):
    req = requests.get(rf"https://en.wikipedia.org/wiki/{vegname}")
    soup = BeautifulSoup(req.text)
    tds = soup.find_all("td")
    for i, table in enumerate(tds):
        if str(table.contents[0]).rstrip() == "Family:":
            j = i + 1
            break
    family = tds[j].find('a', href=True).contents[0]

    return family

if __name__ == "__main__":
    # Quick test to check it gets the correct families
    print(getVegFamily("tomato"))
    print(getVegFamily("potato"))
    print(getVegFamily("carrot"))
    print(getVegFamily("celery"))

    while True:
        userinput = input("Input a vegetable: ")
        try:
            print(getVegFamily(str(userinput)))
        except:
            print("No Family Found")