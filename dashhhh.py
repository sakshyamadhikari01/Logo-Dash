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
                    elif char == "^":
render_line += "[red]▲[/]"#dripstone danger
else:
render_line += " "# emply space to symbolize emptiness of sky, could become a poet hehe
display_line.append(render_line)
#now to push the raw construced text blocks into our display engine container
self.query_one("#screen-render", Static).update("\n".join(display_lines))

def watch_player_x(self, old:int,new:int) -> None:\
self.render_map()
    
def watch_player_y(self, old:int,new:int) -> None:
    self.render_map()

def watch_console_msg(self, old:str,new:str) -> f"> {msg}")
    
    def action_reset(self) -> None:
        """Instant restoration of player back to the starting position"""
        self.player_x = 2
        self.player_y = 9
        self.console_msg = "game reset. Try planning ur movements kiddo"

        def check_collisions(self) -> None:
            """Evaluation if player hits safe place or wall or a drippystone"""
        #check check not mic but boundaries
         if self.player_x < 0: self.player_x = 0
        if self.player_x >= self.MAP_WIDTH: self.player_x = self.MAP_WIDTH -1 

        #pull map block type at our specific geometric location coordinates
        current_tile = self.LEVEL_MAP [self.player_y][self.player_x]

        if current_title == "^":
            self.console_msg = "[blink [red]CRASHED! Run 'r' or press R key to reset.[/]"
            self.notify("You exploded",severity = "error")
        elif current_tile == "#":
            #IF it is inside a solid block, it will push them up out of it 
            self.player_y -= 1
            self.console_msg = "blocked by terrain feature"

            def execute_command(self, raw_cmd: str) -> None:
                """to use MS-LOGO style terminal movement"""
                parts = raw_cmd.strip().lower().split()
         
