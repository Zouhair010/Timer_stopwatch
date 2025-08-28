# libs needed in that project
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.widget import Widget
from kivymd.uix.button import MDRectangleFlatIconButton
from threading import Thread
import threading
from kivymd.color_definitions import colors
from kivy.clock import Clock
import time

class FirstScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main layout properties
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10
        # Box for timer display
        self.timer_boxlayout=MDBoxLayout(
            orientation = "horizontal",
            size_hint_y=None,
            height=60,
        )
        # Timer text input (read-only)
        self.timer_textInput = TextInput(
            halign="center",
            readonly=True,
            size_hint=(140,None),
            font_size=40,
            size=(200,60),
            background_normal='',
            background_active='',
            background_color=(0,0,0,0),
            foreground_color= colors["Blue"]["800"]
        )
        # Add timer with spacers
        self.timer_boxlayout.add_widget(Widget(height=100))# spacer
        self.timer_boxlayout.add_widget(self.timer_textInput)
        self.timer_boxlayout.add_widget(Widget(height=100))# spacer
        self.add_widget(self.timer_boxlayout)
        # Add timer with spacers
        self.buttons_boxlayout = MDGridLayout(cols=8, spacing=10, padding=20, size_hint_y=None, height=50)
        # Start button
        self.start_button = MDRectangleFlatIconButton(
            text="start",
            font_style='H6',
            icon="play",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.start_button.bind(on_release=self.start) 
        self.buttons_boxlayout.add_widget(self.start_button)
        # Pause button
        self.pause_button = MDRectangleFlatIconButton(
            text="pause",
            font_style='H6',
            icon="pause",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.pause_button.bind(on_release=self.pause)
        self.buttons_boxlayout.add_widget(Widget())
        self.buttons_boxlayout.add_widget(self.pause_button)
        # Restart button
        self.restart_button = MDRectangleFlatIconButton(
            text="restart",
            font_style='H6',
            icon="replay",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.restart_button.bind(on_release=self.restart) 
        self.buttons_boxlayout.add_widget(Widget())
        self.buttons_boxlayout.add_widget(self.restart_button)
        # Lap button
        self.lap_button = MDRectangleFlatIconButton(
            text="lap",
            font_style='H6',
            icon="plus",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.lap_button.bind(on_release=self.addLaps) 
        self.buttons_boxlayout.add_widget(Widget())
        self.buttons_boxlayout.add_widget(self.lap_button)
        self.add_widget(self.buttons_boxlayout)
        # Spacer between buttons and laps
        self.spacer = MDBoxLayout(size_hint_y=None, height=100,orientation ="horizontal",spacing=10, padding=10)
        self.add_widget(self.spacer)
        # Scrollable list for laps
        self.scroll = MDScrollView()#to make tasks scroll
        self.laps = MDList()
        self.scroll.add_widget(self.laps)
        self.add_widget(self.scroll)
        # Initialize timer display
        self.replaceTime(f"{0:02}:{0:02}:{0:02}.{0:02}")
        # Condition for thread loop
        self.cond = True

    # Add current timer value as a lap
    def addLaps(self,instance):
        self.laps.add_widget(OneLineListItem(
            text=self.timer_textInput.text.strip(),
            font_style='H6',
            theme_text_color="Custom",
            text_color= colors["Blue"]["800"],
        ))
    # Replace displayed time
    def replaceTime(self,txt):
        self.timer_textInput.text = txt
    # Start timer thread 
    def start(self,instance):
        global thread
        print(threading.active_count())
        if threading.active_count() == 1:
            thread = Thread(target=self.updateTime)
            thread.daemon = True
            thread.start()
    # Pause timer
    def pause(self,instance):
        try:
            self.cond = False
            thread.join()
        except:
            print("exception")

        self.cond = True
    # Restart timer
    def restart(self,instance):
        try:
            self.cond = False
            thread.join()
        except:
            print("exception")

        self.cond = True
        self.replaceTime(f"{0:02}:{0:02}:{0:02}.{0:02}")
        self.laps.clear_widgets()
    # Timer update loop with microseconds
    def updateTime(self):
        hours, minutes, seconds, microsecs = self.getTime()
        while self.cond:
            Clock.schedule_once(lambda dt: self.replaceTime(f"{hours:02}:{minutes:02}:{seconds:02}.{microsecs:02}"))
            time.sleep(0.1)
            microsecs+=1
            if microsecs == 10:
                print(seconds)
                microsecs = 0
                seconds+=1
                if seconds%60 == 0:
                    seconds = 0
                    minutes+=1
                    if minutes%60 == 0:
                        minutes = 0
                        hours+=1 
    # Extract time values from displayed text
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

# Main app class
class Timer(MDApp):
    def build(self):
        return FirstScreen()


if __name__ == "__main__":
    Timer().run()