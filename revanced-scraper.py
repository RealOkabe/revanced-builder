import json
import requests
from bs4 import BeautifulSoup

URL_GITHUB_API = "https://api.github.com/repos/"
URL_REVANCED_CLI = URL_GITHUB_API + "revanced/revanced-cli/releases"

jsonData = json.loads(requests.get(URL_REVANCED_CLI).text)
for i in jsonData:
    print(i['name'])