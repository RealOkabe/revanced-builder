import json
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://api.github.com/repos/revanced/"
URL_REVANCED_CLI = URL_BASE + "revanced-cli/releases"
URL_REVANCED_PATCHES = URL_BASE + "revanced-patches/releases"
URL_REVANCED_INTEGRATIONS = URL_BASE + "revanced-integrations/releases"

cliReleases = json.loads(requests.get(URL_REVANCED_CLI).text)
patchesReleases = json.loads(requests.get(URL_REVANCED_PATCHES).text)
integrationsReleases = json.loads(requests.get(URL_REVANCED_INTEGRATIONS).text)
