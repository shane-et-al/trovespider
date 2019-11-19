import os
import argparse
import json
import requests
import time
import random

# Make directories if they don't exists
def makedirs(dirs):
    path = "/".join(dirs)
    if not os.path.exists("./download/"+path):
        os.makedirs("./download/"+path)

parser = argparse.ArgumentParser(description='Download all docs in Trove path')
parser.add_argument('path', metavar='P', type=str, nargs='+',
                    help='Trove path element')

args = parser.parse_args()
if args.path[0] != "Home":
    args.path = ["Home"]+args.path

with open("trove.json") as trovefile:
    docs = json.load(trovefile)

for doc in docs:
    if len(args.path) > len(doc["path"]) or args.path != doc["path"][:len(args.path)]:
        continue
    makedirs(doc["path"])
    filepath = "download/"+"/".join(doc["path"])+"/"+doc["title"]
    if os.path.exists(filepath):
        print("File '",filepath,"' already exists. Skipping.")
        continue
    print("Downloading:",doc["path"],doc["title"])
    req = requests.get(doc["url"])
    file = open(filepath, 'wb')
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()
    time.sleep(round(random.uniform(0.5, 2.5), 2))
    
