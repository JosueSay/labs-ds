#!/usr/bin/env python3
import os
import subprocess
import shutil

# m0-0.0.png
srcDir = "./data/train2"
outDir = "./data/train"

numberToName = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}
for i in range(0, 10):
    subprocess.run(["mkdir", "-p", f"{outDir}/{numberToName[i]}"])

for root, dirs, files in os.walk(srcDir):
    # if len(dirs) > 0:
    #     continue

    print(root)
    print(files[:10])

    rootId = root.split("/")[-1]
    for file in files:
        number = file.split(".")[-2]
        src = f"{root}/{file}"
        dest = f"{outDir}/{numberToName[int(number)]}/{file}"
        print(src, dest)
        shutil.move(src, dest)
    # for file in files:
    #     src = root + "/" + file
    #     dest = root + "/../" + rootId + "-" + file
    #     print(src, "->", dest)
    #     subprocess.run(["mv", src, dest])
