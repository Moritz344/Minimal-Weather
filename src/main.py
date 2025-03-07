from customtkinter import *
from cities import *
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
        window.geometry("1280x700")
        window.iconbitmap("assets/icon.ico")

        window.configure(fg_color=RAISIN_BLACK)
        

        window.minsize(1280,700)
        window.maxsize(1280,700)

        self.city = "City "
        self.country = ""
        self.wetter_desc = ""
        self.temp_celsius = "0°"
        self.temp_feel = "0°"
        self.temp_max = None
        self.temp_min = None
        self.wetter = None
        self.pressure = "0 hPa" 
        self.visibility = "0 km"
        self.humidity = "0°"
        self.clouds = "0 %"

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
        self.entry.place(x=1000,y=40)


        self.button_img = ctk.CTkImage(dark_image=Image.open("assets/button_img.png"),size=(30,30))

        self.button = ctk.CTkButton(window,text="",image=self.button_img,command=self.get_entry_info,
        width=10,
        height=40,
        hover_color=PLATINUM,
        fg_color="White")
        self.button.place(x=1210,y=40)
        
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
            self.temp_feel = "0°"
            self.humidity = "0°"
            self.clouds = "0 %"
            self.pressure = "0 hPa"
            self.visibility = "0 km"
            
            # aktualisiere den error wert
            self.temp_label.configure(text=f"{self.temp_celsius}")
            self.humidity_label.configure(text=f"{self.humidity}")
            self.temp_feel_label.configure(text=f"{self.temp_feel}")
            self.city_label.configure(text=f"{self.city}")
            self.vis_label.configure(text=f"{self.visibility}")
            self.pressure_label.configure(text=f"{self.pressure}")
            self.clouds_label.configure(text=f"{self.clouds}")



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
            self.humidity = self.data["main"]["humidity"]
            self.country = self.data["sys"]["country"]
            self.wetter_desc = self.data["weather"][0]["description"]
            self.visibility = self.data["visibility"]
            self.visibility = self.visibility / 1000
            self.clouds = self.data["clouds"]["all"]
            self.pressure = self.data["main"]["pressure"]

            
            self.temp_celsius = round(self.temp - 273.15,2)
            self.temp_feel = round(self.temp_feel - 273.15,2)
            self.temp_max = round(self.temp_max - 273.15,2)
            self.temp_min = round(self.temp_min - 273.15,2)
            self.update_label()
            

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
            self.clouds_label.configure(text=f"{self.clouds} %")

            self.temp_feel_label.configure(text=f"{self.temp_feel}°")
            self.humidity_label.configure(text=f"{self.humidity}°")
            self.country_label.configure(text=f"{self.country}")
            self.vis_label.configure(text=f"{self.visibility} km")
            self.pressure_label.configure(text=f"{self.pressure} hPa")

        except Exception as e:
            print(e)

    def tempetaure_block(self,window):
        self.temp_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="white",#"#0d0d0d",
        border_width=1,

        border_color="white")
        self.temp_frame.place(x=50,y=200)

        self.country_label = ctk.CTkLabel(self.temp_frame,
        text=f"{self.country}",
        text_color=BLACK,
        font=("opensans",20))

        self.country_label.place(x=10,y=30)

        self.temp_label = ctk.CTkLabel(self.temp_frame,
        text=f"{self.temp_celsius}",
        text_color=BLACK,
        font=("opensans",50,"bold"),
        width=len(self.temp_celsius)
        )
        self.temp_label.place(x=46,y=60)

        self.city_label = ctk.CTkLabel(self.temp_frame,
        text=f"{self.city}",
        text_color=BLACK,
        font=("opensans",20),
        )
        self.city_label.place(x=10,y=5)


        self.wetter_label = ctk.CTkLabel(self.temp_frame,
        text=f"{self.wetter}",
        text_color=BLACK,
        font=("opensans",20),
        )

        self.wetter_label.place(x=10,y=150)
        try:
            self.wetter_icon = ctk.CTkImage(dark_image=Image.open(f"assets/{self.wetter}.png"),size=(30,30))
            self.wetter_icon_label = ctk.CTkLabel(self.temp_frame,text="",image=self.wetter_icon) 
            self.wetter_icon_label.place(x=10,y=120)
        except Exception:
            print("Passendes Wetter icon nicht gefunden.")

    def feels_like_block(self,window):
        self.feels_like_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="white",
        border_width=1,
        border_color="white")
        self.feels_like_frame.place(x=300,y=200)

        self.temp_feel_text = ctk.CTkLabel(self.feels_like_frame,
        text=("Feels like"),
        text_color="black",
        font=("opensans",20,))
        self.temp_feel_text.place(x=45,y=8)

        self.temp_feel_label = ctk.CTkLabel(self.feels_like_frame,
        text=f"{self.temp_feel}",
        text_color=BLACK,
        width=190,
        height=len(self.temp_feel),
        font=("opensans",30,"bold"),
        )

        self.temp_feel_icon = ctk.CTkImage(dark_image=Image.open("assets/temp-hoch.png"),size=(30,30))
        self.temp_feel_icon_label = ctk.CTkLabel(self.feels_like_frame,
        text="",image=self.temp_feel_icon)
        
        self.temp_feel_icon_label.place(x=5,y=5)
        self.temp_feel_label.place(x=8,y=80)

    def humidity_block(self,window):

        self.humidity_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="white",
        border_width=1,
        border_color="white")
        self.humidity_frame.place(x=550,y=200)

        self.humidity_label = ctk.CTkLabel(self.humidity_frame,
        text=f"{self.humidity}",
        text_color=BLACK,
        width=190,
        height=50,
        font=("opensans",30,"bold"))
        self.humidity_icon = ctk.CTkImage(dark_image=Image.open("assets/humidity.png"),size=(30,30))

        self.humidity_text = ctk.CTkLabel(self.humidity_frame,
        text=f"Humidity",
        text_color="black",
        font=("opensans",20))
        self.humidity_text.place(x=50,y=7)

        self.humidity_icon_label = ctk.CTkLabel(self.humidity_frame,
        text="",image=self.humidity_icon)
        self.humidity_icon_label.place(x=5,y=5)

        self.humidity_label.place(x=5,y=65)
    
    def visibility_block(self,window):
        self.vis_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="white",
        border_width=1,
        border_color="white")
        self.vis_frame.place(x=50,y=430)

        self.vis_label = ctk.CTkLabel(self.vis_frame,
        text=f"{self.visibility}",
        width=180,
        text_color=BLACK,
        height=50,
        font=("opensans",30,"bold"))
        self.vis_label.place(x=5,y=70)

        self.vis_icon = ctk.CTkImage(dark_image=Image.open("assets/eye.png"))
        self.vis_icon_label = ctk.CTkLabel(self.vis_frame,text="",image=self.vis_icon)
        self.vis_icon_label.place(x=10,y=10)


        self.vis_text = ctk.CTkLabel(self.vis_frame,
        text="Visibility",
        text_color=BLACK,
        font=("opensans",20,),)
        self.vis_text.place(x=40,y=10)

    def pressure_block(self,window):


        self.pressure_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="white",
        border_width=1,
        border_color="white")
        self.pressure_frame.place(x=300,y=430)

        self.pressure_text = ctk.CTkLabel(self.pressure_frame,
        text="Pressure",
        text_color=BLACK,
        font=("opensans",20,),)
        self.pressure_text.place(x=40,y=10)

        self.pressure_icon = ctk.CTkImage(dark_image=Image.open("assets/speed.png"))
        self.pressure_icon_label = ctk.CTkLabel(self.pressure_frame,text="",image=self.pressure_icon,)
        self.pressure_icon_label.place(x=10,y=10)

        
        self.pressure_label = ctk.CTkLabel(self.pressure_frame,
        text=f"{self.pressure}",
        width=190,
        height=50,
        text_color=BLACK,
        font=("opensans",30,"bold"),)
        
        self.pressure_label.place(x=5,y=70)


    def clouds_block(self,window):
        self.clouds_frame = ctk.CTkFrame(window,
        height=200,
        width=200,
        corner_radius=10,
        fg_color="white",
        border_width=1,
        border_color="white")
        self.clouds_frame.place(x=550,y=430)

        self.clouds_text = ctk.CTkLabel(self.clouds_frame,
        text="Clouds",
        text_color=BLACK,
        font=("opensans",20,),)
        self.clouds_text.place(x=40,y=10)

        self.clouds_icon = ctk.CTkImage(dark_image=Image.open("assets/Clouds.png"))
        self.clouds_icon_label= ctk.CTkLabel(self.clouds_frame,text="",image=self.clouds_icon,)
        self.clouds_icon_label.place(x=10,y=10)

        self.clouds_label = ctk.CTkLabel(self.clouds_frame,
        text=f"{self.clouds}",
        width=190,
        height=50,
        text_color=BLACK,
        font=("opensans",30,"bold"),)
        
        self.clouds_label.place(x=5,y=70)

    def list_of_cities(self,window):
        self.city_frame = ctk.CTkFrame(window,
        width=400,
        height=430,
        fg_color=RAISIN_BLACK
        )
        

        city_template(self.city_frame,"New York",100,30,50,10)
        city_template(self.city_frame,"Tokyo",100,110,50,10)
        city_template(self.city_frame,"Sydney",100,190,50,10)
        city_template(self.city_frame,"Shanghai",100,270,50,10)
        city_template(self.city_frame,"Berlin",100,350,50,10)

        self.text = ctk.CTkLabel(window,text="Other Large Cities: ",font=("opensans",20))
        self.text.place(x=950,y=170)

        self.city_frame.place(x=850,y=200)


    def show_data(self,window):
        
        self.tempetaure_block(window)
        self.feels_like_block(window)
        self.humidity_block(window)
        self.visibility_block(window)
        self.list_of_cities(window)
        self.pressure_block(window)
        self.clouds_block(window)

    
        


App()
