from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.widget import Widget
from threading import Thread
import threading
from kivymd.color_definitions import colors
from kivy.clock import Clock
import time

class FirstScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        self.timer_boxlayout=MDBoxLayout(
            orientation = "horizontal",
            size_hint_y=None,
            height=40,
        )
    
        self.timer_textInput = TextInput(
            halign="center",
            readonly=True,
            size_hint=(140,None),
            font_size=40,
            size=(200,60),
            background_normal='',
            background_active='',
            background_color=(0,0,0,0)
        )
    
        self.timer_boxlayout.add_widget(Widget(height=100))# spacer
        self.timer_boxlayout.add_widget(self.timer_textInput)
        self.timer_boxlayout.add_widget(Widget(height=100))# spacer
        self.add_widget(self.timer_boxlayout)

        self.buttons_boxlayout = MDGridLayout(cols=8, spacing=10, padding=50, size_hint_y=None, height=50)
        
        self.start_button = MDRaisedButton(
            text="star",
            theme_text_color="Custom",
            # font_style='H6'
        )
        self.start_button.bind(on_release=self.start) 
        self.buttons_boxlayout.add_widget(self.start_button)

        self.pause_button = MDRaisedButton(
            text="pause",
            theme_text_color="Custom",
            # font_style='H6'
        )
        self.pause_button.bind(on_release=self.pause)
        self.buttons_boxlayout.add_widget(Widget())
        self.buttons_boxlayout.add_widget(self.pause_button)

        self.restart_button = MDRaisedButton(
            text="restar",
            theme_text_color="Custom",
            # font_style='H6'
        )
        self.restart_button.bind(on_release=self.restart) 
        self.buttons_boxlayout.add_widget(Widget())
        self.buttons_boxlayout.add_widget(self.restart_button)

        self.add_widget(self.buttons_boxlayout)

        self.spacer = MDBoxLayout(size_hint_y=None, height=100,orientation ="horizontal",spacing=10, padding=10)
        self.add_widget(self.spacer)


        self.scroll = MDScrollView()#to make tasks scroll
        self.laps = MDList()
        self.scroll.add_widget(self.laps)
        self.add_widget(self.scroll)

        self.replaceTime(f"{0:02}:{0:02}:{0:02}")

        self.cond = True

    

    def replaceTime(self,txt):
        self.timer_textInput.text = txt

    def start(self,instance):
        global thread
        thread = Thread(target=self.updateTime)
        thread.daemon = True
        thread.start()
        

    def pause(self,instance):
        self.cond = False
        thread.join()
        self.cond = True

    def restart(self,instance):
        self.cond = False
        thread.join()
        self.cond = True
        self.replaceTime(f"{0:02}:{0:02}:{0:02}")
    
    def updateTime(self):
        hours, minutes, seconds = self.getTime()
        while self.cond:
            Clock.schedule_once(lambda dt: self.replaceTime(f"{hours:02}:{minutes:02}:{seconds:02}"))
            time.sleep(1)
            seconds+=1
            if seconds%60 == 0:
                seconds = 0
                minutes+=1
                if minutes%60 == 0:
                    minutes = 0
                    hours+=1 

    def getTime(self):
        dur = self.timer_textInput.text.strip()
        durParts = []
        part = ""
        for ch in dur:
            if ch.isdigit():
                part+=ch
            else:
                durParts.append(int(part))
                part = ""
        durParts.append(int(part))
        part = "" 
        return durParts


class TodoList(MDApp):
    def build(self):
        return FirstScreen()


if __name__ == "__main__":
    TodoList().run()