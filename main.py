import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import requests
import matplotlib.ticker as ticker
import json
from dotenv import load_dotenv
import os

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

season_string = ""

inputdata = dict()
inputdata["Teams"] = list()
inputdata["Result"] = list()
inputdata["Win-Loss"] = list()


def fetchStandingData(year: str):
    response = requests.get("https://api-nba-v1.p.rapidapi.com/standings?league=standard&season=" + year,
                            headers={
                                "X-RapidAPI-Host": RAPIDAPI_HOST,
                                "X-RapidAPI-Key": RAPIDAPI_KEY
                            },
                            timeout=15
                            )

    if response.status_code == 200:
        return response.json()
    else:
        return None


# print(fetchStandingData("2022")["response"])


def fetchTeamNames(teamId: str):
    response = requests.get("https://api-nba-v1.p.rapidapi.com/teams?id=" + teamId,
                            headers={
                                "X-RapidAPI-Host": RAPIDAPI_HOST,
                                "X-RapidAPI-Key": RAPIDAPI_KEY
                            },
                            timeout=15
                            )
    if response.status_code == 200:
        return response.json()["response"][0]["name"]
    else:
        return None


if __name__ == "__main__":

    try:
        while len(season_string) <= 2:
            season_string = input("Enter the NBA Season: ")

        response = fetchStandingData(season_string)

        if response:

            standings_data = response["response"]

            for team_data in standings_data:
                print(team_data)
                team_name = team_data["team"]["name"]

                inputdata["Teams"].append(team_name)
                inputdata["Result"].append("Win")
                inputdata["Win-Loss"].append(int(team_data["win"]["total"]))

                inputdata["Teams"].append(team_name)
                inputdata["Result"].append("Loss")
                inputdata["Win-Loss"].append(int(team_data["loss"]["total"]))

                print("Team: " + team_name)
                print("Wins: " + str(team_data["win"]["total"]))
                print("Loss: " + str(team_data["loss"]["total"]))
        df = pd.DataFrame(inputdata)
        sns.set(style="darkgrid")

        ax = sns.catplot(x="Teams", y="Win-Loss", hue="Result", data=df, kind="bar", height=4, aspect=2)

        plt.xticks(
            rotation=45,
            horizontalalignment='right',
            fontweight='light',
            fontsize='xx-small'
        )

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print("Error")
        print(e)
