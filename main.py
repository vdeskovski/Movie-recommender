from bs4 import BeautifulSoup
import requests
from tkinter import *
from random import *
from PIL import Image, ImageTk
from tkinter import messagebox

WINDOW_BACKGROUND_COLOR = "#2B2E4A"
BTN_BACKGROUND_COLOR = "#E84545"
TITLE_FONT_COLOR = "#3282B8"
OTHER_FONT_COLOR = "#A6E3E9"
omdbApi_key = "YOUR API KEY HERE"


def display_image_from_url(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    temp_file = "temp_image.jpg"
    with open(temp_file, "wb") as f:
        f.write(response.content)

    image = Image.open(temp_file)

    tk_image = ImageTk.PhotoImage(image)

    global canvas
    canvas = Canvas(width=300, height=465, highlightthickness=0, bg=WINDOW_BACKGROUND_COLOR)
    canvas.create_image(150, 232, image=tk_image)
    canvas.grid(row=3, column=0)

    image.close()
    canvas.mainloop()


def get_movie_list():
    response = requests.get("https://www.empireonline.com/movies/features/best-movies-2/")
    page = response.text
    soup = BeautifulSoup(page, "html.parser")
    divs = soup.find_all("div", class_="jsx-1913936986")
    movies = []
    for div in divs:
        para = div.find_all("p")
        if len(para) >= 2:
            second = para[1].text
            movie = " ".join(second.split(" ")[4:])
            movies.append(movie)
        elif len(para) != 0 and len(para[0].text) > 2:
            for p in para:
                link = p.find_all("a")[2]
            movie = " ".join(link.text.split(" ")[4:])
            movies.append(movie)
    return movies


def get_request():
    movie_request_url = "http://www.omdbapi.com/"
    movie_request_param = {
        "apikey": omdbApi_key,
        "t": choice(movies)
    }
    response = requests.get(movie_request_url, params=movie_request_param)
    response.raise_for_status()
    data = response.json()
    title = data["Title"]
    year = data["Year"]
    rated = data["Rated"]
    runtime = data["Runtime"]
    genre = data["Genre"]
    director = data["Director"]
    plot = data["Plot"]
    poster = data["Poster"]
    metascore = data["Metascore"]  # int
    imdbRating = data["imdbRating"]  # float
    try:
        set_up_labels(title, year, rated, runtime, genre, director, plot, poster, metascore, imdbRating)
    except:
        messagebox.showinfo(title="No information", message=f"Unable to find information for movie: {title}")


def clear_labels():
    try:
        global lblTitle
        lblTitle.destroy()
        # global lblYear
        # lblYear.destroy()
        global lblRated
        lblRated.destroy()
        global lblRuntime
        lblRuntime.destroy()
        global lblGenre
        lblGenre.destroy()
        global lblDirector
        lblDirector.destroy()
        global lblMetascore
        lblMetascore.destroy()
        global lblImdb
        lblImdb.destroy()
        global canvas
        canvas.destroy()
    except:
        pass


def set_up_labels(title, year, rated, runtime, genre, director, plot, poster, metascore, imdbRating):
    clear_labels()
    global lblTitle
    lblTitle = Label(text=f"{title} ({year})", font=("Arial", 20, "bold"), bg=WINDOW_BACKGROUND_COLOR,
                     fg=TITLE_FONT_COLOR, wraplength=350)
    lblTitle.grid(row=1, column=0, padx=(0, 30))

    # global lblYear
    # lblYear = Label(text=f"Year: {year}", font=("Arial", 15), bg=WINDOW_BACKGROUND_COLOR, fg=OTHER_FONT_COLOR)
    # lblYear.grid(row=1, column=1)

    global lblRated
    lblRated = Label(text=f"Rated: {rated}", font=("Arial", 15), bg=WINDOW_BACKGROUND_COLOR, fg=OTHER_FONT_COLOR)
    lblRated.grid(row=2, column=1)

    global lblRuntime
    lblRuntime = Label(text=f"Runtime: {runtime}", font=("Arial", 15), bg=WINDOW_BACKGROUND_COLOR, fg=OTHER_FONT_COLOR)
    lblRuntime.grid(row=4, column=1)

    global lblGenre
    lblGenre = Label(text=f"Genre: {genre}", font=("Arial", 15), bg=WINDOW_BACKGROUND_COLOR, fg=OTHER_FONT_COLOR)
    lblGenre.grid(row=1, column=1)

    global lblDirector
    lblDirector = Label(text=f"Director(s): {director}", font=("Arial", 15), bg=WINDOW_BACKGROUND_COLOR,
                        fg=OTHER_FONT_COLOR)
    lblDirector.grid(row=2, column=0)

    # lblPlot = Label(text=f"Plot: {plot}")
    # lblPlot.grid(row=2, column=1)

    canvasP = Canvas(height=280, width=300, bg=WINDOW_BACKGROUND_COLOR, highlightthickness=0)
    plot_text = canvasP.create_text(150, 125, width=280,
                                    text=f"{plot}",
                                    font=("Arial", 15, "italic"), fill=OTHER_FONT_COLOR)
    canvasP.grid(row=3, column=1, padx=(20, 0))

    global lblMetascore
    lblMetascore = Label(text=f"Metascore: {metascore}", font=("Arial", 15), bg=WINDOW_BACKGROUND_COLOR,
                         fg=OTHER_FONT_COLOR)
    lblMetascore.grid(row=5, column=1)

    global lblImbd
    lblImbd = Label(text=f"Imdb rating: {imdbRating}", font=("Arial", 15), bg=WINDOW_BACKGROUND_COLOR,
                    fg=OTHER_FONT_COLOR)
    lblImbd.grid(row=6, column=1)

    display_image_from_url(poster)


movies = get_movie_list()
window = Tk()
window.title("Movie recommender")
window.config(padx=30, pady=30, bg=WINDOW_BACKGROUND_COLOR)
btnRecommend = Button(text="Recommend!", width=20, font=("Arial", 20, "italic"), command=get_request,
                      bg=BTN_BACKGROUND_COLOR, activebackground=BTN_BACKGROUND_COLOR)
btnRecommend.grid(row=0, column=0, pady=(0, 50), columnspan=2)

window.mainloop()
