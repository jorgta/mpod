import menus


mpod_horiz_items = [
    menus.menu_item("/index", "home"),
    menus.menu_item("/data/intro", "datafiles"),
    menus.menu_item("/dict/intro", "dictionary"),
    ]

mpod_verti_items = [
    menus.menu_item("/index", "introduction"),
    menus.menu_item("/references", "references"),
    menus.menu_item("/credits", "credits"),
    menus.menu_item("/disclaimer", "disclaimer"),
    ]
    
data_verti_items = [
    menus.menu_item("/data/intro", "intro"),
    menus.menu_item("/data/search", "search"),
    menus.menu_item("/data/properties", "properties"),
    menus.menu_item("/data/doc", "documentation"),
    menus.menu_item("/data/references", "references"),
    ]

dict_verti_items = [
    menus.menu_item("/dict/intro", "introduction"),
    menus.menu_item("/dict/doc", "documentation"),
    ]

mpod_horiz_menu={"items":mpod_horiz_items, "menu_class":"hor_menu", "menu_ul_id":"nav"}
mpod_verti_menu={"items":mpod_verti_items, "menu_class":"ver_menu", "menu_ul_id":"menu1"}
data_verti_menu={"items":data_verti_items, "menu_class":"ver_menu", "menu_ul_id":"menu1"}
dict_verti_menu={"items":dict_verti_items, "menu_class":"ver_menu", "menu_ul_id":"menu1"}

if __name__=="__main__":
    items_list_act=menus.add_active_to_menu(dj_txrf_horiz_menu.get("items"), "\index.html", 0)
    print items_list_act
