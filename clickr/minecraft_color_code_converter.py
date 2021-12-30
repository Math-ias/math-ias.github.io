import sys
import re

FORMATTING_CODE = "§"

COLOR_CODE_TO_HEX = {
    # BLACK
    "0": "#000000",
    # DARK_BLUE
    "1": "#0000AA",
    #DARK_GREEN
    "2": "#00AA00",
    #DARK_AQUA
    "3": "#00AAAA",
    #DARK_RED
    "4": "#AA0000",
    #DARK_PURPLE
    "5": "#AA00AA",
    #GOLD
    "6": "#FFAA00",
    #GRAY
    "7": "#AAAAAA",
    #DARK_GRAY
    "8": "#555555", 
    #BLUE
    "9": "#5555FF", 
    #GREEN
    "A": "#55FF55", 
    #AQUA
    "B": "#55FFFF",
    #RED
    "C": "#FF5555", 
    #LIGHT_PURPLE
    "D": "#FF55FF", 
    #YELLOW
    "E": "#FFFF55", 
    #WHITE
    "F": "#FFFFFF"
}

data = sys.stdin.read()
print(re.sub(
    re.escape(FORMATTING_CODE) + r'(\w)(.)',
    lambda match_obj: f"<span style=\"color: {COLOR_CODE_TO_HEX[match_obj.group(1).upper()]}\">{match_obj.group(2)}</span>",
    data))