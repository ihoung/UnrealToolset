import os
import sys
import json
from pathlib import Path
import unreal

sys.path.append(os.path.dirname(__file__))

from tools.attach_socket import AttachSocketWnd

def add_entry(menu: unreal.ToolMenu, subdata):
    section_name = subdata["section"].strip()
    if section_name:
        menu.add_section(section_name, subdata["section"])

    if subdata["type"]:
        sub_menu = menu.add_sub_menu(
            owner=menu.menu_name, 
            section_name=section_name, 
            name=subdata["name"], 
            label=subdata["label"], 
            tool_tip=subdata["tool_tip"]
        )
        for sub_data in subdata["subs"]:
            add_entry(sub_menu, sub_data)
    else:
        entry = unreal.ToolMenuEntry(
            name = subdata["name"],
            type = unreal.MultiBlockType.MENU_ENTRY,
        )
        entry.set_label(subdata["label"])
        entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, "Python", subdata["command"])
        menu.add_menu_entry(section_name, entry)


def main():

    menus = unreal.ToolMenus.get()

    # Find the 'edit' menu, this should not fail, 
    # but if we're looking for a menu we're unsure about 'if not' 
    # works as nullptr check,
    main_menu = menus.find_menu("LevelEditor.MainMenu")
    toolset_menu = main_menu.add_sub_menu("My.Menu", "Python", "Toolset", "Toolset")

    # for name in ["Foo", "Bar", "Baz"]:
    #     e = unreal.ToolMenuEntry(
    #         name = name,
    #         type = unreal.MultiBlockType.MENU_ENTRY, # If you pass a type that is not supported Unreal will let you know,
    #     )
    #     e.set_label(name)
    #     toolset_menu.add_menu_entry("Items", e)
    path = Path(__file__).with_name("menu.json")
    with path.open('r') as file:
        file_str = file.read()
        data = json.loads(file_str)
        for subdata in data:
            add_entry(toolset_menu, subdata)

    menus.refresh_all_widgets()

if __name__ == '__main__':
    main()