import os
from tkinter import *
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

# Creating a window
root = Toplevel

root = tk.ThemedTk()
root.get_themes

root.set_theme("radiance")
# Fonts - Arial (corresponds to Helvetica ), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana

# Styles - nprmal ,bold, roman, italic, underline and overstrike.
# fg = red is used for font color
# bg = red is used for background color
# relief = border decoration (default:Flat, SUNKEN,RAISED,GROOVE AND RIDGE)
# anchor = how information in the widget is psitioned to the inner margin

statusbar = ttk.Label(root, text='Welcome to melody', relief=SUNKEN, anchor=N, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

#.pack is is used to organize widgets in blocks before placing them in the parent widget
#fill - default: NONE and X,Y,BOTH - determines whether wiget fills any extra space allocated to it by the packer or keeps it's own minimal dimeension

# for wave files
#     def show_details():
#
#         filelabel['text'] = 'Playing music' + ' ' + os.path.basename(filename)
#
#         a = mixer.sound(filename)
#         total_length = a.get_length
#         # dividing total_length by 60 and % by 60
#         mins, secs = divmod(total_length, 60)
#         mins = round(mins)
#         secs = round(secs)
#         timeformat = '{:02d}:{02d}'.format(mins,secs)
#
#         filelabel['text'] = 'Total length' + ' ' + timeformat

# for mp file
''' mixer.sound file is unable to handle mp3 file as they are very big
    and mixer also doesn't have the functionality 
    pygame gives mixer the functionality to handle the mp3 files therefore using a paackage  neutagen'''


def show_details(play_song):
    '''file_label['text'] = 'Playing music' + ' ' + os.path.basename(filename)'''
    #play_song = ['C:/Users/parsh/Desktop/Parshav/Python Projects-20191127T064137Z-001/Python Projects/Melody/04 - Dekha Hazaro Dafaa - DownloadMing.SE.mp3']
    file_data = os.path.splitext(play_song) #('C:/Users/parsh/Desktop/Parshav/Python Projects-20191127T064137Z-001/Python Projects/Melody/04 - Dekha Hazaro Dafaa - DownloadMing.SE', '.mp3')
    if file_data[1] == '.mp3':
        audio = MP3(play_song) # gets the length and bitrate of an MP3 file.
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # dividing total_length by 60 and % by 60
    mins, secs = divmod(total_length, 60) # computes both division and modulus
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)

    length_label['text'] = 'Total length' + ' ' + time_format

    t1 = threading.Thread(target=start_count, args=(total_length,))
    # start_count(total_length)
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy - returns false when we press the stop button(music stop playing)
    current_time = 0
    #check if the music stream is playing - mixer.music.get_busy()
    while current_time <= t and mixer.music.get_busy():

        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            current_time_label['text'] = 'Current Time' + ' - ' + time_format
            time.sleep(1)  # Number of seconds for which the code is required to be stopped.
            current_time += 1


def play_music():
    global paused

    if paused:
        # if pause is true and then we press play button then music unpause
        mixer.music.unpause()
        statusbar['text'] = 'Music resume' # shows status
        paused = FALSE # update
    else:
        try:  # Execute the code below if the paused var is not initialised
            stop_music()  # stops the already playing music before switching on to new song
            time.sleep(1)  # make sure the player has a buffer time of 1 second to switch the music ---?
            # why it is 1 second bcoz in our threading we have declared the time as 1 sec therfore the next iteration of this loop stops the music and tis get_busy() returns a falseand it is a false value then the difference between the iteration is 1 sec
            selected_song = playlistbox.curselection()  # it gives us a tuple
            selected_song = int(selected_song[0])  # it gives us the integer value
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            print("This play btn works ")
            statusbar['text'] = 'Playing music' + ' ' + os.path.basename(play_it) # path = '/home/User/Documents'  givess  basename 'Documents'
            show_details(play_it)

        except NameError:
            tkinter.messagebox.showerror("file not found", 'Melody could not find the error')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'Music Stopped'


playlist = []


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename() # filedialog is a module with open and save dialog functions.
    # To open file: Dialog that requests selection of an existing file.
    add_to_playlist(filename_path)
    # print(filename)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    print(playlist)
    index += 1


def about_us():
    tkinter.messagebox.showinfo('Our title', 'this is the info that we want')


paused = FALSE


def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = 'Music Paused'


def rewind_music():
    play_music()
    statusbar['text'] = 'Rewind Music'


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)  # as the set__volume function of python takes only thevalues from 0 to 1


# Creating a menu bar
menu_bar = Menu(root)  # initializing menu bar
# config To make an ordinary button look like it’s held down,
root.config(menu=menu_bar)  # it means make menu bar ready to receive the sub menu and to make it fix at the top

# Creating sub menu
subMenu = Menu(menu_bar, tearoff=0)  # initializing a sub menu
# Normally, a menu can be torn off, the first position (position 0) in the list of choices is occupied by the tear-off element, and the additional choices are added starting at position 1. If you set tearoff=0, the menu will not have a tear-off feature, and choices will be added starting at position 0.
menu_bar.add_cascade(label="File", menu=subMenu) # Creates a new hierarchical menu by associating a given menu to a parent menu
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)

subMenu = Menu(menu_bar)
menu_bar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

# initializing the mixer
mixer.init()

# to  give height and width f the video
root.geometry() # when we start te program then the size of display will be in accordance to all the contents of the s/w

root.title("Music Player")

'''It supports only .ico file so first need to convert png,jpeg file into ico file'''
root.iconbitmap(r'images/melody.ico')
# Under Windows, the DEFAULT parameter can be used to set the icon for the widget and any descendents that don't have an icon set explicitly. DEFAULT can be the relative path to a .ico file

''' whenever we want to add something inside our video we first add widget to it and then it is must to pack it
    Adding text '''

'''file_label = Label(root, text='Lets make Some Noise!')
# This label Function also act as a container that contains all of
# your stuff
file_label.pack()'''

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()
# Lb1 = Listbox(leftframe)
# # Lb1.insert(0, 'song1')
# # Lb1.insert(1, 'song2')
# Lb1.pack()

addbtn = ttk.Button(leftframe, text='+ Add', command=browse_file)
addbtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()  # it gives us a tuple
    # Returns a tuple containing the line numbers of the selected element or elements, counting from 0. If nothing is selected, returns an empty tuple.
    selected_song = int(selected_song[0])  # it gives us the integer value
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)  # if we use playlist.remove(it requires the name of the song to be deleted)
    print(playlist)


delbtn = ttk.Button(leftframe, text='- Del', command=del_song)
delbtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

length_label = ttk.Label(topframe, text='Total length - 00:00')
# This label Function also act as a container that contains all of
length_label.pack(pady=5)

current_time_label = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
current_time_label.pack()

# Pack layout Manager//Less Complexity of buttons with increasing complexity we move to grid layout manager
# relief = RAISED, borderwidth = 1
middleframe = Frame(rightframe)
middleframe.pack(pady=40)

'''Adding Image'''
photo = PhotoImage(file='images/playsongbutton.png')  # Adding image and it's path
'''labelphoto = Label(root,image = photo)#it is necessary to mention that the object you are entering is of what type bcoz the deafult mode is string
labelphoto.pack()'''
# creating a button
# instead of image we can also write text = 'sfgsdhig' to work
play_music_btn = ttk.Button(middleframe, image=photo, command=play_music)
play_music_btn.grid(row=0, column=0, padx=10)
# play_music_btn.pack(side=LEFT, padx=10)


stopPhoto = PhotoImage(file='images/stop.png')
stop_music_btn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stop_music_btn.grid(row=0, column=1, padx=10)
# stop_music_btn.pack(side=LEFT, padx=10)

pausePhoto = PhotoImage(file='images/Pause.png')
pause_music_btn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
# pause_music_btn.pack(side=LEFT, padx=10)
pause_music_btn.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

# Music volume controller
scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # set the volume default value
mixer.music.set_volume(0.70)
scale.grid(row=0, column=2, pady=15, padx=30)

rewindPhoto = PhotoImage(file='images/rewind.png')
rewind_music_btn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewind_music_btn.grid(row=0, column=0, padx=10)

mutePhoto = PhotoImage(file="images/mute.png")
volumePhoto = PhotoImage(file='images/Volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1, padx=10)


def on_closing():
    # tkinter.messagebox.showinfo('Prank', 'you have been pranked this window wont close')
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
# whenever we watch a video a video has got number of f that changes at frequency of ms
# # so here also the window which we see is changing / getting refreshed very fast thramesat is undetectable by our eye
# infinite loop makes the frame stay stable
root.mainloop()
