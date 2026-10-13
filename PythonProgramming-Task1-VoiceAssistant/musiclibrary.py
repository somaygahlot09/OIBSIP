import random
import webbrowser

# Song name -> YouTube link
MUSIC = {
    "song": "https://www.youtube.com/watch?v=4DfVxVeqk2o",
    "save": "https://www.youtube.com/watch?v=QH-87ZXQ2pw",
    "daytona": "https://www.youtube.com/watch?v=XULDXoFU1hQ",
    "thing": "https://www.youtube.com/watch?v=p9Y2J02JYTA",
}


def get_music():
    """Return the dictionary of song names and links."""
    return MUSIC


def play_random():
    """Open a random song in the browser and return its name."""
    name, url = random.choice(list(MUSIC.items()))
    webbrowser.open(url)  # works on Windows, macOS and Linux
    return name
