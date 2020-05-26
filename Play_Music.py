import os
from tkinter.filedialog import askdirectory
import pygame
from tkinter import *
from random import *
root=Tk()
root.geometry("500x500")
l=[]
pygame.mixer.init()
#EXTRACT .MP3 FILE
def Import_Songs():
    path=askdirectory()
    os.chdir(path)
    for files in os.listdir(path):
        if files.endswith(".mp3"):
            l.append(files)
Import_Songs()
song_list=Listbox(root)
for i in l:
    song_list.insert(END,i)
song_list.pack()
index=-1

#DEFINE ALL PLAY OPTIONS
def Play_songs_inorder(event):
    global index
    index = (index + 1) % len(l)
    pygame.mixer.music.load(song_list.get(index))
    pygame.mixer.music.play()
    song_list.activate(index)
def Play_song_Randomly(event):
    i = randint(0,song_list.size()-1)
    pygame.mixer.music.load(song_list.get(i))
    pygame.mixer.music.play()
    song_list.activate(i)
    global index
    index=i+1
def Play_Selected(event):
    global index
    for i in song_list.curselection():
        pygame.mixer.music.load(song_list.get(i))
        pygame.mixer.music.play()
        index=i
def Play_Previous(event):
    global index
    if index==0:
        index=song_list.size()-1
    else:
        index-=1
    print(index)
    pygame.mixer.music.load(song_list.get(index))
    pygame.mixer.music.play()

# ADD INTO PLAYLIST
def Add_to_PlayList(event):
    s=""
    for i in song_list.curselection():
        s += song_list.get(i)+","
    if s == "":
        return
    playlist=Listbox(root)
    playlist.insert(0,"Add to Playlist")
    playlist.place(height=20,x=song_list.winfo_x()+event.x,y=song_list.winfo_y()+event.y)
    def Add(event):
        f=open("playlist.txt","r")
        str=f.read().split(",")
        print(str)
        if s in str:
            playlist.destroy()
            return
        f.close()
        f=open("playlist.txt","a")
        f.write(s)
        f.close()
        playlist.destroy()
    playlist.bind("<Double-1>",Add)

#DISPLAY SONGS
def My_Playlist(event):
    f=open("playlist.txt","r")
    str=f.read().split(",")
    song_list.delete(0,song_list.size()-1)
    for s in str:
        if s is not "":
            song_list.insert(END,s)
    global index
    index=-1
def All_Songs(event):
    song_list.delete(0,song_list.size()-1)
    for i in l:
        song_list.insert(END,i)
#MANAGE VOLUME
def Volume_Up(event):
    if(pygame.mixer.music.get_volume()==0):
        pygame.mixer.music.set_volume(1/10)
        return
    x=pygame.mixer.music.get_volume()*(11/10)
    if x>1:
        return
    else:
        pygame.mixer.music.set_volume(x)
def Volume_Down(event):
    x=pygame.mixer.music.get_volume()*(9/10)
    if x<0:
        return
    else:
        pygame.mixer.music.set_volume(x)
# PLAYING OPTIONS
def Pause(event):
    print(pygame.mixer.music.get_pos(),pygame.mixer.music._MUSIC_POINTER)
    pygame.mixer.music.pause()
def UnPause(event):
    pygame.mixer.music.unpause()
def Stop(event):
    global index
    index=0
    print(event.char,end=",")
    pygame.mixer.music.stop()
def p(event):
    print(event.char,end=",")
#INITIALIZE ALL BUTTONS
in_order=Button(root,text="Next")
in_order.pack()
shuffle=Button(root,text="Shuffle Play")
shuffle.pack()
pause=Button(root,text="Pause")
pause.pack()
unpause=Button(root,text="UnPause")
unpause.pack()
stop=Button(root,text="Stop")
stop.pack()
playlist=Button(root,text="My Playlist")
playlist.pack()
all_songs=Button(root,text="All Songs")
all_songs.pack()
pre=Button(root,text="Previous")
pre.pack()
volume_up=Button(root,text="^",height=5,width=5)
volume_up.pack()
volume_down=Button(root,text="v",height=5,width=5)
volume_down.pack()
#BIND ALL BUTTONS
in_order.bind("<Button-1>",Play_songs_inorder)
shuffle.bind("<Button-1>",Play_song_Randomly)
pre.bind("<Button-1>",Play_Previous)
song_list.bind("<Double-1>",Play_Selected)
pause.bind("<Button-1>",Pause)
unpause.bind("<Button-1>",UnPause)
#root.bind("<FocusIn>",Stop)
stop.bind("<Button-1>",Stop)
song_list.bind("<Button-3>",Add_to_PlayList)
playlist.bind("<Button-1>",My_Playlist)
all_songs.bind("<Button-1>",All_Songs)
volume_up.bind("<Button-1>",Volume_Up)
volume_down.bind("<Button-1>",Volume_Down)
root.mainloop()