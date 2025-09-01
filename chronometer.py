# libs needed on the project
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.widget import Widget
from kivymd.uix.button import MDRectangleFlatIconButton
from threading import Thread
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

        # Box for chronometer display
        self.chronometer_boxlayout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=60,
        )

        # chronometer text input (read-only)
        self.chronometer_textInput = TextInput(
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

        # Add chronometer with spacers
        self.chronometer_boxlayout.add_widget(Widget(height=100)) # spacer
        self.chronometer_boxlayout.add_widget(self.chronometer_textInput)
        self.chronometer_boxlayout.add_widget(Widget(height=100)) # spacer
        self.add_widget(self.chronometer_boxlayout)

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

        # Initialize chronometer display
        self.replaceChronometerValue(f"{0:02}.{0:06}")

        # Condition for thread loop
        self.cond = True
        
        #to check if there is a update chronometer thread 
        self.therIsthread = False

    # Start chronometer
    def start(self, instance):
        #add a if statment to avoid creating many updateChronometerDisplay threads by checking if ther is a thread
        if not self.therIsthread:
            global thread
            self.therIsthread = True
            thread = Thread(target=self.updateChronometerDisplay)
            thread.daemon = True
            thread.start()
    
    # update chronometer display using datetime 
    def updateChronometerDisplay(self):
        #intialDateTime is the diffrence between the start datetime and the delta (the time on the chronometer)
        # intialDateTime allows us to complete counting from the time that we was stoped in
        currrentDateTime = datetime.now()
        h,m,s,ms = self.convertChronometerValue(self.getChronometerValue()) #the time on the chronometer as (hours, minutes, seconds, microseconds)
        delta = timedelta(hours=h,minutes=m,seconds=s,microseconds=ms)
        intialDateTime = currrentDateTime-delta
        #  This relies on real time, making the chronometer more accurate and updating every 0.000001 seconds.
        while self.cond:
            currDateTime = datetime.now()
            # calculate the difference between the current datetime and the start datetime directly (currDateTime - intialDateTime).
            Clock.schedule_once(lambda dt: self.replaceChronometerValue(self.chronometerFormat(currDateTime-intialDateTime)))
            time.sleep(0.000001)
    
    #change the chronometer format to display hours and minutes correctly
    def chronometerFormat(self,chronoValue):
        h,m,s,ms = self.convertChronometerValue(str(chronoValue))
        if h > 0:
            return str(chronoValue)
        elif m > 0:
            return f"{m:02}:{s:02}.{ms:06}"
        else:
            return f"{s:02}.{ms:06}"
               
    # Pause chronometer
    def pause(self, instance):
        #to avoid NameError(name 'thread' is not defined) if 
        # the pause button is pressed befor start button( befor creating updateChronometer thread).
        if self.therIsthread:
            self.cond = False
            thread.join()
            self.cond = True
            self.therIsthread = False

    # Restart chronometer
    def restart(self, instance):
        #to avoid NameError(name 'thread' is not defined.) if 
        # the restart button is pressed befor start button( befor creating updateChronometer thread)
        if self.therIsthread:
            self.cond = False
            thread.join()
            self.replaceChronometerValue(f"{0:02}.{0:06}")
            self.cond = True
            self.therIsthread = False
            self.laps.clear_widgets()
        else:
            self.replaceChronometerValue(f"{0:02}.{0:06}")
            self.laps.clear_widgets()

    # Add current chronometer value as a lap on the scrollable lips list
    def addLaps(self, instance):
        #to avoid adding laps befor geting the chronometer started 
        if self.therIsthread:
            self.laps.add_widget(OneLineListItem(
                text=self.chronometer_textInput.text.strip(),
                font_style='H6',
                theme_text_color="Custom",
                text_color=colors["Blue"]["800"],
            ))

    # Replace displayed chronometer value
    def replaceChronometerValue(self, txt):
        self.chronometer_textInput.text = txt
            
    # Get desplyed chronometer value as string
    def getChronometerValue(self):
        return self.chronometer_textInput.text.strip()

    # Convert chronometer value (string) into hours, minutes, seconds, microseconds
    def convertChronometerValue(self, chronoValue):
        timeParts = [0,0,0,0]
        tracker = -1
        part = ""
        for i in range(len(chronoValue)-1,-1,-1):
            if chronoValue[i].isdigit():
                part = chronoValue[i]+part
            else:
                timeParts[tracker] = int(part)
                tracker -= 1
                part = ""
        timeParts[tracker] = int(part)
        return timeParts

# Main app class
class Chronometer(MDApp):
    def build(self):
        return FirstScreen()

if __name__ == "__main__":
    Chronometer().run()