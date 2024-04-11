import copy
import json
import os
import re
from asnake.client import ASnakeClient
import datetime


def setup():
    reponum = input("Please enter repository number: ")
    file = input("Please enter your connection file name: ")
    if file == "" or file == "\n":
        file = "ArchivesSpaceConnection.txt"
    resourcenum = input("Please Enter Resource Number, or enter for all: ")
    if resourcenum == "" or resourcenum == "\n":
        resourcenum = 0
    global logFile
    logFile = input("Please enter a CSV filename for log output: ")
    if not os.path.isfile(logFile):
        if not os.path.exists(logFile):
            log = open(logFile, "a+")
            log.write("Date/Time,URI,Previous Value, Updated Value, Status")
            log.close()
        else:
            print(
                f"Cannot write to {logFile}: Is a directory. ArchivesSpace has not been modified"
            )
            return
    else:
        print("Warning: Logfile already exists, log output will be appended")
    session = create_session(file=str(file))
    strip_tags(session, reponum, resourcenum)


def log(uri, previousvalues, updatedvalues, result):
    file = open(logFile, "a+")
    file.write(
        f"\n{datetime.datetime.now()},{uri},{previousvalues},{updatedvalues},{'Success' if result == 200 else result}"
    )
    file.close()


def create_session(file="ArchivesSpaceConnection.txt"):
    file = open(file)
    endpoint = file.readline().strip()
    user = file.readline().strip()
    pw = file.readline().strip()
    client = ASnakeClient(baseurl=endpoint, username=user, password=pw)
    client.authorize()
    return client


def strip_tags(session, reponum, resourcenum):
    maxpage = 1
    page = 1
    while page <= maxpage:
        page += 1
        result = session.get(
            f"repositories/{reponum}/digital_objects", params={"page": page}
        ).json()
        maxpage = result["last_page"]
        for result in result["results"]:
            if (
                resourcenum == 0
                or {"ref": f"/repositories/{reponum}/resources/{resourcenum}"}
                in result["collection"]
            ):
                process_digital_object(session, result)


def process_digital_object(session, result: json):
    edited = copy.deepcopy(result)
    wasChanged = False
    for versionnum in range(len(result["file_versions"])):
        preservicalink = re.findall(
            '<a href="(https://uorrcl.access.preservica.com/.+?/)">',
            result["file_versions"][versionnum]["file_uri"],
        )
        if preservicalink:
            edited["file_versions"][versionnum]["file_uri"] = preservicalink[0]
            wasChanged = True

    if wasChanged:
        request = session.post(f"{result['uri']}", json=edited)
        log(
            result["uri"],
            result["file_versions"][1]["file_uri"],
            edited["file_versions"][1]["file_uri"],
            request.json()["status"],
        )


setup()
