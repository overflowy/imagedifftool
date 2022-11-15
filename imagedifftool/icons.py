"""
https://github.com/tabler/tabler-icons

MIT License

Copyright (c) 2020-2022 Paweł Kuna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

COLOR = "white"
STROKE_WIDTH = 2


run = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-player-play" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M7 4v16l13 -8z"></path>
</svg>"""
undo = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-arrow-back-up" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M9 13l-4 -4l4 -4m-4 4h11a4 4 0 0 1 0 8h-1"></path>
</svg>"""
redo = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-arrow-forward-up" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M15 13l4 -4l-4 -4m4 4h-11a4 4 0 0 0 0 8h1"></path>
</svg>"""
pointer = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-pointer" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
  <path d="M7.904 17.563a1.2 1.2 0 0 0 2.228 .308l2.09 -3.093l4.907 4.907a1.067 1.067 0 0 0 1.509 0l1.047 -1.047a1.067 1.067 0 0 0 0 -1.509l-4.907 -4.907l3.113 -2.09a1.2 1.2 0 0 0 -.309 -2.228l-13.582 -3.904l3.904 13.563z" />
</svg>"""
marquee = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-marquee-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M4 6v-1a1 1 0 0 1 1 -1h1m5 0h2m5 0h1a1 1 0 0 1 1 1v1m0 5v2m0 5v1a1 1 0 0 1 -1 1h-1m-5 0h-2m-5 0h-1a1 1 0 0 1 -1 -1v-1m0 -5v-2"></path>
</svg>"""
move = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-arrows-move" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M18 9l3 3l-3 3"></path>
   <path d="M15 12h6"></path>
   <path d="M6 9l-3 3l3 3"></path>
   <path d="M3 12h6"></path>
   <path d="M9 18l3 3l3 -3"></path>
   <path d="M12 15v6"></path>
   <path d="M15 6l-3 -3l-3 3"></path>
   <path d="M12 3v6"></path>
</svg>"""
crop = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-crop" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M8 5v10a1 1 0 0 0 1 1h10"></path>
   <path d="M5 8h10a1 1 0 0 1 1 1v10"></path>
</svg>"""
zoomIn = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-zoom-in" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <circle cx="10" cy="10" r="7"></circle>
   <line x1="7" y1="10" x2="13" y2="10"></line>
   <line x1="10" y1="7" x2="10" y2="13"></line>
   <line x1="21" y1="21" x2="15" y2="15"></line>
</svg>"""
zoomOut = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-zoom-out" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <circle cx="10" cy="10" r="7"></circle>
   <line x1="7" y1="10" x2="13" y2="10"></line>
   <line x1="21" y1="21" x2="15" y2="15"></line>
</svg>"""
zoomFit = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-zoom-code" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <circle cx="10" cy="10" r="7"></circle>
   <path d="M21 21l-6 -6"></path>
   <path d="M8 8l-2 2l2 2"></path>
   <path d="M12 8l2 2l-2 2"></path>
</svg>"""
rotateClockwise = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-rotate-clockwise" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M4.05 11a8 8 0 1 1 .5 4m-.5 5v-5h5"></path>
</svg>"""
rotateCounterClockwise = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-rotate" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M19.95 11a8 8 0 1 0 -.5 4m.5 5v-5h-5"></path>
</svg>"""
flipHorizontal = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-flip-horizontal" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <line x1="3" y1="12" x2="21" y2="12"></line>
   <polyline points="7 16 17 16 7 21 7 16"></polyline>
   <polyline points="7 8 17 8 7 3 7 8"></polyline>
</svg>"""
flipVertical = f"""<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-flip-vertical" width="24" height="24" viewBox="0 0 24 24" stroke-width="{STROKE_WIDTH}" stroke="{COLOR}" fill="none" stroke-linecap="round" stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <line x1="12" y1="3" x2="12" y2="21"></line>
   <polyline points="16 7 16 17 21 17 16 7"></polyline>
   <polyline points="8 7 8 17 3 17 8 7"></polyline>
</svg>"""
