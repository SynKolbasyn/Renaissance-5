import os


os.mkdir("../game_data/")
os.mkdir("../players_data/")
os.mkdir("../game_data/languages/")
os.mkdir("../game_data/resources/")
open("../game_data/languages/en.json", "x")
open("../game_data/resources/actions.json", "x")
open("../game_data/resources/items.json", "x")
open("../game_data/resources/locations.json", "x")
open("../game_data/resources/npc.json", "x")
open("../game_data/resources/quests.json", "x")
open("../game_data/resources/statuses.json", "x")
with open("../game_data/token", "w") as file:
    file.write(input("Enter bot token: "))
print("Project structure created. BUT YOU MUST FILL FILES BY DATA!!! WITHOUT DATA BOT WILL NOT WORK!!!")
