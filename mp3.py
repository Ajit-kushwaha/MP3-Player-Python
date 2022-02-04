import tkinter
import tkinter.filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


window=tkinter.Tk()
window.title('mp3')
window.geometry('500x450')
#initialize pygame
pygame.mixer.init()


#create function for time
def play_time():
    if stopped:
        return
#get current time
    current_time=pygame.mixer.music.get_pos() / 1000
#convert song time to time format
    converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))

    song=playlist_box.get(tkinter.ACTIVE)
    song=f'E:/GALLERY/music/{song}.mp3'

    song_mut=MP3(song)
# get the lenght of song using mutagen
    global song_length
    song_length=song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    #song slider
    song_slider.config(to=song_length)
    # Check to see if song is over
    if int(song_slider.get()) == int(song_length):
        stop()
    elif paused:
    # Check to see if paused, if so then pass
        pass
    else:
#move slider along 1 second at a time
        next_time=int(song_slider.get())+1
        song_slider.config(to=song_length,value=next_time)
        # Convert Slider poition to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

        # Output slider
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')


#add current time to status bar
    if current_time >= 1:
        status_bar.config(text=f' Playing: {converted_current_time} of {converted_song_length}')
#create loop to check the time every seconds
    status_bar.after(1000,play_time)



#func to add one song
def add_song():
    song=tkinter.filedialog.askopenfilename(initialdir='E:\GALLERY\music',title="Choose one Song",filetypes=(("mp3 Files","*.mp3"),))
#to replace the folder loc
    song=song.replace('E:/GALLERY/music/', "")
    song=song.replace(".mp3","")  
    playlist_box.insert(tkinter.END, song)

#func to add many song
def add_manysongs():
    songs=tkinter.filedialog.askopenfilenames(initialdir='E:\GALLERY\music',title="Choose many Song",filetypes=(("mp3 Files","*.mp3"),))
    for song in songs:

#to replace the folder loc.
        song=song.replace('E:/GALLERY/music/', "")
        song=song.replace(".mp3","")  
        playlist_box.insert(tkinter.END, song)

#to delete song
def Delete_song():
        playlist_box.delete(tkinter.ANCHOR)
def Delete_all_songs():
        playlist_box.delete(0,tkinter.END)

#create play func
def play():
    global stopped
    stopped=False

    song=playlist_box.get(tkinter.ACTIVE)
    song=f'E:/GALLERY/music/{song}.mp3'

    #load songs with pygame mixer
    pygame.mixer.music.load(song)
    #play song with pygame mixer
    pygame.mixer.music.play()
#get song time
    play_time()


global stopped
#create stop function
def stop():
    #stop the music
    pygame.mixer.music.stop()
    #clear selected playlist bar
    playlist_box.selection_clear(tkinter.ACTIVE)

    status_bar.config(text='')

    song_slider.config(value=0)

    global stopped
    stopped=True
#create paused variable
global paused
paused=False

#create pause function
def pause(is_paused):
    global paused
    paused=is_paused

    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused=False
    else:
        #pause
        pygame.mixer.music.pause()
        paused=True
        

#create func to play next song
def next_song():
    # Reset Slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)
    #get current song number
    next_one=playlist_box.curselection()
    next_one=next_one[0] + 1
    #get the next song from playlist
    song=playlist_box.get(next_one)
    song=f'E:/GALLERY/music/{song}.mp3'
    #load the next music
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    #clear the active selection in playlist
    playlist_box.selection_clear(0,tkinter.END)
    playlist_box.activate(next_one)
    #uncheck the previous selection and check the next song
    playlist_box.selection_set(next_one,last=None)

def previous_song():
    # Reset Slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)
    #get current song number
    next_one=playlist_box.curselection()
    next_one=next_one[0] - 1
    #get the next song from playlist
    song=playlist_box.get(next_one)
    song=f'E:/GALLERY/music/{song}.mp3'
    #load the next music
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    #clear the active selection in playlist
    playlist_box.selection_clear(0,tkinter.END)
    playlist_box.activate(next_one)
    #uncheck the previous selection and check the next song
    playlist_box.selection_set(next_one,last=None)

#create volume func
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


#create slider fun
def slider(x):
    song=playlist_box.get(tkinter.ACTIVE)
    song=f'E:/GALLERY/music/{song}.mp3'

    #load songs with pygame mixer
    pygame.mixer.music.load(song)
    #play song with pygame mixer
    pygame.mixer.music.play(start=song_slider.get())
#create main frame
main_frame=tkinter.Frame(window)
main_frame.pack(pady=20)

#create volume slider frame
volume_frame=tkinter.LabelFrame(main_frame,text='volume')
volume_frame.grid(row=0,column=1,padx=30)

#create volume slider
volume_slider=ttk.Scale(volume_frame,from_=1,to=0,value=1,orient='vertical',length=125,command=volume)
volume_slider.pack(pady=10)


#create song slider
song_slider=ttk.Scale(main_frame,from_=1,to=100,length=360,command=slider)
song_slider.grid(row=2,column=0,pady=20)

#create playlist box
playlist_box=tkinter.Listbox(main_frame,bg="black",fg="green",width=60,selectbackground="black",selectforeground="white")
playlist_box.grid(row=0,column=0)

#create button frame
control_frame=tkinter.Frame(main_frame)
control_frame.grid(row=1,column=0,pady=20)

#btn images
back_img=tkinter.PhotoImage(file="E:/python/back50.png")
forward_img=tkinter.PhotoImage(file="E:/python/forward50 (1).png")
play_img=tkinter.PhotoImage(file="E:/python/play50.png")
pause_img=tkinter.PhotoImage(file="E:/python/pause50.png")
stop_img=tkinter.PhotoImage(file="E:/python/stop50.png")

#create play buttons
back_button=tkinter.Button(control_frame,image=back_img,borderwidth=0,command =previous_song)
forward_button=tkinter.Button(control_frame,image=forward_img,borderwidth=0,command=next_song)
play_button=tkinter.Button(control_frame,image=play_img,borderwidth=0,command=play)
pause_button=tkinter.Button(control_frame,image=pause_img,borderwidth=0,command=lambda: pause(paused))
stop_button=tkinter.Button(control_frame,image=stop_img,borderwidth=0,command=stop)

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

#create men
my_menu=tkinter.Menu(window)
window.config(menu=my_menu)

#create add song menu dropdown
add_song_menu=tkinter.Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Add songs",menu=add_song_menu)

#add one song commands
add_song_menu.add_command(label="Add one song",command=add_song)
#add many songs command
add_song_menu.add_command(label="Add many songs",command=add_manysongs)

#Create Delete Songs dropdown
remove_song_menu=tkinter.Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Delete Song",menu=remove_song_menu)

#delete one song command
remove_song_menu.add_command(label="Delete one song",command=Delete_song)
#delete many songs command
remove_song_menu.add_command(label="Delete All song",command=Delete_all_songs)


#status bar
status_bar=tkinter.Label(window,text='nothing',bd=2,relief="groove",anchor='e')
status_bar.pack(fill='x',side='bottom',ipady=5)


#temporary label
my_label=tkinter.Label(window,text=' ')
my_label.pack(pady=20)

window.mainloop()
