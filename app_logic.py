from tvmaze_test import search_shows, get_next_episode
from database import add_show, remove_show, follow_list, update_next, get_show_by_id


"""
This file chooses which api function to call and cleans the data for the app.
tvmaze_test communicates with the api and returns raw data while this file acts as the decision
maker and decides which parts to return.
"""

def add_show_by_name(name):
    #search show using api
    results = search_shows(name)
    
    #handle no result
    if not results:
        return "Not found"

    #pick best match
    show = results[0]
    
    #check if already in database
    show_id = show['id']
    show_name = show['name']
    if get_show_by_id(show_id):
        return "already added"
   
    add_show(show) # add to list
    return "added"

def remove_show_by_id(show_id):
    if get_show_by_id(show_id):
        remove_show(show_id)
        return "removed"
    return "not found"

def get_all_shows():
    rows = follow_list()

    shows = []
    for row in rows:
        shows.append({"id":row['id'], "name":row['name'], "next_episode":row['next_episode']})

    return shows

def check_for_new_ep():
    shows = get_all_shows() #get all tracked shows
    new_episodes = []
    for show in shows:
        show_id = show['id']
        latest_ep = get_next_episode(show_id)
        
        if latest_ep is not None:
            latest_airdate = latest_ep.get('airdate')
            current_next = show.get('next_episode')
            
            #update
            
            if latest_airdate and (current_next is None or latest_airdate>current_next):
                update_next(show_id, latest_ep) #updates with latest ep

                new_episodes.append({"show":show['name'],
                                     "episode":latest_ep['name'],
                                     "airdate":latest_ep['airdate']})
    return new_episodes

