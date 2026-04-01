import requests
import time
import json
import urllib3
from requests.auth import HTTPBasicAuth
from stats_scraper import get_winrate


urllib3.disable_warnings()


with open(r"C:\Riot Games\League of Legends\lockfile", "r", encoding="utf-8") as f:
    read_data = f.read()
    lockfile_data = read_data.split(":")

    port = lockfile_data[2]
    password = lockfile_data[3]

    basic = HTTPBasicAuth("riot", password)

    print(f"Porta isolada: {port} | Senha isolada: {password}")

team_memory = {}

versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
j_versions = versions.json()
latest_versions = j_versions[0]

champions = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_versions}/data/pt_BR/champion.json")
heroes = champions.json()

riot_data = heroes["data"]

heroes_table = {}   

for hero in riot_data.values():
    hero_id = hero["key"]
    hero_name = hero["name"]

    heroes_table[hero_id] = hero_name

while True:

    r = requests.get(
        f"https://127.0.0.1:{port}/lol-champ-select/v1/session",
        verify=False,
        auth=basic,
    )

    if r.status_code == 404:
        print("👀 Aguardando Tela de Seleção...")

    elif r.status_code == 200:
        lobby_data = r.json()

        my_team = lobby_data["myTeam"]

        for player in my_team:
            current_pick = player["championPickIntent"]
            locked_pick = player["championId"]
            player_name = player["gameName"]
            player_tag = player["tagLine"]

            if player_name == "":
                player_name = player["cellId"]
                
            if player_name not in team_memory:
                
                if isinstance(player_name, int) or str(player_name).isdigit():
                    current_winrate = "Hidden"
                else:
                    try:
                        e = get_winrate(player_name, player_tag)
                        current_winrate = e[2]
                    except:
                        current_winrate = "Error when searching"
                        
                team_memory[player_name] = {
                    "champion": current_pick,
                    "winrate": current_winrate
                }
                

            previous_pick = team_memory[player_name]["champion"]
    

            if locked_pick != 0:
                current_pick = locked_pick

            if current_pick == 0:
                translated_name = "None"
            else:
                translated_name = heroes_table.get(str(current_pick), "Unknown Hero")

            if current_pick != previous_pick:
                print(
                    f"Player: {player_name} | ID: {translated_name} | "
                    f"Gen. WR: {team_memory[player_name]['winrate']}%"
                )
            team_memory[player_name]["champion"] = current_pick

        with open("champ_select.json", "w", encoding="utf-8") as f:
            json.dump(lobby_data, f, indent=4)

    time.sleep(3)
