#!/usr/bin/env python3
import os
import subprocess

for root, dirs, files in os.walk("./data/test/"):
    if len(dirs) > 0:
        continue

    print(root)
    print(files[:10])

    rootId = root.split("/")[-1]
    for file in files:
        src = root + "/" + file
        dest = root + "/../" + rootId + "-" + file
        print(src, "->", dest)
        subprocess.run(["mv", src, dest])
