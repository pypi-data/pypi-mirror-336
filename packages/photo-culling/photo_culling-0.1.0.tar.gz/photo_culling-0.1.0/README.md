# Photoculling
Fast image viewer, which uses aggressive prefetching and caching to very quickly move between photos.
Minimal interface to select photos to keep and copy to output directory.

# Installation
Installation is easiest using the uv package manager.

[Install uv](https://docs.astral.sh/uv/getting-started/installation/), which exists for linux, macOS, windows, e.g. via
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install photoculling
```bash
uv tool install photoculling
```
This installs a compatible python environment, the photoculling package and all its dependencies (mainly Qt).

Start culling!
```bash
cull path/to/directory/with/jpgs
```

# Controls 

- Left/right arrow keys: move 1 image
- A/D keys: move 10 images
- F11: fullscreen
- ESC: quit

In the top left corner the current position within the photo stack is displayed and in parenthesis the number of selected images.
For photos which have been selected this textbox is green.
When quitting, all selected photos (and all other files which share the selected filenames but with different extensions, e.g. RAW files) are copied to the selected target directory.

