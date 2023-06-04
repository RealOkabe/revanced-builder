import json
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://api.github.com/repos/revanced/"
URL_REVANCED_CLI = URL_BASE + "revanced-cli/releases"
URL_REVANCED_PATCHES = URL_BASE + "revanced-patches/releases"
URL_REVANCED_INTEGRATIONS = URL_BASE + "revanced-integrations/releases"
VERSIONS_FILE_HANDLE = open("versions.json", "r+")


def checkFileVersions():
    # Get the releases
    cliReleases = json.loads(requests.get(URL_REVANCED_CLI).text)
    patchesReleases = json.loads(requests.get(URL_REVANCED_PATCHES).text)
    integrationsReleases = json.loads(requests.get(URL_REVANCED_INTEGRATIONS).text)

    # Get latest versions from releases
    latestVersionCli = cliReleases[0]['id']
    print("Latest Version CLI {}".format(latestVersionCli))
    latestVersionPatches = patchesReleases[0]['id']
    print("Latest Version Patches {}".format(latestVersionPatches))
    latestVersionIntegrations = integrationsReleases[0]['id']
    print("Latest Version Integrations {}".format(latestVersionIntegrations))

    # Get last versions from cache
    VERSIONS_FILE = json.loads(VERSIONS_FILE_HANDLE.read())
    lastVersionCli = int(VERSIONS_FILE[0]['vCli'])
    lastVersionPatches = int(VERSIONS_FILE[0]['vPatches'])
    lastVersionIntegrations = int(VERSIONS_FILE[0]['vIntegrations'])

    if latestVersionCli > lastVersionCli:
        lastVersionCli = latestVersionCli

    if latestVersionPatches > lastVersionPatches:
        lastVersionPatches = latestVersionPatches

    if latestVersionIntegrations > lastVersionIntegrations:
        lastVersionIntegrations = latestVersionIntegrations

    data = [{
        "vCli": lastVersionCli,
        "vIntegrations": lastVersionIntegrations,
        "vPatches": lastVersionPatches
    }]
    VERSIONS_FILE_HANDLE.seek(0)
    VERSIONS_FILE_HANDLE.truncate()
    json.dump(data, VERSIONS_FILE_HANDLE)

checkFileVersions()