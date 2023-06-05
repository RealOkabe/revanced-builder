import glob, json, os, requests
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
        downloadRevancedFile(URL_REVANCED_CLI, latestVersionCli)

    if latestVersionPatches > lastVersionPatches:
        lastVersionPatches = latestVersionPatches
        downloadRevancedFile(URL_REVANCED_PATCHES, latestVersionPatches)

    if latestVersionIntegrations > lastVersionIntegrations:
        lastVersionIntegrations = latestVersionIntegrations
        downloadRevancedFile(URL_REVANCED_INTEGRATIONS, latestVersionIntegrations)

    data = [{
        "vCli": lastVersionCli,
        "vIntegrations": lastVersionIntegrations,
        "vPatches": lastVersionPatches
    }]
    VERSIONS_FILE_HANDLE.seek(0)
    VERSIONS_FILE_HANDLE.truncate()
    json.dump(data, VERSIONS_FILE_HANDLE)


def downloadRevancedFile(downloadUrl, downloadVersion):
    assetsUrl = f"{downloadUrl}/{downloadVersion}/assets"
    fileToRemove = []
    if downloadUrl == URL_REVANCED_CLI:
        fileToRemove = glob.glob("*cli*jar")
    elif downloadUrl == URL_REVANCED_PATCHES:
        fileToRemove = glob.glob("*patches*jar")
    elif downloadUrl == URL_REVANCED_INTEGRATIONS:
        fileToRemove = glob.glob("*integrations*apk")
    
    for i in fileToRemove:
        os.remove(i)
    cliReleases = json.loads(requests.get(assetsUrl).text)
    if downloadUrl == URL_REVANCED_PATCHES:
        currentRelease = cliReleases[1]
    else:
        currentRelease = cliReleases[0]
    browserDownloadUrl = currentRelease['browser_download_url']
    file_name = currentRelease['name']
    response = requests.get(browserDownloadUrl)
    with open(file_name, 'wb') as f:
        f.write(response.content)


checkFileVersions()