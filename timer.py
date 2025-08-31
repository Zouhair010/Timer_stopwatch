# libs needed on the project
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
from datetime import datetime, timedelta

# Main layout
class FirstScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout properties
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        # Box for timer display
        self.timer_boxlayout = MDBoxLayout(
            orientation="horizontal",
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
            foreground_color=colors["Blue"]["800"]
        )

        # Add timer with spacers
        self.timer_boxlayout.add_widget(Widget(height=100)) # spacer
        self.timer_boxlayout.add_widget(self.timer_textInput)
        self.timer_boxlayout.add_widget(Widget(height=100)) # spacer
        self.add_widget(self.timer_boxlayout)

        # Layout for buttons
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
        self.buttons_boxlayout.add_widget(Widget()) # spacer
        self.buttons_boxlayout.add_widget(self.pause_button)

        # Restart button
        self.restart_button = MDRectangleFlatIconButton(
            text="restart",
            font_style='H6',
            icon="replay",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.restart_button.bind(on_release=self.restart)
        self.buttons_boxlayout.add_widget(Widget()) # spacer
        self.buttons_boxlayout.add_widget(self.restart_button)

        # Lap button
        self.lap_button = MDRectangleFlatIconButton(
            text="lap",
            font_style='H6',
            icon="plus",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.lap_button.bind(on_release=self.addLaps)
        self.buttons_boxlayout.add_widget(Widget()) # spacer
        self.buttons_boxlayout.add_widget(self.lap_button)

        self.add_widget(self.buttons_boxlayout)

        # Spacer between buttons and laps
        self.spacer = MDBoxLayout(size_hint_y=None, height=100, orientation="horizontal", spacing=10, padding=10)
        self.add_widget(self.spacer)

        # Scrollable list for laps
        self.scroll = MDScrollView() # to make laps scrollable
        self.laps = MDList()
        self.scroll.add_widget(self.laps)
        self.add_widget(self.scroll)

        # Initialize timer display
        self.replaceTime(f"{0:02}:{0:02}:{0:02}.{0:06}")

        # Condition for thread loop
        self.cond = True
        
        #to check if there is a updatetime thread 
        self.therIsthread = False

    # Start timer thread
    def start(self, instance):
        #add a if statment to avoid creating many updatetime threads by checking if ther is a thread
        if not self.therIsthread:
            global thread
            self.therIsthread = True
            thread = Thread(target=self.updateTime)
            thread.daemon = True
            thread.start()
    
    # update timer display using datetime 
    def updateTime(self):
        currrentDateTime = datetime.now()
        #intialDateTime is the diffrence between the start datetime and the delta (the time on the stopwatch)
        # intialDateTime allows us to complete counting from the time that we was stoped in
        h,m,s,ms = self.convertTime(self.getTime()) #the time on the stopwatch as (hours, minutes, seconds, microseconds)
        delta = timedelta(hours=h,minutes=m,seconds=s,microseconds=ms)
        print(currrentDateTime)
        intialDateTime = currrentDateTime-delta
        print(intialDateTime)
        #  This relies on real time, making the timing more accurate and updating every 0.000001 seconds.
        while self.cond:
            currDateTime = datetime.now()
            # calculate the difference between the current datetime and the start datetime directly (currDateTime - intialDateTime).
            Clock.schedule_once(lambda dt: self.replaceTime(f"{currDateTime-intialDateTime}"))
            time.sleep(0.000001)

    # Pause timer
    def pause(self, instance):
        #to avoid NameError(name 'thread' is not defined.) if the pause button is pressed befor start button( befor creating updatetime thread)
        if self.therIsthread:
            self.cond = False
            thread.join()
            self.cond = True
            self.therIsthread = False

    # Restart timer
    def restart(self, instance):
        #to avoid NameError(name 'thread' is not defined.) if the restart button is pressed befor start button( befor creating updatetime thread)
        if self.therIsthread:
            self.cond = False
            thread.join()
            self.replaceTime(f"{0:02}:{0:02}:{0:02}.{0:06}")
            self.cond = True
            self.therIsthread = False
            self.laps.clear_widgets()
        else:
            self.replaceTime(f"{0:02}:{0:02}:{0:02}.{0:06}")
            self.laps.clear_widgets()

    # Add current timer value as a lap on the scrollable lips list
    def addLaps(self, instance):
        #to avoid adding laps befor geting stopwatch started 
        if self.therIsthread:
            self.laps.add_widget(OneLineListItem(
                text=self.timer_textInput.text.strip(),
                font_style='H6',
                theme_text_color="Custom",
                text_color=colors["Blue"]["800"],
            ))

    # Replace displayed time
    def replaceTime(self, txt):
        self.timer_textInput.text = txt
            

    # Get desplyed timer value as string
    def getTime(self):
        return self.timer_textInput.text.strip()

    # Convert time string into hours, minutes, seconds, microseconds
    def convertTime(self, time):
        durParts = []
        part = ""
        for ch in time:
            if ch.isdigit():
                part += ch
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