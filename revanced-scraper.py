import json
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://api.github.com/repos/revanced/"
URL_REVANCED_CLI = URL_BASE + "revanced-cli/releases"
URL_REVANCED_PATCHES = URL_BASE + "revanced-patches/releases"
URL_REVANCED_INTEGRATIONS = URL_BASE + "revanced-integrations/releases"
VERSIONS_FILE_PATH = "versions.json"

def checkFileVersions():
    # Get the releases
    cliReleases = json.loads(requests.get(URL_REVANCED_CLI).text)
    patchesReleases = json.loads(requests.get(URL_REVANCED_PATCHES).text)
    integrationsReleases = json.loads(requests.get(URL_REVANCED_INTEGRATIONS).text)

    # Get latest versions from releases
    latestVersionCli = cliReleases[0]['id']
    latestVersionPatches = patchesReleases[0]['id']
    latestVersionIntegrations = integrationsReleases[0]['id']

    # Get last versions from cache
    VERSIONS_FILE = json.loads(open(VERSIONS_FILE_PATH).read())
    lastVersionCli = VERSIONS_FILE[0]['vCli']
    lastVersionPatches = VERSIONS_FILE[0]['vPatches']
    lastVersionIntegrations = VERSIONS_FILE[0]['vIntegrations']

    if latestVersionCli > lastVersionCli:
        updateFiles(URL_REVANCED_CLI)

    if latestVersionPatches > lastVersionPatches:
        updateFiles(URL_REVANCED_PATCHES)
    
    if latestVersionIntegrations > lastVersionIntegrations:
        updateFiles(URL_REVANCED_INTEGRATIONS)

