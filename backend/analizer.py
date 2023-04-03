import requests
from bs4 import BeautifulSoup
username = input("enter username:\n")
r = requests.get(f"https://analisa.io/profile/{username}")
soup = BeautifulSoup(r.text)
tag = soup.find("meta", {"name":"description"})
print(tag["content"])
