# Load csvs
import pandas as pd
import re as r
import random


ROCK = pd.read_csv("DataBase/ROCK.csv")
ROCK["Genre"] = "ROCK" 
ROCK["id"] = ROCK["id"].str.replace("ROCK","")

ELECTRONIC = pd.read_csv("DataBase/ELECTRONIC.csv")
ELECTRONIC["Genre"] = "ELECTRONIC" 
ELECTRONIC["id"] = ELECTRONIC["id"].str.replace("ELECTRONIC","")

POP = pd.read_csv("DataBase/POP.csv")
POP["Genre"] = "POP" 
POP["id"] = POP["id"].str.replace("POP","")

RAP = pd.read_csv("DataBase/RAP.csv")
RAP["Genre"] = "RAP" 
RAP["id"] = RAP["id"].str.replace("RAP","")

# Concatenar todos los DataFrame
SONGS_DB = pd.concat([ROCK, ELECTRONIC, POP, RAP])

SONGS_DB.drop("Unnamed: 0", axis=1, inplace=True)
SONGS_DB.drop("id",axis=1,inplace=True)

SONGS_DB["ID"] = range(1,len(SONGS_DB)+1)

currented_played = []
def recommend_song(path:str, genre:str):
    currented_played.append(path)
    randipity = random.randint(0,6)
    if randipity >=3:
        current_genre = SONGS_DB[SONGS_DB["Genre"]==genre].head(1).Genre.unique()[0]
        recommendation = SONGS_DB[~SONGS_DB["shortedPath"].isin(currented_played)]
        recommendation = recommendation[recommendation["Genre"]== current_genre].head(1).shortedPath.unique()[0]
    else:
        current_genre = SONGS_DB[SONGS_DB["Genre"]!=genre].head(1).Genre.unique()[0]
        recommendation = SONGS_DB[~SONGS_DB["shortedPath"].isin(currented_played)]
        recommendation = recommendation[recommendation["Genre"]== current_genre].head(1).shortedPath.unique()[0]
    
    recommendation = recommendation.split("/")
    
    return {"genre":recommendation[2], "artist":recommendation[3], "title":recommendation[4]}

### CHAT ###


### FASTAPI ###

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

# Create a route to serve the static files
app.mount("/static", StaticFiles(directory="Playlist"), name="static")
app.mount("/static2", StaticFiles(directory="Home_Page"), name="static2")
app.mount("/static3", StaticFiles(directory="Users"), name="static3")

templates = Jinja2Templates(directory="Playlist")

@app.get("/playlist/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def read_item(request: Request, genre: str, artist: str, title: str):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre}
    )

@app.get("/playlist2/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def get_next_song(request: Request, genre: str, artist: str, title:str):
    path = f"/tracks/{genre}/{artist}/{title}"
    if True:
        a = recommend_song(path,genre)
        genre = a["genre"]
        artist = a["artist"]
        title = a["title"]
        return templates.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "id": id}
    )
    return f"{genre}_song_1.mp3"

@app.get("/helloworld")
def greeting():
    return {"message": f"Hello World. Welcome to my first web app. Add /home to the URL to see the home page."}
    
@app.get("/home")
async def home():
    return FileResponse("Home_Page/index.html") 

@app.get("/")
async def user():
    return FileResponse("Users/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4444)

