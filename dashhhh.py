from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal 
from textual.widgets import Header, Footer, Button, Static, Digits, TabbedContent, TabPane
from textual.reactive import reactive

class LogoDashApp(App):
    """A Logo Dash Game Using Textual"""

    CSS = """
    Screen {
        align: center Middle;
        background: $background;
        }


        #game-layout {
        width: 70;
        height: 24;
        border: double $primary;
        padding: 1;
        }


        #screen-render {
        width: 100%;
        height: 16;
        background: $boost;
        border: solid $surface;
        content-align: left top;
        }

        #console-log {
height: 3;
 margin-top: 1;
background: $panel;
color: $success;
 padding-left: 1;
}


Input{
margin-top: 1;
border:  tall $accent;
}
"""

BINDINGS = [
    ("q","quit", "Quit Game"),
    ("r", "reset", "Reset Positin")
]

#variablessszzz for map (width:60, Height:12)
MAP_WIDTH = 60
MAP_HEIGHT = 12

#level arrayy layouutt:
#'.' Sky, '#' = Solid Platform, '^' = Danger Dripstonee (like in minecraft for refrence hehe!)

LEVEL_MAP = [
    "............................................................",
    "............................................................",
    "............................................................",
    "............................................................",
    "............................................................",
    "............................................................",
    "............................................................",
    "............................................................",
    "...........................#######..........................",
    "............................................................",
    "......................^^...................^^...............",
    "############################################################",
    "############################################################",

]

#active playerss statee variablesss
player_x = reactive(2)
player_y = reactive(9) #spawing area and thats safe area i.e. ground floor btw if ya'll are curious -_-
console_msg = reactive("Wassup Guys! Welcome to My game :D  avoid the Drippystones! (^) btw type commands like 'fd 3' or 'jp'")\


def compose(self) -> ComposeResult:
yield Header(title="Log0 Dash", show_clock= True)
with Vertical (id="game-layout"):
yield Static(id="screen-render")
yield Static(id="console-log")
yield Imput(placeholder="Enter command (e.g., fd 5, bk 2, jp)...", id="cmd-input")
yield Footer()

def on_mount(self) -> None:
    self.render_map()
    self.query_one("#cmd-input").focus()

def render_map(self) -> None:
    """Actually it draws the combined frame of game map and the player cube"""
    display_lines = []
    

    for y,line in enumerate(self.LEVEL_MAP):
        render_line = ""
        for x, char in enumerate(line):
            #what it basically does is it checks if the current occupying this tile frame coordinates
            if x == self.player_x and y == self.player_y:
                render_line += "[b][yellow]■[/][/]"#geometry dash player inspiration hehe actiually a excuse so i dont need to make hard characters
            else:
                if char == "#":
                    render_line += "[white]█[/]"#solid block 
        
