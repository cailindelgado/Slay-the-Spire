from a2_game import *
import tkinter as tk 
from PIL import ImageTk


#NOTE colours
royal_purple = "#7851a9"

def player_choice_screen():
    #setting background colour
    tk.Label(frame1, 
             text = "What would you like to play as?", 
             bg = royal_purple,
             fg = "black",
             font=("TKMenuFont", 14), 
             ).pack()
    
    tk.Button(
        frame1, 
        text="Silent",
        font=20,
        bg="#6951a9",
        fg="white",
        cursor="hand2",
        activebackground="#9272bb",
        activeforeground="#9272bb",
        command= lambda:selected_silence()).pack(padx=10, pady=10)
    
    tk.Button(
        frame1, 
        text="IronClad",
        font=20,
        bg="#9272bb",
        fg="white",
        cursor="hand2",
        activebackground="#9272bb",
        activeforeground="#9272bb",
        command=lambda:selected_ironclad()).pack(padx=10, pady=10)

#NOTE game screen, will display the 3 game options
def game_choice():
    #is the creator for the game.
    pass

#NOTE display monster/s
def monster_display():
    pass

#NOTE display character
def player_display():
    pass

#NOTE display encounter.
def encounter_display():
    pass

#initialize the app
root = tk.Tk()
root.title("Slay The Spire")

#Add in frame readjusters
root.geometry('500x600') #NOTE change to be the appropriate width and height 
                #width x height
# root.eval("tk::PlaceWindow . center")


#frames
frame1 = tk.Frame(root, bg=royal_purple)

frame2 = tk.Frame(root, bg= royal_purple)

#pack heierarchy
frame1.pack(fill='both', expand= True)
frame2.pack()


player_choice_screen()

root.mainloop()
