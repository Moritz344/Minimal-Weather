from customtkinter import *
import customtkinter as ctk
from tkinter import *
import json
import requests
import CTkMessagebox
from settings import *
from PIL import Image
from dotenv import load_dotenv


class App():
    def __init__(self):
    
        window = ctk.CTk()
        window.title("Weather App")
        window.geometry("800x600")
        ctk.set_appearance_mode("dark")
        window.minsize(800,600)
        window.maxsize(800,600)

        self.city = "City "
        self.temp_celsius = "0°"
        self.temp_feel = None
        self.temp_max = None
        self.temp_min = None
        self.wetter = None

        def no_focus_entry(event):
            # Verliert den Fokus auf das Entry feld wenn enter gedrückt wird
            # Dazu funktioniert die enter taste wie die Lupe
            self.entry.master.focus_set()
            self.get_entry_info()

        self.entry = ctk.CTkEntry(window,width=200,height=5,
        font=("opensans",30),
        fg_color=LIGHT_BLACK,
        state="normal",
        border_width=1,
        border_color="white",
        corner_radius=4,
        placeholder_text="Search city..")
        self.entry.place(x=540,y=40)


        self.button_img = ctk.CTkImage(dark_image=Image.open("assets/button_img.png"),size=(30,30))

        self.button = ctk.CTkButton(window,text="",image=self.button_img,command=self.get_entry_info,
        width=10,
        height=40,
        hover_color=PLATINUM,
        fg_color="White")
        self.button.place(x=750,y=40)
        
        self.show_data(window)
        
        window.bind("<Return>",no_focus_entry)

        window.mainloop()



    def get_entry_info(self):
        self.city = self.entry.get()
        self.update_label()
        self.entry.delete(0,ctk.END)
        self.get_weather_info()

    def error_values(self):
            self.city = "Invalid Input"
            self.temp_celsius = "0°"
            self.temp_label.configure(text=f"{self.temp_celsius}")
            self.city_label.configure(text=f"{self.city}")


    def get_weather_info(self,):
        load_dotenv("secret.env")
        self.api_key = os.getenv("API_KEY")
        self.url=f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}"
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            self.data = self.response.json()
            #print(self.data)

            self.wetter = self.data["weather"][0]["main"]
            self.temp = self.data["main"]["temp"]
            self.temp_feel = self.data["main"]["feels_like"]
            self.temp_min = self.data["main"]["temp_min"]
            self.temp_max = self.data["main"]["temp_max"]

            
            self.temp_celsius = round(self.temp - 273.15,2)
            self.temp_feel = round(self.temp_feel - 273.15,2)
            self.temp_max = round(self.temp_max - 273.15,2)
            self.temp_min = round(self.temp_min - 273.15,2)
            self.update_label()
            

            #print("Wetter:",self.wetter)
            #print("Temperatur:",self.temp_celsius)
            #print("Temperature feels like:",self.temp_feel)
            #print("Temperature minimum:",self.temp_min)
            #print("Temperature maximum:",self.temp_max)
        else:
            self.error_values()
            msg = CTkMessagebox.CTkMessagebox(message="Invalid Input",icon="warning",
            font=("opensans",30),
            title="Error")
            print("Wetter Daten konnten nicht aufgerufen werden!")

    def update_label(self):
        try:
            self.temp_label.configure(text=f"{self.temp_celsius}°")
            self.city_label.configure(text=f"{self.city}")
            self.wetter_label.configure(text=f"{self.wetter}")

            self.wetter_icon.configure(dark_image=Image.open(f"assets/{self.wetter}.png"))
            #self.temp_feel_label.configure(text=f"Temperature feels like: {self.temp_feel}°C")
            #self.temp_min_label.configure(text=f"Temperature minimum: {self.temp_min}°C")
            #self.temp_max_label.configure(text=f"Temperature maximum: {self.temp_max}°C")
        except Exception:
            print("Nur um sicher zu gehen.")

    def show_data(self,window):
        

        self.temp_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="#0d0d0d",
        border_width=1,
        border_color="white")
        self.temp_frame.place(x=50,y=200)

        self.temp_label = ctk.CTkLabel(self.temp_frame,
        text=f"{self.temp_celsius}",
        font=("opensans",50,"bold"),
        width=len(self.temp_celsius)
        )
        self.temp_label.place(x=46,y=60)

        self.city_label = ctk.CTkLabel(self.temp_frame,
        text=f"{self.city}",
        font=("opensans",20),
        )
        self.city_label.place(x=10,y=5)


        self.wetter_label = ctk.CTkLabel(self.temp_frame,
        text=f"{self.wetter}",
        font=("opensans",20),
        )

        self.wetter_label.place(x=10,y=150)
        try:
            self.wetter_icon = ctk.CTkImage(dark_image=Image.open(f"assets/{self.wetter}.png"),size=(30,30))
            self.wetter_icon_label = ctk.CTkLabel(self.temp_frame,text="",image=self.wetter_icon) 
            self.wetter_icon_label.place(x=10,y=120)
        except Exception:
            print("Passendes Wetter icon nicht gefunden.")

    
        self.feels_like_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="#0d0d0d",
        border_width=1,
        border_color="white")
        self.feels_like_frame.place(x=300,y=200)

        #self.temp_feel_label = ctk.CTkLabel(self.data_frame,
        #text=f"Temperature feels like: {self.temp_feel}",
        #font=("opensans",25),
        #)
        ##self.temp_feel_label.place(x=10,y=90)

        self.humidity_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="#0d0d0d",
        border_width=1,
        border_color="white")
        self.humidity_frame.place(x=550,y=200)
        
        self.other_frame = ctk.CTkFrame(window,
        height=150,
        width=700,
        corner_radius=10,
        fg_color="#0d0d0d",
        border_width=1,
        border_color="white")
        self.other_frame.place(x=50,y=430)

        #self.temp_max_label = ctk.CTkLabel(self.data_frame,
        #text=f"Temperature maximum: {self.temp_max}",
        #font=("opensans",25),
        #)
        ##self.temp_max_label.place(x=10,y=130)

        #self.temp_min_label = ctk.CTkLabel(self.data_frame,
        #text=f"Temperature minimum: {self.temp_min}",
        #font=("opensans",25),
        #)
        ##self.temp_min_label.place(x=10,y=170)


App()
