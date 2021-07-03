#!/usr/bin/env python3

import configparser
import pathlib
import subprocess
import sys
import fnmatch

fontmeta = configparser.ConfigParser()
with open("fontmeta.ini", "r") as configfile:
    fontmeta.read_file(configfile)

if len(sys.argv) > 1:
    filter_pattern = sys.argv[1]
else:
    filter_pattern = None

for fontname in fontmeta.sections():
    # filter fontname based on pattern argument
    if (filter_pattern is not None) and (not fnmatch.fnmatch(fontname, filter_pattern)):
        continue
    fontpath = pathlib.Path(fontname)
    woffpath = fontpath / "woff"
    woff2path = fontpath / "woff2"
    ttfpath = fontpath / "ttf"
    woffpath.mkdir(exist_ok=True)
    woff2path.mkdir(exist_ok=True)
    for fontfile in ttfpath.glob("*.ttf"):
        wofffile = woffpath / (fontfile.stem + ".woff")
        woff2file = woff2path / (fontfile.stem + ".woff2")
        print("Converting", fontfile.stem, "to woff")
        subprocess.run(
            ["pyftsubset", str(fontfile), "*", "--flavor=woff",
            "--output-file=" + str(wofffile)])
        print("Converting", fontfile.stem, "to woff2")
        subprocess.run(
            ["pyftsubset", str(fontfile), "*", "--flavor=woff2",
            "--output-file=" + str(woff2file)])
