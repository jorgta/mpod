from django.template.loader import get_template
from django.template import Template
from django.template import Context

import os
import string

class menu_item:
    def __init__(self, ref, name, item_class=False):
        self.ref, self.name, self.item_class = ref, name, item_class

class menu_list:
    def __init__(self, items_list, menu_class, list_id, menu_level):
        t = get_template('mpod_menu_base.html')
        c=Context({
        'menu_div_class': menu_class,
        'menu_ul_id': list_id,
        'menu_items_list':items_list
        })
        self.html=t.render(c)
        self.level=menu_level
        
def add_active_to_menu(menu_items, req_item_ref, menu_level):
    """
    level 0 is the most surface level
    level 1 is 1 level down and so on
    the requested item is e.g. "/index.html" or "en/index.htm"
    "index.html" is the level 0 "en" is level 1
    """
    menu_items_refs=[menu_item.ref for menu_item in menu_items]
    req_item_ref_clean=req_item_ref.replace("\\","/").split("/")[-(menu_level+1)]
    if req_item_ref_clean in menu_items_refs:
        inde=menu_items_refs.index(req_item_ref_clean)
        menu_items[inde].item_class="active"
    return menu_items

def menu(menu_dict, request_path, level):
    items_list_act=add_active_to_menu(menu_dict.get("items"), request_path, level)
    this_menu=menu_list(items_list_act, menu_dict.get("menu_class"), menu_dict.get("menu_ul_id"), level)
    return this_menu.html
