import requests
from bs4 import BeautifulSoup

class SteamID:
    def __init__(self):
        self.steamID = None
        self.steamID3 = None
        self.steamID64 = None
        self.customURL = None
        self.profileState = None
        self.profileCreated = None
        self.name = None
        self.location = None
        self.status = None
        self.profile = None

    def fetch_data(self, steam_id="76561197960435530"):
        url = f"https://steamid.io/lookup/{steam_id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        data = soup.find_all("div", class_="col-md-8")[0]

        self.steamID = data.find_all("div")[0].text.strip()
        self.steamID3 = data.find_all("div")[1].text.strip()
        self.steamID64 = data.find_all("div")[2].text.strip()
        self.customURL = data.find_all("div")[3].text.strip()
        self.profileState = data.find_all("div")[4].text.strip()
        self.profileCreated = data.find_all("div")[5].text.strip()
        self.name = data.find_all("div")[6].text.strip()
        self.location = data.find_all("div")[7].text.strip()
        self.status = data.find_all("div")[8].text.strip()
        self.profile = data.find_all("div")[9].text.strip()

        return self

if __name__ == "__main__":
    steam_id = "76561197960435530"
    steam_id_data = SteamID().fetch_data(steam_id)

    print(steam_id_data.steamID)
    print(steam_id_data.steamID3)
    print(steam_id_data.steamID64)
    print(steam_id_data.customURL)
    print(steam_id_data.profileState)
    print(steam_id_data.profileCreated)
    print(steam_id_data.name)
    print(steam_id_data.location)
    print(steam_id_data.status)
    print(steam_id_data.profile)
