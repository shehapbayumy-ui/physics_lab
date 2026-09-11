import json
import math
import threading
import time
import urllib.request
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider


# ============================================================
# COLORS
# ============================================================

BG = (0.015, 0.025, 0.055, 1)
PANEL = (0.035, 0.055, 0.105, 1)
PANEL2 = (0.055, 0.08, 0.145, 1)
BLUE = (0.05, 0.55, 1, 1)
CYAN = (0.1, 0.8, 1, 1)
WHITE = (0.92, 0.96, 1, 1)
GRAY = (0.55, 0.62, 0.72, 1)
GREEN = (0.15, 1, 0.5, 1)
RED = (1, 0.25, 0.3, 1)
ORANGE = (1, 0.55, 0.1, 1)


# ============================================================
# SPACE BACKGROUND
# ============================================================

class SpaceBackground(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*BG)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

            Color(0.03, 0.08, 0.16, 0.5)
            self.glow = Ellipse(
                pos=(dp(30), dp(200)),
                size=(dp(300), dp(300))
            )

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


# ============================================================
# COMMON BUTTON
# ============================================================

class MainButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = PANEL2
        self.color = WHITE
        self.font_size = dp(16)
        self.bold = True

        with self.canvas.after:
            Color(*BLUE)
            self.button_line = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(12)
                ),
                width=1.1
            )

        self.bind(pos=self.update_line, size=self.update_line)

    def update_line(self, *args):
        self.button_line.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(12)
        )


# ============================================================
# EXPERIMENT CARD
# ============================================================

class ExperimentCard(Button):

    def __init__(
        self,
        title,
        subtitle,
        icon,
        index,
        locked=False,
        special=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.title_name = title
        self.subtitle_name = subtitle
        self.icon_name = icon
        self.index = index
        self.locked = locked
        self.special = special

        self.background_normal = ""
        self.background_down = ""
        self.background_color = PANEL
        self.color = WHITE
        self.markup = True

        lock_text = "  [color=#FFB347]PRO[/color]" if locked else ""

        self.text = (
            f"[size=18][b]{icon}[/b][/size]   "
            f"[b]{title}[/b]{lock_text}\n"
            f"[color=#8F9BAF]{subtitle}[/color]"
        )

        with self.canvas.after:
            Color(*BLUE)
            self.card_line = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(14)
                ),
                width=0.8
            )

        self.bind(pos=self.update_card, size=self.update_card)

    def update_card(self, *args):
        self.card_line.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(14)
        )


# ============================================================
# HOME
# ============================================================

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = SpaceBackground()
        self.add_widget(root)

        title = Label(
            text="[b]PHYSICS[/b] [color=#36A8FF][b]LAB[/b][/color]",
            markup=True,
            font_size=dp(38),
            color=WHITE,
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "center_y": 0.67}
        )
        root.add_widget(title)

        subtitle = Label(
            text="Explore physics in a different way",
            font_size=dp(17),
            color=GRAY,
            size_hint=(1, None),
            height=dp(40),
            pos_hint={"center_x": 0.5, "center_y": 0.59}
        )
        root.add_widget(subtitle)

        start = MainButton(
            text="START LAB",
            size_hint=(0.72, None),
            height=dp(58),
            pos_hint={"center_x": 0.5, "center_y": 0.47}
        )
        start.bind(on_release=self.start_lab)
        root.add_widget(start)

        info = Label(
            text="9 experiments + ISS Mission Center",
            color=GRAY,
            font_size=dp(13),
            size_hint=(1, None),
            height=dp(30),
            pos_hint={"center_x": 0.5, "center_y": 0.35}
        )
        root.add_widget(info)

    def start_lab(self, *args):
        self.manager.current = "experiments"


# ============================================================
# EXPERIMENTS
# ============================================================

class ExperimentsScreen(Screen):

    experiments = [
        ("MECHANICS", "Motion & Forces", "M", 0, False, None),
        ("GRAVITY", "Orbits & Gravity", "G", 1, False, None),
        ("SOLAR SYSTEM", "Planets & Motion", "S", 2, True, None),
        ("RELATIVITY", "Time & Speed", "R", 3, True, None),
        ("WAVES", "Frequency & Motion", "W", 4, False, None),
        ("OPTICS", "Light & Reflection", "O", 5, False, None),
        ("ELECTRICITY", "Circuits & Current", "E", 6, True, None),
        ("ENERGY", "Energy Transformations", "N", 7, True, None),
        ("QUANTUM", "The Quantum World", "Q", 8, True, None),
        (
            "ISS MISSION CENTER",
            "International Space Station",
            "ISS",
            99,
            True,
            "iss"
        ),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = SpaceBackground()
        self.add_widget(root)

        title = Label(
            text="[b]PHYSICS[/b] [color=#36A8FF][b]LAB[/b][/color]",
            markup=True,
            font_size=dp(25),
            size_hint=(1, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "top": 0.98}
        )
        root.add_widget(title)

        scroll_area = FloatLayout(
            size_hint=(0.94, 0.80),
            pos_hint={"center_x": 0.5, "y": 0.09}
        )

        positions = [
            (0.02, 0.82), (0.51, 0.82),
            (0.02, 0.66), (0.51, 0.66),
            (0.02, 0.50), (0.51, 0.50),
            (0.02, 0.34), (0.51, 0.34),
            (0.02, 0.18), (0.51, 0.18),
        ]

        for i, data in enumerate(self.experiments):

            title_text, subtitle, icon, index, locked, special = data

            card = ExperimentCard(
                title_text,
                subtitle,
                icon,
                index,
                locked,
                special,
                size_hint=(0.47, 0.13),
                pos_hint={
                    "x": positions[i][0],
                    "y": positions[i][1]
                }
            )

            card.bind(
                on_release=lambda btn, d=data:
                self.open_experiment(d)
            )

            scroll_area.add_widget(card)

        root.add_widget(scroll_area)

        back = MainButton(
            text="BACK",
            size_hint=(0.25, None),
            height=dp(45),
            pos_hint={"x": 0.04, "y": 0.02}
        )
        back.bind(on_release=lambda x: self.back())
        root.add_widget(back)

        pro = MainButton(
            text="PRO",
            size_hint=(0.25, None),
            height=dp(45),
            pos_hint={"right": 0.96, "y": 0.02}
        )
        pro.bind(on_release=lambda x: self.open_pro())
        root.add_widget(pro)

    def back(self):
        self.manager.current = "home"

    def open_pro(self):
        self.manager.current = "pro"

    def open_experiment(self, data):

        title_text, subtitle, icon, index, locked, special = data

        app = App.get_running_app()

        if locked and not app.pro_unlocked:
            self.manager.current = "pro"
            return

        if special == "iss":
            self.manager.current = "iss"
            return

        screen = self.manager.get_screen("experiment")
        screen.setup(title_text, index)
        self.manager.current = "experiment"


# ============================================================
# PRO SCREEN
# ============================================================

class ProScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = SpaceBackground()
        self.add_widget(root)

        title = Label(
            text="[b]PHYSICS LAB[/b] [color=#36A8FF][b]PRO[/b][/color]",
            markup=True,
            font_size=dp(30),
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        root.add_widget(title)

        sub = Label(
            text="Go beyond the classroom",
            color=GRAY,
            font_size=dp(17),
            size_hint=(1, None),
            height=dp(40),
            pos_hint={"center_x": 0.5, "top": 0.84}
        )
        root.add_widget(sub)

        features = (
            "ADVANCED SOLAR SYSTEM\n\n"
            "BLACK HOLE LAB\n\n"
            "RELATIVITY LAB\n\n"
            "ELECTRICITY LAB\n\n"
            "ENERGY LAB\n\n"
            "QUANTUM LAB\n\n"
            "PHYSICS CHALLENGES\n\n"
            "ISS MISSION CENTER"
        )

        feature_label = Label(
            text=features,
            color=WHITE,
            font_size=dp(15),
            halign="left",
            valign="top",
            size_hint=(0.8, 0.55),
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        feature_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )
        root.add_widget(feature_label)

        price = Label(
            text="[b]69 EGP[/b]  -  ONE TIME",
            markup=True,
            color=CYAN,
            font_size=dp(23),
            size_hint=(1, None),
            height=dp(45),
            pos_hint={"center_x": 0.5, "y": 0.13}
        )
        root.add_widget(price)

        unlock = MainButton(
            text="UNLOCK PRO",
            size_hint=(0.65, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.055}
        )
        unlock.bind(on_release=self.unlock_demo)
        root.add_widget(unlock)

        back = MainButton(
            text="BACK",
            size_hint=(0.23, None),
            height=dp(40),
            pos_hint={"x": 0.04, "top": 0.96}
        )
        back.bind(on_release=lambda x: self.back())
        root.add_widget(back)

    def unlock_demo(self, *args):
        App.get_running_app().pro_unlocked = True
        self.manager.current = "experiments"

    def back(self):
        self.manager.current = "experiments"


# ============================================================
# BASIC SIMULATION
# ============================================================

class Simulation(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.t = 0

        with self.canvas:
            Color(*BLUE)
            self.object = Ellipse(
                pos=(dp(100), dp(200)),
                size=(dp(45), dp(45))
            )

        Clock.schedule_interval(self.update, 1 / 60)

    def update(self, dt):

        self.t += dt

        x = dp(100) + math.sin(self.t) * dp(100)
        y = dp(200) + math.cos(self.t * 1.5) * dp(50)

        self.object.pos = (x, y)


# ============================================================
# EXPERIMENT SCREEN
# ============================================================

class ExperimentScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root_layout = SpaceBackground()
        self.add_widget(self.root_layout)

        self.title_label = Label(
            text="EXPERIMENT",
            font_size=dp(26),
            color=WHITE,
            size_hint=(1, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "top": 0.96}
        )

        self.root_layout.add_widget(self.title_label)

        self.description = Label(
            text="Interactive physics simulation",
            color=GRAY,
            font_size=dp(16),
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "top": 0.82}
        )

        self.root_layout.add_widget(self.description)

        self.simulation = Simulation(
            size_hint=(0.9, 0.45),
            pos_hint={"center_x": 0.5, "y": 0.25}
        )

        self.root_layout.add_widget(self.simulation)

        back = MainButton(
            text="BACK",
            size_hint=(0.28, None),
            height=dp(45),
            pos_hint={"x": 0.05, "y": 0.05}
        )

        back.bind(
            on_release=lambda x:
            setattr(self.manager, "current", "experiments")
        )

        self.root_layout.add_widget(back)

    def setup(self, title, index):

        self.title_label.text = title

        descriptions = {
            0: "Study motion, force and acceleration.",
            1: "Explore gravity and orbital motion.",
            4: "Study frequency, amplitude and waves.",
            5: "Explore reflection and light.",
        }

        self.description.text = descriptions.get(
            index,
            "Advanced experiment available in PRO."
        )


# ============================================================
# ISS MISSION CENTER
# ============================================================

class ISSScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root_layout = SpaceBackground()
        self.add_widget(self.root_layout)

        self.live = False
        self.fetching = False

        self.iss_lat = 0.0
        self.iss_lon = 0.0
        self.altitude = 408.0
        self.velocity = 27600.0
        self.distance = 1000.0

        self.sim_time = 0.0

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        self.title = Label(
            text="[b]ISS MISSION CENTER[/b]",
            markup=True,
            font_size=dp(25),
            color=WHITE,
            size_hint=(1, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "top": 0.97}
        )
        self.root_layout.add_widget(self.title)

        self.status = Label(
            text="SIMULATION MODE",
            font_size=dp(14),
            color=ORANGE,
            size_hint=(1, None),
            height=dp(35),
            pos_hint={"center_x": 0.5, "top": 0.89}
        )
        self.root_layout.add_widget(self.status)

        # ----------------------------------------------------
        # EARTH AREA
        # ----------------------------------------------------

        self.earth_area = FloatLayout(
            size_hint=(0.90, 0.48),
            pos_hint={"center_x": 0.5, "y": 0.34}
        )

        self.root_layout.add_widget(self.earth_area)

        with self.earth_area.canvas:

            Color(0.04, 0.25, 0.55, 1)

            self.earth = Ellipse(
                pos=(dp(60), dp(30)),
                size=(dp(220), dp(220))
            )

            Color(0.15, 0.65, 1, 0.7)

            self.orbit = Line(
                ellipse=(
                    dp(35),
                    dp(5),
                    dp(270),
                    dp(270)
                ),
                width=1.3
            )

            Color(1, 1, 1, 1)

            self.iss_dot = Ellipse(
                pos=(dp(0), dp(0)),
                size=(dp(12), dp(12))
            )

            Color(0.3, 0.8, 1, 0.35)

            self.trail = Line(
                points=[],
                width=2
            )

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        self.lat_label = self.make_data(
            "LATITUDE",
            0.88,
            self.root_layout
        )

        self.lon_label = self.make_data(
            "LONGITUDE",
            0.78,
            self.root_layout
        )

        self.alt_label = self.make_data(
            "ALTITUDE",
            0.68,
            self.root_layout
        )

        self.velocity_label = self.make_data(
            "VELOCITY",
            0.58,
            self.root_layout
        )

        self.distance_label = self.make_data(
            "DISTANCE",
            0.48,
            self.root_layout
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        refresh = MainButton(
            text="REFRESH LIVE DATA",
            size_hint=(0.55, None),
            height=dp(48),
            pos_hint={"center_x": 0.5, "y": 0.20}
        )

        refresh.bind(on_release=self.refresh_live)
        self.root_layout.add_widget(refresh)

        self.back_button = MainButton(
            text="BACK",
            size_hint=(0.25, None),
            height=dp(42),
            pos_hint={"x": 0.05, "y": 0.07}
        )

        self.back_button.bind(
            on_release=lambda x:
            setattr(self.manager, "current", "experiments")
        )

        self.root_layout.add_widget(self.back_button)

        self.pause_button = MainButton(
            text="PAUSE",
            size_hint=(0.25, None),
            height=dp(42),
            pos_hint={"right": 0.95, "y": 0.07}
        )

        self.paused = False

        self.pause_button.bind(
            on_release=self.toggle_pause
        )

        self.root_layout.add_widget(self.pause_button)

        Clock.schedule_interval(
            self.update_simulation,
            1 / 30
        )

    def make_data(self, name, y, parent):

        label = Label(
            text=f"{name}: --",
            color=WHITE,
            font_size=dp(14),
            halign="left",
            size_hint=(0.9, None),
            height=dp(30),
            pos_hint={"center_x": 0.5, "y": y}
        )

        parent.add_widget(label)

        return label

    # --------------------------------------------------------
    # SIMULATION
    # --------------------------------------------------------

    def update_simulation(self, dt):

        if self.paused:
            return

        self.sim_time += dt

        if not self.live:

            angle = self.sim_time * 0.7

            self.iss_lat = math.sin(angle) * 51.6
            self.iss_lon = (
                ((self.sim_time * 20) + 180) % 360
            ) - 180

            self.altitude = 408 + math.sin(
                self.sim_time * 0.4
            ) * 3

            self.velocity = 27600 + math.sin(
                self.sim_time
            ) * 50

        self.update_visuals()

    def update_visuals(self):

        # Map latitude/longitude to a simple orbit visualization.

        cx = dp(170)
        cy = dp(140)

        radius_x = dp(125)
        radius_y = dp(125)

        angle = math.radians(
            self.iss_lon
        )

        x = cx + math.cos(angle) * radius_x
        y = cy + math.sin(
            math.radians(self.iss_lat)
        ) * radius_y

        self.iss_dot.pos = (
            x,
            y
        )

        self.lat_label.text = (
            f"LATITUDE: {self.iss_lat:.2f} deg"
        )

        self.lon_label.text = (
            f"LONGITUDE: {self.iss_lon:.2f} deg"
        )

        self.alt_label.text = (
            f"ALTITUDE: {self.altitude:.1f} km"
        )

        self.velocity_label.text = (
            f"VELOCITY: {self.velocity:.0f} km/h"
        )

        self.distance_label.text = (
            f"DISTANCE: {self.distance:.0f} km"
        )

    # --------------------------------------------------------
    # LIVE API
    # --------------------------------------------------------

    def refresh_live(self, *args):

        if self.fetching:
            return

        self.fetching = True

        self.status.text = "CONNECTING TO ISS..."
        self.status.color = ORANGE

        thread = threading.Thread(
            target=self.fetch_iss_data,
            daemon=True
        )

        thread.start()

    def fetch_iss_data(self):

        url = "https://api.wheretheiss.at/v1/satellites/25544"

        try:

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent":
                    "PhysicsLab/1.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=8
            ) as response:

                data = json.loads(
                    response.read().decode("utf-8")
                )

            Clock.schedule_once(
                lambda dt:
                self.apply_live_data(data)
            )

        except Exception as error:

            print("ISS API ERROR:", error)

            Clock.schedule_once(
                lambda dt:
                self.live_failed()
            )

    def apply_live_data(self, data):

        self.fetching = False

        try:

            self.iss_lat = float(
                data.get("latitude", 0)
            )

            self.iss_lon = float(
                data.get("longitude", 0)
            )

            self.altitude = float(
                data.get("altitude", 0)
            )

            self.velocity = float(
                data.get("velocity", 0)
            )

            self.distance = 0

            self.live = True

            self.status.text = (
                "LIVE DATA  -  ISS / ZARYA"
            )

            self.status.color = GREEN

            self.update_visuals()

        except Exception:

            self.live_failed()

    def live_failed(self):

        self.fetching = False
        self.live = False

        self.status.text = (
            "SIMULATION MODE  -  LIVE DATA UNAVAILABLE"
        )

        self.status.color = ORANGE

    # --------------------------------------------------------
    # PAUSE
    # --------------------------------------------------------

    def toggle_pause(self, *args):

        self.paused = not self.paused

        if self.paused:
            self.pause_button.text = "RESUME"
        else:
            self.pause_button.text = "PAUSE"


# ============================================================
# MAIN APP
# ============================================================

class PhysicsLab(App):

    pro_unlocked = False

    def build(self):

        self.title = "Physics Lab"

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(name="home")
        )

        manager.add_widget(
            ExperimentsScreen(name="experiments")
        )

        manager.add_widget(
            ProScreen(name="pro")
        )

        manager.add_widget(
            ExperimentScreen(name="experiment")
        )

        manager.add_widget(
            ISSScreen(name="iss")
        )

        return manager


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    PhysicsLab().run()