from kivy.config import Config

# Set window size to approximate a phone screen
Config.set('graphics', 'width', '360')   # width in pixels
Config.set('graphics', 'height', '640')  # height in pixels

# Optional: disable resizing for a more phone-like feel
Config.set('graphics', 'resizable', False)

#relevant imports
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from database import follow_list, add_show, remove_show
from tvmaze_test import search_shows, get_next_episode, get_last_episode
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.factory import Factory
from datetime import datetime

#Label that allows for interactive text element
class ClickableLabel(ButtonBehavior, Label):
    pass

# defining the main search screen of the app
class SearchScreen(Screen):
    
    # triggered when user presses search button, searches api and displays matching shows
    def on_search_button(self):
        query = self.ids.search_input.text.strip()
        if not query:
            return
        
        self.ids.results_box.clear_widgets()

        results = search_shows(query)
        for show in results:
            poster_url = show['image'] if show['image'] else ""
            row = SearchResultRow(
                title=show['name'],
                poster= poster_url,
                button_text = "Add"
            )

            row.on_button_press = lambda s=show: self.add_to_shows(s)
            self.ids.results_box.add_widget(row)

    # adds the selected show to the user's followed list
    def add_to_shows(self,show):
        add_show(show)
        self.ids.search_input.text = ""

        print(f"Added {show['name']} to My Shows")

# reusable ui component (components of list of shows matching search)
class SearchResultRow(BoxLayout):
    title = StringProperty("")
    poster = StringProperty("")
    button_text = StringProperty("Add")

    def on_button_press(self):
        print(f"{self.button_text}: {self.title}")

# reusable UI component. Layout for followed shows list
class MyShowsRow(BoxLayout):
    poster = StringProperty("")
    title = StringProperty("")
    subtitle = StringProperty("")
    show_id = NumericProperty(0)
    screen = ObjectProperty(None)

# defines the screen that displays followed shows
class MyShowsScreen(Screen):
    
    #reloads list whenever this screen is entered
    def on_pre_enter(self):
        self.load_my_shows()

    # creates a row filled with show data
    def add_show_card(self, show):
        row = Factory.MyShowsRow(
            poster=show.get('image','default.jpg'),
            title=show['name'],
            show_id=show['id'],
            screen=self
        )

        self.ids.myshows_box.add_widget(row)

    # rebuilds UI list (clears current)
    def load_my_shows(self):
        self.ids.myshows_box.clear_widgets()

        shows = follow_list()
        for show in shows:
            self.add_show_card(show)

    # remove show from followed and reload the screen
    def remove_refresh(self, show_id):
        remove_show(show_id)
        self.load_my_shows()

    # displays upcoming or last episode information in a popup
    def show_episode_info(self, show_id, show_name):
        next_episode = get_next_episode(show_id)
        if next_episode:
            airstamp = next_episode['airstamp']
            dt = datetime.fromisoformat(airstamp)
            airdate_time = dt.strftime("%Y-%m-%d %H:%M")
            message = f"Next episode: {next_episode['name']}\n"\
                      f"Season {next_episode['season']} Episode {next_episode['number']}\n"\
                      f"Air date and time: {airdate_time}"
        else:
            last_episode = get_last_episode(show_id)
            message = f"Show completed\n"\
                      f"Last episode: {last_episode['name']}\n"\
                      f"Season {last_episode['season']} Episode {last_episode['number']}\n"\
                      f"Air date: {last_episode['airdate']}"
            
        popup = Popup(title=show_name, content=Label(text=message), size_hint = (0.8,0.5))
        popup.open()

#static screen displaying app information
class AboutScreen(Screen):
    pass

#root application class
class CatchUp(App):
    pass

if __name__ == "__main__":
    CatchUp().run()
