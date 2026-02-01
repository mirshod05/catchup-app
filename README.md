# catchup-app
Mobile app created with python and kivy that allows you to see when the next episode of your favorite show is releasing. This app uses TVMaze API to fetch information about tv shows and new episodes.

## How it works:
When you run main.py, the app launches on the Search screen. From here, you can search for TV shows that are currently airing using the TVMaze API. After finding a show, click Add to include it in your list of tracked shows.

Using the bottom navigation bar, you can switch to the My Shows screen. This screen displays all the shows you are following. For each show, you can press the New Ep button to check for upcoming episodes. A popup will appear showing either the release date and time of the next episode or, if the show has ended, information about the last episode that aired. 

The app stores followed shows locally and creates a fresh database on first run. 

## Running on Mobile (Android)

This app can be run on an Android device using **Pydroid 3**.
For now, the app is not packaged as an APK, but it has been tested by running the Python source directly on Android via Pydroid.

Steps:
1. Install Pydroid 3 from the Play Store
2. Copy the project files to your device
3. Run `main.py` inside Pydroid

Future work includes packaging the app as a standalone Android APK
