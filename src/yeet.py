# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re
import io

data = []
from pathlib import Path


pathlist = Path("../hyfetch/hyfetch/distros").glob("**/*.py")
for path in pathlist:
    print(path)
    regex = re.compile(
        r"match=.*?['\"](?P<name>.+)['\"].*color='(?P<colors>.*)'.*?r\"{3}(?P<ascii>.*)\"{3}",
        re.MULTILINE | re.DOTALL,
    )

    test_str = io.open(path, mode="r", encoding="utf-8").read()

    match = regex.search(test_str)
    if match is not None:
        name = [
            x.strip()
            for x in match.group("name")
            .replace("'", "")
            .replace('"', "")
            .replace("*", "")
            .split("|")
        ]
        colors = []
        for k in match.group("colors").split():
            if k == "fg":
                colors += ["    - Reset"]
            # elif k == "bg":
            #     colors += [{"Bg": None}]
            elif len(k) == 9 or len(k) == 7:
                k = k.strip('"')
                colors += [
                    f"""    - !Rgb
      r: {int(k[1:3],16)}
      g: {int(k[3:5],16)}
      b: {int(k[5:7],16)}
"""
                ]
            else:
                colors += [f"    - !AnsiValue {int(k)}"]

        art = match.group("ascii").strip().split("\n")
        width = max([len(re.sub(r"\$\{c.*?\}", "", line.rstrip())) for line in art])
        art = "\n".join(["    " + x.replace(":", ";").ljust(width) for x in art])
        data += [
            f"""- name: {name}
  width: {width}
  colors:
{'\n'.join(colors)}
  art: |
{art}
"""
        ]

    else:
        print(path)
# TODO: make sure this uses multi line strings, and formats colors correctly
with open("../data/icons.yaml", "r+", encoding="utf-8") as f:
    f.write("\n".join(data))
