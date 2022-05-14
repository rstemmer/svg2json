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


def main():
    with open("LineTest.svg") as fd:
        sourcesvg = fd.read()

    optimizedsvg = Optimize(sourcesvg)
    print(optimizedsvg)


if __name__ == "__main__":
    main()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

