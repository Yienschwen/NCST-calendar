# NCST calendar generator

## Quickstart

1. Save the `HTML` source of the table which contains all course info. 
   You may have a look at the `example.html` to find out what it really means and looks like.
2. Make a directory `output`, where to place the `svg` files of each week.
2. Open `main.py` and revise the date of the first day yourself, in line 8 as `d = date(yyyy, mm, dd)`.
3. Execute `python3 main.py YOUR_HTML_SOURCE.html`. This step will generate `svg` files of each week.
4. (Optional) Here I enclosed a simple tool `svg2pdf.sh`. Copy this script into `./output` and execute it.
   This will convert `week_i.svg` to `week_i.svg.pdf`. You may want `pdf`-format files rather than `svg`
   to print it out.

## Dependency

* `python3`
* (Optional, needed by `svg2pdf.sh`) `rsvg-convert`

## Lisence

GPLv2