# svg2json

Collects a set of SVG vector graphics into a single JSON file using data URIs

**This project is currently in beta stage**

TODO: Motivation:

- lots of small files
- -> lots of communication overhead
- -> bad UX - some icons (in browser cache) are visible, some pop up later

## Dependencies

- scour: https://github.com/scour-project/scour

## Build and Install from Source

```bash
./pkg-build
sudo pip install --upgrade ./dist/svg2json-0.2.0-py3-none-any.whl
```

## Install via pip

```bash
pip install svg2json
```

## Usage

```bash
svg2json --help
```

```bash
svg2json -o iconset.json iconset/*.svg
```

```bash
svg2json good.svg bad.svg > status.json
```

## Example Use-Case

A set of icons shall be collected and used by a web application, instead of loading each icon individually.
The client then should use the cached icons from the JSON file.

This example setup and the provided JavaScript code are based on
and inspired by the [MusicDB Project](https://github.com/rstemmer/musicdb).

### Server Side

```bash
# What we start with:
ls ./icons
# Add.svg  Album.svg  AlbumFile.svg ... vMax.svg  vMin.svg  vThis.svg
find ./icons -type f -name "*.svg" -print | wc -l
# 92 svg files
du -hc ./icons/*.svg
# 592KB of data

# Collecting all vector graphics into a singe JSON file:
svg2json -o icons.json ./icons/*.svg

# The resulting JSON file
du -h icons.json
# 204K - thanks to size optimization using Scour
```

Example of a generated JSON file (here: icons.json):
```json
{
    "Add":       "data:image/svg+xml;base64,<data>",
    "Album":     "data:image/svg+xml;base64,<data>",
    "AlbumFile": "data:image/svg+xml;base64,<data>",
    // ...
    "vMax":      "data:image/svg+xml;base64,<data>",
    "vMin":      "data:image/svg+xml;base64,<data>",
    "vThis":     "data:image/svg+xml;base64,<data>"
}
```

### Client side

The `IconManager` class loads the JSON file with all accumulated icons.
Keep in mind that this happens asynchronously.
So right after creating an instanced of this class, the cache is empty.
Anyway the `GetIcon` code is aware of this situation and allows loading
icons from the server that are not yet cached.
Either the JSON file has not been loaded or the icons are not included in the cached icon files.

```javascript
// Warning: I just hacked down this code for demonstration purpose.
// It certainly can be improved. At least by error handling inside the LoadIcons method.

class IconManager
{
    constructor(fileurl=null)
    {
        this.iconcache = new Object();  // Empty object = empty cache
        if(typeof fileurl === "string")
            this.LoadIcons(fileurl);    // Load icons
    }

    LoadIcons(fileurl)
    {
        let request = new XMLHttpRequest();
        request.addEventListener("load", 
            (event)=>
            {
                let jsonstring = event.target.responseText;
                this.iconcache = JSON.parse(jsonstring);
            },
            false);
        request.open("GET", fileurl);
        request.send();
    }

    GetIcon(iconname)
    {
        // If icon exists in the cache, use it.
        // Otherwise load it from the server.
        let uri;
        if(iconname in this.iconcache)
            uri = `url(${this.iconcache[iconname]})`;
        else
            uri = `url("img/icons/${iconname}.svg")`;

        // Create image element and set the icon as source
        let icon = new Image();
        icon.src = uri;
        return icon;
    }
}
```

```javascript
let iconmanager = new IconManager("img/icons.json");

// ...

let icon_add = iconmanager.GetIcon("Add");
document.body.appendChild(icon_add);
```

The shown example code comes without any dependencies despite some classes that are provided by web browsers:

- [XMLHttpRequest](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest) for loading files from the server
- [Image](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/Image) for creating an HTML image element (`<img>`)

