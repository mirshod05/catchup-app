import requests

BASE_URL = "https://api.tvmaze.com"

#search function, calls API and returns a dictionary of shows
def search_shows(query):
    '''
    This function will allow the user to search for a list of shows
    '''
    endpoint = "/search/shows"
    url = BASE_URL + endpoint
    params = {
        "q":query
        }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()  # Convert JSON response into Python dict
        results = []
        for item in data:
            show = item["show"]
            show_id = show['id']
            name = show['name']
            image = show["image"]["medium"] if show["image"] else None
            results.append({"id": show_id, "name": name, "image": image})

        return results

    else:
        print("Error fetching data:", response.status_code)
        return []

#api call to check for next episode
def get_next_episode(show_id):
    url = BASE_URL + f"/shows/{show_id}"
    params = {"embed":"nextepisode"}
    response = requests.get(url,params=params)

    if response.status_code==200:
        data = response.json()
        next_ep = data.get("_embedded", {}).get("nextepisode")

        if next_ep == None:
            return None
        else:
            return {
                "season": next_ep["season"],
                "number": next_ep["number"],
                "name": next_ep["name"],
                "airdate": next_ep["airdate"],
                "airstamp": next_ep["airstamp"]
                } 
            

    else:
        print("Error fetching data:", response.status_code)
        return None

# calls api to check for latest episode
def get_last_episode(show_id):
    url = BASE_URL + f"/shows/{show_id}/episodes"
    response = requests.get(url)
    if response.status_code ==200:
        episodes = response.json()
        last_ep = episodes[-1]

        if last_ep == None:
            return None
        else:
            return {
                "season": last_ep["season"],
                "number": last_ep["number"],
                "name": last_ep["name"],
                "airdate": last_ep["airdate"],
                "airstamp": last_ep["airstamp"]
                }
    else:
        print("Error fetching data:", response.status_code)
        return None
    
