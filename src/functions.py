import os
import aiogram

import player


def create_new_account(id: int, username: str, full_name: str) -> player.Player:
    account = player.Player(
        id=id,
        login=username,
        name=full_name,
        language="en",
        location={"location": "Forest", "status": "Stay"},
        previous_locations=[],
        hp=100,
        experience=0,
        reputation=0,
        money=0,
        equipment={"cloths": "Rags", "weapon": "Stick"},
        inventory={},
        quests={},
        enemies={},
        buttons=[]
    )
    account.update_data()
    return account


def create_exist_account(id: int, username: str, full_name: str) -> player.Player:
    player_data = player.get_dict_from_json(f"../players_data/{id}.json")
    account = player.Player(
        id=id,
        login=username,
        name=full_name,
        language=player_data["language"],
        location=player_data["location"],
        previous_locations=player_data["previous_locations"],
        hp=player_data["hp"],
        experience=player_data["experience"],
        reputation=player_data["reputation"],
        money=player_data["money"],
        equipment=player_data["equipment"],
        inventory=player_data["inventory"],
        quests=player_data["quests"],
        enemies=player_data["enemies"],
        buttons=player_data["buttons"]
    )
    return account


def except_new_player(id: int, username: str, full_name: str) -> player.Player:
    if f"{id}.json" in os.listdir("../players_data/"):
        return create_exist_account(id, username, full_name)
    return create_new_account(id, username, full_name)


def execute_action(id: int, username: str, full_name: str, text: str) -> str:
    account = except_new_player(id, username, full_name)
    return account.perform_action(text)


def get_action_buttons(id: int, username: str, full_name: str) -> list:
    account = except_new_player(id, username, full_name)
    account.update_buttons()
    buttons = []
    for button in account.buttons:
        buttons.append(aiogram.types.InlineKeyboardButton(button["text"], callback_data=button["cbd"]))
    return buttons


def get_languages_buttons() -> list:
    languages = []
    for language in os.listdir("../game_data/languages/"):
        languages.append(aiogram.types.InlineKeyboardButton(language.split(".")[0], callback_data=language.split(".")[0]))
    return languages


def get_all_actions() -> tuple:
    return tuple(player.get_dict_from_json("../game_data/resources/actions.json").keys())


def get_player_info(id: int, username: str, full_name: str) -> str:
    account = except_new_player(id, username, full_name)
    return account.info()


def get_player_inventory_info(id: int, username: str, full_name: str) -> str:
    account = except_new_player(id, username, full_name)
    return account.inventory_info()


def get_quests_progres(id: int, username: str, full_name: str) -> str:
    account = except_new_player(id, username, full_name)
    return account.quests_info()
