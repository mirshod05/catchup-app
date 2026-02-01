import sqlite3
from datetime import datetime

conn = sqlite3.connect("tvmazedata.db")
cursor = conn.cursor()

#creates table to store shows in db file
cursor.execute("""
CREATE TABLE IF NOT EXISTS shows(
    id INTEGER PRIMARY KEY,
    name TEXT,
    image TEXT,
    next_episode TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders(
    show_id INTEGER PRIMARY KEY,
    remind_before INTEGER DEFAULT 60,
    notified INTEGER DEFAULT 0
)
""")

conn.commit()

# adds show to list
def add_show(show_dict):
    #add shows
    show_id = show_dict["id"]
    name = show_dict["name"]
    image = show_dict["image"]
    next_date = show_dict.get("next_airdate")

    cursor.execute("INSERT OR REPLACE INTO shows (id, name, image, next_episode) VALUES (?,?,?,?)", (show_id, name, image, next_date))
    conn.commit()
    
#remove show from list
def remove_show(show_id):
    cursor.execute("DELETE FROM shows WHERE id=?", (show_id,))
    conn.commit()

# return list of followed shows   
def follow_list():
    cursor.execute("SELECT id, name, image, next_episode FROM shows")
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append({
            "id":row[0],
            "name": row[1],
            "image": row[2],
            "next_episode": row[3]
        })

    return results
    
# if new episode, updates table
def update_next(show_id, next_ep_dict):
    next_airdate= next_ep_dict.get("airdate")
    cursor.execute("UPDATE shows SET next_episode = ? WHERE id = ?", (next_airdate, show_id))
    conn.commit()

# return show based on show_id
def get_show_by_id(show_id):
    cursor.execute("SELECT id FROM shows WHERE id=?", (show_id,))
    row = cursor.fetchone()
    return row

    
