import os
import download_game_data


os.mkdir("../game_data/")
os.mkdir("../players_data/")
os.mkdir("../game_data/images/")
os.mkdir("../game_data/languages/")
os.mkdir("../game_data/resources/")
os.mkdir("../game_data/images/locations/")
open("../game_data/languages/en.json", "x").close()
open("../game_data/resources/actions.json", "x").close()
open("../game_data/resources/items.json", "x").close()
open("../game_data/resources/locations.json", "x").close()
open("../game_data/resources/npc.json", "x").close()
open("../game_data/resources/quests.json", "x").close()
open("../game_data/resources/statuses.json", "x").close()
with open("../game_data/token", "w") as file:
    file.write(input("Enter bot token: "))
os.system("pip install -r requirements.txt")
print("Project structure created. BUT YOU MUST FILL FILES BY DATA!!! WITHOUT DATA BOT WILL NOT WORK!!!")
if input("Do you have access to original game data?[Y/n]: ").strip().lower() in ("y", "yes"):
    download_game_data.main()
