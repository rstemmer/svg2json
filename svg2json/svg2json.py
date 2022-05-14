#!/usr/bin/env python3

#  svg2json
#
#  Copyright 2022 Ralf Stemmer <ralf.stemmer@gmx.net>
#
#  This file is part of svg2json, https://github.com/rstemmer/svg2json
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import base64
import json

# Load Scour for SVG optimization
from scour.scour import scourString
from scour.scour import sanitizeOptions as sanitizeScourOptions
from scour.scour import parse_args as parseScourArgs

VERSION = "0.0.1"


def Optimize(sourcesvg):
    scouroptions = parseScourArgs([
        "--enable-id-stripping",
        "--enable-comment-stripping",
        "--shorten-ids",
        "--indent=none",
        "--no-line-breaks"])
    scouroptions = sanitizeScourOptions(scouroptions)
    optimizedsvg = scourString(sourcesvg, scouroptions)
    return optimizedsvg


def Base64Encode(sourcesvg):
    utf8code     = sourcesvg.encode("UTF-8")
    base64code   = base64.b64encode(utf8code)
    base64string = base64code.decode("UTF-8")
    return base64string


def MakeDataURI(data, mediatype="image/svg+xml", encoding="base64"):
    uri  = "data:"
    uri += mediatype
    if type(encoding) is str:
        uri += ";" + encoding
    uri += "," + data
    return uri


def main():
    with open("LineTest.svg") as fd:
        sourcesvg = fd.read()

    optimizedsvg = Optimize(sourcesvg)
    print(optimizedsvg)
    encodedsvg   = Base64Encode(optimizedsvg)
    print(encodedsvg)
    datauri      = MakeDataURI(encodedsvg)
    print(datauri)
    svgmap       = list()
    svgmap.append({"LineTest": datauri})
    jsonstring   = json.dumps(svgmap)
    print(jsonstring)


if __name__ == "__main__":
    main()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

