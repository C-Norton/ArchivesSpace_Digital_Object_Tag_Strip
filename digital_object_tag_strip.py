import copy
import datetime
import json
import os
import re

from asnake.client import ASnakeClient


def setup():
    repo = input("Please enter repository number: ")
    file = input("Please enter your connection file name: ")
    if file == "" or file == "\n":
        file = "ArchivesSpaceConnection.txt"
    resource = input("Please Enter Resource Number, or enter for all: ")
    if resource == "" or resource == "\n":
        resource = 0
    global log_file_name
    log_file_name = input("Please enter a CSV filename for log output: ")
    if not os.path.isfile(log_file_name):
        if not os.path.exists(log_file_name):
            log_file = open(log_file_name, "a+")
            log_file.write(
                "Date/Time,URI,Previous Value, Updated Value, Status")
            log_file.close()
        else:
            print(
                f"Cannot write to {log_file_name}:"
                f"Is a directory. ArchivesSpace has not been modified")
            return
    else:
        print("Warning: Logfile already exists, log output will be appended")
    session = create_session(file=str(file))
    strip_tags(session, repo, resource)


def log(uri, previous, updated, result):
    file = open(log_file_name, "a+")
    file.write(f"\n{datetime.datetime.now()},{uri},{previous},{updated}"
               f",{'Success' if result == 200 else result}")
    file.close()


def create_session(file="ArchivesSpaceConnection.txt"):
    file = open(file)
    endpoint = file.readline().strip()
    user = file.readline().strip()
    pw = file.readline().strip()
    client = ASnakeClient(baseurl=endpoint, username=user, password=pw)
    client.authorize()
    return client


def strip_tags(session, repo, resource):
    max_page = 1
    page = 1
    while page <= max_page:
        page += 1
        result = session.get(f"repositories/{repo}/digital_objects",
                             params={"page": page}).json()
        max_page = result["last_page"]
        for result in result["results"]:
            uri = f"/repositories/{repo}/resources/{resource}"
            if resource == 0 or {"ref": uri} in result["collection"]:
                process_digital_object(session, result)


def process_digital_object(session, result: json):
    edited = copy.deepcopy(result)
    changed = False
    for version in range(len(result["file_versions"])):
        preservica_link = re.findall(
            '<a href="(https://uorrcl.access.preservica.com/.+?/)">',
            result["file_versions"][version]["file_uri"], )
        if preservica_link:
            edited["file_versions"][version]["file_uri"] = preservica_link[0]
            changed = True

    if changed:
        request = session.post(f"{result['uri']}", json=edited)
        log(result["uri"], result["file_versions"][1]["file_uri"],
            edited["file_versions"][1]["file_uri"], request.json()["status"], )


setup()
