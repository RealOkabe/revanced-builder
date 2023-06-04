import json
import requests
import os
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
    latestVersionPatches = patchesReleases[0]['id']
    latestVersionIntegrations = integrationsReleases[0]['id']

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


def downloadCliVersion():
    cliReleases = json.loads(requests.get(URL_REVANCED_CLI).text)
    browser_download = cliReleases[0]['assets'][0]['browser_download_url']
    file_name = cliReleases[0]['assets'][0]['name']
    response = requests.get(browser_download)
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    jar_file = [file for file in files if file.endswith(".jar")]
    if jar_file:
        os.remove(jar_file[0])
    with open(file_name, 'wb') as f:
        f.write(response.content)


checkFileVersions()
downloadCliVersion()
