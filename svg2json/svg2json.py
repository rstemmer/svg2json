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

import sys
import argparse
from pathlib import Path

import base64
import json

# Load Scour for SVG optimization
from scour.scour import scourString
from scour.scour import sanitizeOptions as sanitizeScourOptions
from scour.scour import parse_args as parseScourArgs

VERSION = "0.1.0"


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


def SVGFileToDataURI(svgpath):
    try:
        with open(svgpath) as fd:
            sourcesvg = fd.read()
    except FileNotFoundError:
        print("Path %s not found. SVG will be skipped!"%(str(svgpath)), file=sys.stderr)
        return None

    optimizedsvg = Optimize(sourcesvg)
    encodedsvg   = Base64Encode(optimizedsvg)
    datauri      = MakeDataURI(encodedsvg)
    return datauri


def GetSVGNameFromPath(path):
    file = Path(path.name)  # Get full file name from path
    name = file.stem        # Get only the name without suffix
    return str(name)


def main():
    argparser = argparse.ArgumentParser(description="Consolidate svg files into a single json file")
    argparser.add_argument("-v", "--version", action="store_true", help="show version and exit.")
    argparser.add_argument("svgpaths", metavar="svgpath", type=str, nargs="+", help="A set of SVG files to collect.")
    argparser.add_argument("-o", "--output", metavar="jsonpath", type=str, help="Path to store the JSON file. If not given, it will be printed to stdout.")

    # Parse command line arguments
    args = argparser.parse_args()

    if args.version:
        print(VERSION)
        exit(0)

    svgpaths = args.svgpaths
    jsonpath = args.output

    # Process SVG files
    svgmap = list()
    for svgpath in svgpaths:
        svgpath = Path(svgpath)
        datauri = SVGFileToDataURI(svgpath)
        svgname = GetSVGNameFromPath(svgpath)
        svgmap.append({svgname: datauri})

    # Create outpup
    jsonstring   = json.dumps(svgmap)
    jsonstring  += "\n" # I like line breaks at the end of a file

    if jsonpath:
        with open(jsonpath, "w") as fd:
            fd.write(jsonstring)
    else:
        print(jsonstring)


if __name__ == "__main__":
    main()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

