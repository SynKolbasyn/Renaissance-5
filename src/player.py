import ujson
import random


def get_dict_from_json(file_name: str) -> dict:
    with open(file_name, "r", encoding="utf-8") as file:
        return ujson.load(file)


class Player:
    def __init__(self, id: int, login: str, name: str, language: str, location: dict, previous_locations: list, hp: int,
                 experience: int, reputation: int, money: int, equipment: dict, inventory: dict, quests: dict,
                 enemies: dict, buttons: list):
        self.id = id
        self.login = login
        self.name = name
        self.language = language
        self.location = location
        self.previous_locations = previous_locations
        self.hp = hp
        self.experience = experience
        self.reputation = reputation
        self.money = money
        self.equipment = equipment
        self.inventory = inventory
        self.quests = quests
        self.enemies = enemies
        self.buttons = buttons

    def LOCATIONS(self) -> dict:
        return get_dict_from_json("../game_data/resources/locations.json")

    def STATUSES(self) -> dict:
        return get_dict_from_json("../game_data/resources/statuses.json")

    def ACTIONS(self) -> dict:
        return get_dict_from_json("../game_data/resources/actions.json")

    def ITEMS(self) -> dict:
        return get_dict_from_json("../game_data/resources/items.json")

    def QUESTS(self) -> dict:
        return get_dict_from_json("../game_data/resources/quests.json")

    def NPC(self) -> dict:
        return get_dict_from_json("../game_data/resources/npc.json")

    def TRANSLATIONS(self) -> dict:
        return get_dict_from_json(f"../game_data/languages/{self.language}.json")

    def get_dict_data(self) -> dict:
        return {
            "id": self.id,
            "login": self.login,
            "name": self.name,
            "language": self.language,
            "location": self.location,
            "previous_locations": self.previous_locations,
            "hp": self.hp,
            "experience": self.experience,
            "reputation": self.reputation,
            "money": self.money,
            "equipment": self.equipment,
            "inventory": self.inventory,
            "quests": self.quests,
            "enemies": self.enemies,
            "buttons": self.buttons
        }

    def update_data(self):
        with open(f"../players_data/{self.id}.json", "w", encoding="utf-8") as file:
            ujson.dump(self.get_dict_data(), file, indent=2, ensure_ascii=False)

    def damage(self) -> int:
        return self.ITEMS()[self.equipment["weapon"]]["damage"]

    def t(self, string: str) -> str:
        return self.TRANSLATIONS()[string] if string in self.TRANSLATIONS().keys() else string

    def tl(self, array: list) -> list:
        t_array = []
        for element in array:
            t_array.append(self.t(element))
        return t_array

    def info(self) -> str:
        return f"ID: {self.id}\n" \
               f"{self.t('Name')}: {self.name}\n" \
               f"{self.t('Location')}: {self.t(self.location['location'])}\n" \
               f"{self.t('Status')}: {self.t(self.location['status'])}\n" \
               f"{self.t('Cloths')}: {self.t(self.equipment['cloths'])}\n" \
               f"{self.t('Weapon')}: {self.t(self.equipment['weapon'])}\n" \
               f"HP: {self.hp}\n" \
               f"{self.t('Damage')}: {self.damage()}\n" \
               f"{self.t('Experience')}: {self.experience}\n" \
               f"{self.t('Reputation')}: {self.reputation}\n" \
               f"{self.t('Money')}: {self.money}"

    def quests_info(self) -> str:
        if self.quests == {}:
            return self.t("You have not got any quest")
        answer = ""
        for index, quest in enumerate(self.quests):
            answer += f"{index + 1}. {quest} -> {self.quests[quest]['progres']}/{self.quests[quest]['goal']}\n"
        return answer[:-1]

    def inventory_info(self) -> str:
        info = ""
        for item_name in self.inventory:
            info += f"{self.t(item_name)} -> {self.inventory[item_name]}\n"
        if info == "":
            return self.t("Your inventory is empty")
        return info

    def buttons_sell(self) -> list:
        items_to_sell = []
        for item_name in self.inventory:
            if "sell" in self.ITEMS()[item_name]["types"]:
                items_to_sell.append({"text": self.t(item_name) + " - " + str(self.ITEMS()[item_name]["price"]) + "cr", "cbd": item_name})
        items_to_sell.append({"text": self.t("Leave"), "cbd": "Leave"})
        return items_to_sell

    def buttons_buy(self) -> list:
        items_to_buy = []
        for item_name in self.LOCATIONS()[self.location["location"]]["items"]:
            items_to_buy.append({"text": self.t(item_name) + " - " + str(self.LOCATIONS()[self.location["location"]]["items"][item_name]) + "cr", "cbd": item_name})
        items_to_buy.append({"text": self.t("Leave"), "cbd": "Leave"})
        return items_to_buy

    def buttons_info(self) -> list:
        info_items = []
        for item_name in self.inventory:
            if "info" in self.ITEMS()[item_name]["types"]:
                info_items.append({"text": self.t(item_name), "cbd": item_name})
        info_items.append({"text": self.t("Leave"), "cbd": "Leave"})
        return info_items

    def buttons_equip(self) -> list:
        eqip_items = []
        for item_name in self.inventory:
            if ("equipment_cloths" in self.ITEMS()[item_name]["types"]) or ("equipment_weapon" in self.ITEMS()[item_name]["types"]):
                eqip_items.append({"text": self.t(item_name), "cbd": item_name})
        eqip_items.append({"text": self.t("Leave"), "cbd": "Leave"})
        return eqip_items

    def buttons_use(self) -> list:
        use_items = []
        for item_name in self.inventory:
            if "use" in self.ITEMS()[item_name]["types"]:
                use_items.append({"text": self.t(item_name), "cbd": item_name})
        use_items.append({"text": self.t("Leave"), "cbd": "Leave"})
        return use_items

    def buttons_accepts_quest(self) -> list:
        quests = []
        for quest in self.QUESTS():
            if self.location["location"] == self.QUESTS()[quest]["location"]:
                quests.append({"text": self.t(quest), "cbd": quest})
        quests.append({"text": self.t("Leave"), "cbd": "Leave"})
        return quests

    def buttons_submits_quest(self) -> list:
        quests = []
        for quest in self.quests:
            quests.append({"text": self.t(quest), "cbd": quest})
        quests.append({"text": self.t("Leave"), "cbd": "Leave"})
        return quests

    def dynamic_buttons(self) -> list:
        if self.location["status"] == "Sell":
            return self.buttons_sell()
        if self.location["status"] == "Buy":
            return self.buttons_buy()
        if self.location["status"] == "Read":
            return self.buttons_info()
        if self.location["status"] == "Equip":
            return self.buttons_equip()
        if self.location["status"] == "Use":
            return self.buttons_use()
        if self.location["status"] == "Accepts quest":
            return self.buttons_accepts_quest()
        if self.location["status"] == "Submits quest":
            return self.buttons_submits_quest()

    def update_buttons(self):
        if self.STATUSES()[self.location["status"]]["type"] == "new actions":
            self.buttons = []
            for element in self.STATUSES()[self.location["status"]]["actions"]:
                self.buttons.append({"text": self.t(element), "cbd": element})
        elif self.STATUSES()[self.location["status"]]["type"] == "dynamic actions":
            self.buttons = self.dynamic_buttons()
        else:
            self.buttons = []
            for element in self.LOCATIONS()[self.location["location"]]["actions"]:
                self.buttons.append({"text": self.t(element), "cbd": element})
        if self.location["location"] != "Inventory":
            self.buttons.append({"text": self.t("Inventory"), "cbd": "Inventory"})

    def update_image(self) -> str:
        return f"../game_data/images/locations/{self.LOCATIONS()[self.location['location']]['image']}"

    def add_to_inventory(self, item_name: str, count: int):
        if item_name not in self.inventory.keys():
            self.inventory[item_name] = 0
        self.inventory[item_name] += count

    def remove_from_inventory(self, item_name: str, count: int) -> bool:
        if item_name not in self.inventory.keys():
            return False
        self.inventory[item_name] -= count
        if self.inventory[item_name] < 0:
            self.inventory[item_name] += count
            return False
        if self.inventory[item_name] == 0:
            del self.inventory[item_name]
        return True

    def action_language(self, language: str) -> str:
        self.language = language
        return self.t("You changed language to") + f" {self.language}"

    def check_location(self, location: dict) -> bool:
        return location == self.location

    def action_movement(self, action: str) -> str:
        if action == "Leave":
            self.location = self.previous_locations.pop(-1)
            return self.t(self.ACTIONS()[action]["description"])
        if self.check_location(self.ACTIONS()[action]["location_arrive"]):
            return self.t("You are already here or you can't go there")
        self.previous_locations.append(self.location)
        self.location = self.ACTIONS()[action]["location_arrive"]
        while len(self.previous_locations) > 25:
            self.previous_locations.pop(0)
        return self.t(self.ACTIONS()[action]["description"])

    def except_new_enemy(self, enemy_name: str):
        if enemy_name not in self.enemies.keys():
            self.enemies[enemy_name] = self.NPC()[enemy_name]

    def get_drop_from_enemy(self, enemy_name: str) -> str:
        self.experience += self.enemies[enemy_name]["experience"]
        drop = random.choice(self.enemies[enemy_name]["drop"])
        self.add_to_inventory(drop, 1)
        for quest in self.quests:
            if (self.quests[quest]["enemy"] == enemy_name) and self.QUESTS()[quest]["type"] == "kill":
                self.quests[quest]["progres"] += 1
        return drop

    def beat_enemy(self, enemy_name: str) -> str:
        self.enemies[enemy_name]["hp"] -= self.damage()
        if self.enemies[enemy_name]["hp"] <= 0:
            drop = self.get_drop_from_enemy(enemy_name)
            del self.enemies[enemy_name]
            return f"{self.t('You killed')}: {self.t(enemy_name)}. " \
                   f"{self.t('You have gained')}:\n" \
                   f"{self.t('experience')}: {self.NPC()[enemy_name]['experience']}\n" \
                   f"{self.t(drop)}"
        return f"{self.t('You attacked')}: {self.t(enemy_name)}\n" \
               f"{self.t(enemy_name)}: hp - {self.enemies[enemy_name]['hp']}\n"

    def action_attack(self, action: str) -> str:
        self.except_new_enemy(self.ACTIONS()[action]["enemy_name"])
        answer = self.beat_enemy(self.ACTIONS()[action]["enemy_name"])
        return answer

    def action_sell(self, item_name: str) -> str:
        if item_name in self.inventory.keys():
            self.money += self.ITEMS()[item_name]["price"]
            if not self.remove_from_inventory(item_name, 1):
                return f"{self.t('You can not sold')}: {self.t(item_name)}"
            return f"{self.t('You sold')}: {self.t(item_name)}\nYour money: {self.money}cr"
        return f"{self.t('You have not got')}: {self.t(item_name)}"

    def action_buy(self, item_name: str) -> str:
        if item_name not in self.LOCATIONS()[self.location["location"]]["items"].keys():
            return f"{self.t('You can not buy')}: {self.t(item_name)}"
        if self.money < self.LOCATIONS()[self.location["location"]]["items"][item_name]:
            return f"{self.t('You can not buy')}: {self.t(item_name)}\n" \
                   f"Description: {self.t('You do not have enough money')}"
        self.money -= self.LOCATIONS()[self.location["location"]]["items"][item_name]
        self.add_to_inventory(item_name, 1)
        return f"{self.t('You bought')}: {self.t(item_name)}\nYour money: {self.money}cr"

    def action_info(self, item_name: str) -> str:
        if item_name not in self.inventory.keys():
            return f"{self.t('You have not got')}: {self.t(item_name)}"
        return self.t(self.ITEMS()[item_name]["description"])

    def equip_equipment(self, item_name: str) -> str:
        answer = ""
        if "equipment_cloths" in self.ITEMS()[item_name]["types"]:
            self.add_to_inventory(self.equipment["cloths"], 1)
            self.equipment["cloths"] = item_name
            answer += f"{self.t('You are wearing')}: {self.t(item_name)}"
        if "equipment_weapon" in self.ITEMS()[item_name]["types"]:
            self.add_to_inventory(self.equipment["weapon"], 1)
            self.equipment["weapon"] = item_name
            answer += f"{self.t('You have equipped')}: {self.t(item_name)}"
        if answer != "":
            self.remove_from_inventory(item_name, 1)
        else:
            answer += self.t("Unknown equipment type")
        return answer

    def action_equip(self, item_name: str) -> str:
        if item_name not in self.inventory.keys():
            return f"{self.t('You have not got')}: {self.t(item_name)}"
        return self.equip_equipment(item_name)

    def use_item(self, item_name: str) -> str:
        answer = ""
        if "hp_regeneration" in self.ITEMS()[item_name].keys():
            self.hp += self.ITEMS()[item_name]["hp_regeneration"]
            self.hp = min(self.hp, 100)
            answer += f"{self.t('You have replenished')}: {self.ITEMS()[item_name]['hp_regeneration']} hp"
        if answer != "":
            self.remove_from_inventory(item_name, 1)
        return answer

    def action_use(self, item_name: str) -> str:
        if item_name not in self.inventory.keys():
            return f"{self.t('You have not got')}: {self.t(item_name)}"
        return self.use_item(item_name)

    def constrain_damage(self, enemy_name: str) -> int:
        damage = self.enemies[enemy_name]["damage"]
        damage -= self.ITEMS()[self.equipment["cloths"]]["defence"]
        if damage <= 0:
            return 1
        return damage

    def get_enemies_damage(self) -> str:
        answer = ""
        for enemy_name in self.enemies:
            self.hp -= self.constrain_damage(enemy_name)
            answer += f"{self.t('You are being attacked by')}: {self.t(enemy_name)}\n" \
                      f"{self.t('You took damage')}: {self.constrain_damage(enemy_name)}\n" \
                      f"{self.t('Your hp')}: {self.hp}\n"
        return answer[:-1]

    def is_dead(self) -> bool:
        return self.hp <= 0

    def dead_script(self) -> str:
        self.location = {"location": "Forest", "status": "Stay"}
        self.previous_locations = []
        self.hp = 100
        self.experience = 0
        self.reputation = 0
        self.money = 0
        self.equipment = {"cloths": "Rags", "weapon": "Stick"}
        self.inventory = {}
        self.quests = {}
        self.enemies = {}
        return self.t("You are dead")

    def action_accepts_quest(self, quest: str) -> str:
        if quest in self.quests.keys():
            return self.t("You already accept this quest")
        self.quests[quest] = {"enemy": self.QUESTS()[quest]["enemy"], "goal": self.QUESTS()[quest]["goal"], "progres": 0}
        return f"{self.t('You accepted quest')}\n{self.t(self.QUESTS()[quest]['description'])}"

    def action_submits_quest(self, quest: str) -> str:
        if quest not in self.quests.keys():
            return self.t("You have not got this quest")
        if self.quests[quest]["progres"] >= self.quests[quest]["goal"]:
            self.experience += self.QUESTS()[quest]["reward"]["experience"]
            self.reputation += self.QUESTS()[quest]["reward"]["reputation"]
            self.money += self.QUESTS()[quest]["reward"]["money"]
            del self.quests[quest]
            return self.t("You submitted quest")
        return self.t("You do not complete quest")

    def perform_action(self, action: str) -> str:
        answer = ""
        if self.ACTIONS()[action]["type"] == "language":
            answer += self.action_language(action) + "\n"
        if self.ACTIONS()[action]["type"] == "movement":
            answer += self.action_movement(action) + "\n"
        if self.ACTIONS()[action]["type"] == "attack":
            answer += self.action_attack(action) + "\n"
        if self.ACTIONS()[action]["type"] == "item" and self.location["status"] == "Sell":
            answer += self.action_sell(action) + "\n"
        if self.ACTIONS()[action]["type"] == "item" and self.location["status"] == "Buy":
            answer += self.action_buy(action) + "\n"
        if self.ACTIONS()[action]["type"] == "item" and self.location["status"] == "Read":
            answer += self.action_info(action) + "\n"
        if self.ACTIONS()[action]["type"] == "item" and self.location["status"] == "Equip":
            answer += self.action_equip(action) + "\n"
        if self.ACTIONS()[action]["type"] == "item" and self.location["status"] == "Use":
            answer += self.action_use(action) + "\n"
        if self.ACTIONS()[action]["type"] == "quest" and self.location["status"] == "Accepts quest":
            answer += self.action_accepts_quest(action) + "\n"
        if self.ACTIONS()[action]["type"] == "quest" and self.location["status"] == "Submits quest":
            answer += self.action_submits_quest(action) + "\n"
        answer += self.get_enemies_damage() + "\n"
        if self.is_dead():
            answer += self.dead_script()
        self.update_buttons()
        self.update_image()
        self.update_data()
        return answer
