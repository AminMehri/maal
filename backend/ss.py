import requests
from pprint import pprint
username = input("enter username:\n")
r = requests.get(f"https://new-api.coco.gl/dashboard/ads/info?instagramId={username}")
pprint(r.json())

