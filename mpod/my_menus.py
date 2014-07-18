import menus


mpod_left_items = [
    menus.menu_item("/index", "search", "search-option"),
    menus.menu_item("/data/intro", "documentation", "doc-option"),
    menus.menu_item("/dict/intro", "submit", "submit-option"),
    ]

mpod_top_items = [
    menus.menu_item("/index", "introduction"),
    menus.menu_item("/references", "references"),
    menus.menu_item("/credits", "credits"),
    menus.menu_item("/disclaimer", "disclaimer"),
    ]
    
data_top_items = [
    menus.menu_item("/data/intro", "intro"),
    menus.menu_item("/data/search", "search"),
    menus.menu_item("/data/properties", "properties"),
    menus.menu_item("/data/doc", "documentation"),
    menus.menu_item("/data/references", "references"),
    ]

dict_top_items = [
    menus.menu_item("/dict/intro", "introduction"),
    menus.menu_item("/dict/doc", "documentation"),
    ]

mpod_nav_menu={"items":mpod_left_items, "menu_class":"left-nav", "menu_ul_id":"nav"}
mpod_top_menu={"items":mpod_top_items,  "menu_class":"top-nav",  "menu_ul_id":"menu1"}
data_top_menu={"items":data_top_items,  "menu_class":"top-nav",  "menu_ul_id":"menu1"}
dict_top_menu={"items":dict_top_items,  "menu_class":"top-nav",  "menu_ul_id":"menu1"}

if __name__=="__main__":
    items_list_act=menus.add_active_to_menu(dj_txrf_horiz_menu.get("items"), "\index.html", 0)
    print items_list_act
