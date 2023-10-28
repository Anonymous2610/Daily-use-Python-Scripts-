from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium.webdriver.common.by import By
import requests



#Get ALL Song List from Sotify PlayList
def getSongList():
    # url = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF"
    url = input("Enter Playlist Link: ")

    #Web Driver
    driver = webdriver.Chrome()
    driver.get(url) 

    # add to so that website has enough time to load
    sleep(10)

    # get all of the current page's html
    page_html = driver.page_source
    page_source = bs(page_html, "html.parser")

    #Get all songs from the list
    print("Getting Songs from Playlist..................")
    try:
        # song_tables = page_source.find_all("div", attrs={data-testid="playlist-tracklist"})
        tracklist_div = page_source.find("div", attrs={"data-testid":"playlist-tracklist"})
        song_tables = tracklist_div.find_all("div",attrs={"class": "standalone-ellipsis-one-line"})
        albums_tables = tracklist_div.find_all("a", attrs={"class": "standalone-ellipsis-one-line"})
        songs = []
        # print(len(song_tables),len(albums_tables))
        if(len(song_tables)==len(albums_tables)):
            for song, album in zip(song_tables,albums_tables):
                # full name = 
                if song.text[0].isalpha():
                    full_song = song.text
                    full_song = full_song + " from " + album.text
                    songs.append(full_song)
        else: 
            for song in song_tables:
                if song.text[0].isalpha():
                    songs.append(song.text)
        return songs
    except:
        print("errror")



#----------------------------------------------------------------------

#Get all links from song list
def getYTLink(songs):
    links = []
    separator = "+"  
    print("Getting Song Links..............................")
    for song in songs:
        link = "https://www.youtube.com/results?search_query="
        query = '+'.join(song.split())
        link += query
        try :
            driver = webdriver.Chrome()
            driver.get(link) 
            page_html = driver.page_source
            page_source = bs(page_html, "html.parser")
            watch_link = list(page_source.find("a",attrs={"id":"video-title"},href=True))
            links.append(str(watch_link['href']))
        except :
            print(f"some error occured when getting link for {song}")
            continue
    return links
#----------------------------------------------------------------------
from pytube import YouTube
import os

def downloadMp3(string):
    yt = YouTube(string)

    video = yt.streams.filter(only_audio=True).first()

    out_file = video.download(output_path="./MY PLAYLIST")

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

#----------------------------------------------------------------------

#Main Function
if __name__ == "__main__":

    songs = getSongList()

    print(song for song in songs)

    links = getYTLink(songs)

    links = getYTLink(songs)

    print("Downloading songs...........................")
    for link in links:
        ytlink = "https://www.youtube.com/" + link[1:]
        downloadMp3(ytlink)
