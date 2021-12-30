# This script relies on beautifulsoup4.
# I'm also using lxml as the HTML parser,
# which is recommended for better performance.
# I invoke these using a virtualenv.

PARSER = "html5lib"
SIDENOTE_SYMBOL = "†"
SIDENOTE_ELEMENT = "small"
SIDENOTE_CONTAINER_CLASS = "withsmall"
DEFAULT_CSS_ID = "default"
SIDENOTED_CSS_ID = "sidenoted"

import os
SIDENOTE_CSS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sidenote.css")

# A script dedicated to taking HTML as STDIN with sidenotes referenced inline with SIDENOTE_SYMBOL,
#  * finding the <small> element it is referring to (the nearest occurrence)
#  * smartly wrapping _something_ and the <small> element in a <div class="withsmall">.
#       * That something could be a single HTML element.
#       * That something could be multiple HTML elements, bundled together with a div.
#       * The first element not wrapped in text (e.g a paragraph, or list) will have it's top margin reset.

# This script will also inject the necessary stylesheet for sidenotes into the head of the document.
# The document is never in a weird state.

from bs4 import BeautifulSoup
import sys
import re

with open(sys.argv[1]) as fp:
    soup = BeautifulSoup(fp.read(), PARSER)
contains_reference_regex = re.compile(SIDENOTE_SYMBOL)
referencing_sidenote = soup.find_all(text=contains_reference_regex)

if len(referencing_sidenote) > 0:
    # If there ARE sidenotes, we'll override the style.
    head = soup.find("head")
    if head is None:
        raise SyntaxError("HTML document missing head!")
    stylesheet = head.find(id=DEFAULT_CSS_ID)
    existing_stylesheet = head.find(id=SIDENOTED_CSS_ID) # We also check if this file was already been processed.
    if existing_stylesheet or stylesheet is None:
        exit()
    stylesheet['id'] = SIDENOTED_CSS_ID
    with open(SIDENOTE_CSS_FILE) as fp:
        stylesheet.string = fp.read()

from itertools import accumulate

# A method dedicated to finding the sidenote element, starting with next siblings, and then next siblings of ancestors.
# This returns ...
# * the list of ancestors (including that to the root) siblings with the sidenote, the sidenote itself
# * None if nothing can be found.
def find_sidenote(root):
    for sibling_list in accumulate(root.next_siblings, func=lambda prev, curr: prev + [curr], initial=[root]):
        sibling = sibling_list[-1]
        if sibling.name == SIDENOTE_ELEMENT:
            return sibling_list[0:-1], sibling
    if root.parent is None:
        return None, None
    else: 
        return find_sidenote(root.parent)

for navigable_string in referencing_sidenote:
    # First we find the sidenote referenced.
    ancestor_and_siblings, referenced_sidenote = find_sidenote(navigable_string.parent)
    # THEN! The interesting part ...
    # IF the referenced_sidenote cannot be found, we error out!
    if referenced_sidenote is None:
        raise SyntaxError(f"Input ({navigable_string}) uses a sidenote symbol, but no follow-up sidenote element using the <{SIDENOTE_ELEMENT}> tag could be found.")
    # In either case, we'll be creating a sidenote container.
    sidenote_container = soup.new_tag("div")
    sidenote_container['class'] = sidenote_container.get('class', []) + [SIDENOTE_CONTAINER_CLASS]
    ancestor = ancestor_and_siblings[0]
    ancestor['style'] = ancestor.get('style', '') + "margin-top: 0;" 
    ancestor.insert_before(sidenote_container)
    # IF the ancestor is next to the referencing sidenote, we do the wrap with the two elements.
    if len(list(filter(lambda object: object.name is not None, ancestor_and_siblings))) == 1:
        sidenote_container.append(ancestor)
    # IF the ancestor is NOT next to the referencing sidenote, we wrap all non sidenote siblings in a div, and then we wrap.
    else:
        ancestor_and_siblings_container = soup.new_tag("div")
        sidenote_container.append(ancestor_and_siblings_container)
        ancestor_and_siblings_container.extend(ancestor_and_siblings)

    sidenote_container.append(referenced_sidenote)
    
with open(sys.argv[1], "w") as fp:
    fp.write(soup.prettify())