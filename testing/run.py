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

def tab_style() -> str:
  return ".tab { overflow: hidden; border: 1px solid #ccc; "\
       + "background-color: #f1f1f1; }"
  
def button_style() -> str:
  return ".our_button { text-decoration: none; background-color: #EEEEEE; " \
       + "color: #333333; padding: 2px 6px 2px 6px; }"
  
def tooltip
  
def main_style() -> str:
  return ""

#
# Main Section
#

def interface() -> str:
  script = "<script>" + "" + "</script>"
  style = "\n".join(["<style>", main_style(), tab_style(), button_style(),
                     tooltip_style(), "</style>"])
  body = "<body> Hello </body>"
  return "\n".join(["<html>", script, style, body, "</html>"])
  
os.system('echo "" > resources/interface.html')
print(interface(), file = open("resources/interface.html", "w"))



