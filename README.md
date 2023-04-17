# hp-scan-wrapper
This script wraps around [hp-scan](https://developers.hp.com/hp-linux-imaging-and-printing/tech_docs/man_pages/scan) for easier multi-page scans and because i wanted to learn docopt.

My scanner isn't able to scan duplex, so duplex scanning works by scanning pages 1,3,[...] and then turning the paper around to scan pages 10,8,[...]. Afterwards they get sorted and appended in the correct order.

# Known errors
Using higher resolutions and/or scanning many pages at once, you may run into PIL.Image.DecompressionBombError due to the filesize limit. 

![image](https://user-images.githubusercontent.com/460656/232577628-45476133-3eb5-48ec-86b8-568f54f3f183.png)

To fix this you could add ```Image.MAX_IMAGE_PIXELS = None``` in line 1731, where `hp-scan` calls `PIL`.
