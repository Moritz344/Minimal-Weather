from customtkinter import *
import customtkinter as ctk
from settings import *

def city_template(frame,name,xframe,yframe,x,y):
    text_frame_temp = ctk.CTkFrame(frame,
    width=200,height=50,
    fg_color="white",
    )

    text_frame_temp.place(x=xframe,y=yframe)

    text_temp = ctk.CTkLabel(text_frame_temp,text=f"{name}",
    font=("opensans",20),
    text_color="black")
    text_temp.place(x=x,y=y)


