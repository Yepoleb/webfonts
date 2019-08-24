#!/usr/bin/env python3

import string
import configparser
import pathlib

HEADER_TEMPLATE = string.Template(
"""/*
 * $name by $designer - $url
 * License: $license
 */

""")

FONTFACE_TEMPLATE = string.Template(
"""@font-face {
    font-family: '$name';
    font-style: $style;
    font-weight: $weight;
    font-display: swap;
    src: local('$name'),
         url('woff2/$filestem.woff2') format('woff2'),
         url('woff/$filestem.woff') format('woff');
}

""")

FONT_WEIGHTS = {
    "hairline": 100,
    "thin": 200,
    "extralight": 200,
    "light": 300,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
    "extrabold": 800,
    "heavy": 800,
    "black": 900,
}

fontmeta = configparser.ConfigParser()
with open("fontmeta.ini", "r") as configfile:
    fontmeta.read_file(configfile)

for fontname in fontmeta.sections():
    print("Generating CSS for", fontname)
    fontpath = pathlib.Path(fontname)
    cssfile = open(fontpath / (fontname + ".css"), "w")
    cssfile.write(HEADER_TEMPLATE.substitute(
        name=fontname,
        designer=fontmeta[fontname]["Designer"],
        url=fontmeta[fontname]["URL"],
        license=fontmeta[fontname]["License"]
    ))

    variants = []
    for fontfile in fontpath.glob("ttf/*.ttf"):
        filestem = fontfile.stem
        words = filestem.split()
        style = "normal"
        weight = 400
        for word in words:
            word = word.lower()
            if word == "italic":
                style = "italic"
            if word in FONT_WEIGHTS:
                weight = FONT_WEIGHTS[word]

        variants.append({
            "name": fontname,
            "style": style,
            "weight": weight,
            "filestem": filestem
        })

    variants.sort(key=lambda x: (x["weight"], x["style"] == "italic"))
    for variant in variants:
        cssfile.write(FONTFACE_TEMPLATE.substitute(**variant))
