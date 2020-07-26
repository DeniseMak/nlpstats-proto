"""
Jesse Gioannini & Denise Mak

This program generates the web interface HTML document.
"""

import os

#
# Form Section
#

def radio_button() -> str:
  return ""
  
def number_input() -> str:
  return ""
  
def form() -> str:
  return ""
  
#
# Style Section
#

def header_style() -> str:
  return ".header { text-align: center; }"

def tab_style() -> str:
  return """
.tab { overflow: hidden; border: 1px solid #ccc; "background-color: #f1f1f1; }
"""
  
def button_style() -> str:
  return """
.our_button { text-decoration: none; background-color: #EEEEEE;
              color: #333333; padding: 2px 6px 2px 6px; }
"""
  
def tooltip_style() -> str:
  return """
/* Adapted from W3Schools Tutorial: https://www.w3schools.com/css/css_tooltip.asp*/
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  

  position: absolute;
  z-index: 1;
  top: -5px;
  left: 105%;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
}
"""

def footer_style() -> str:
  return ".footer { text-align: center; }"

#
# Body Section
#
  
def header() -> str:
  return """
<div class="header">
<h1>System Performance Calculator</h1>
</div>
"""

def tooltip(string: str) -> str:
  return '<div class="tooltip"> ? <span class="tooltiptext">' + string \
       + '</span> </div>'

def footer() -> str:
  return """
<div class="footer">
<p>Copyright 2020 AUTHORS. This website is released under the terms of the LICENSE. See the paper at LINK.</p>
</div>
"""

def main_style() -> str:
  return ""

#
# Main Section
#

def interface() -> str:
  script = "<script>" + "" + "</script>"
  style = "\n".join(["<style>", header_style(), tooltip_style(), footer_style(), "</style>"])
  body = "\n".join(["<body>", header(), tooltip("Answer"), footer(), "</body>"])
  return "\n".join(["<!DOCTYPE html><html>", script, style, body, "</html>"])
  
os.system('echo "" > templates/interface.html')
print(interface(), file = open("templates/interface.html", "w"))

#
# Flask
#


