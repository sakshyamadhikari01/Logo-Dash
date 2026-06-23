from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Input
from textual.reactive import reactive

class LogoDashApp(App):
    """Logo Dash: A text-programmed command platformer for Macondo Level 4."""
    
    # Letz use the header title here
    TITLE =  "LOGO DASH"

    #for interested devvs only :D

    #I got inspiration of this game form the games i used to play a long before like mario, geometry dash,
    #minecraft etc. This game is made for terminal and it works like mario and has character from geometry 
    #dash ofc to reduce the complexity. Oh yea i used concept from old days ms logo, sheesh brings back memory 
    #from 5th grade in computer lab. I used commands like fd, jp and since like im using concept from games 
    #like minecraft and geometry dash i used system of blocks for measurement like fd 3 makes it moves 3 blocks.

    CSS = """
    Screen {
        align: center middle;
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
    Input {
        margin-top: 1;
        border: tall $accent;
    }
    """
    
    BINDINGS = [   #keybinds yeaaaa
        ("q", "quit", "Quit Game"), #it results in quiting the game
        ("r", "reset", "Reset Position") #it results in reseting postion
    ]

    MAP_WIDTH = 60 from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Input
from textual.reactive import reactive

class LogoDashApp(App):
    """Logo Dash: A text-programmed command platformer for Macondo Level 4."""
    
    # Letz use the header title here
    TITLE =  "LOGO DASH"

    CSS = """
    Screen {
        align: center middle;
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
    Input {
        margin-top: 1;
        border: tall $accent;
    }
    """
    
    BINDINGS = [   #keybinds yeaaaa
        ("q", "quit", "Quit Game"),
        ("r", "reset", "Reset Position")
    ]

    MAP_WIDTH = 60 #map specifications width
    MAP_HEIGHT = 12#map specifications height
    
    LEVEL_MAP = [
        "............................................................", #dis one for za mapps
        "............................................................",
        "............................................................",
        "............................................................",
        "............................................................",
        "............................................................",
        "............................................................",
        "............................######..........................", 
        "............................................................",
        "......................^^..................^^................",#these are the spikes on this line
        "############################################################",
        "############################################################",
    ]

    player_x = reactive(2)
    player_y = reactive(9)  
    console_msg = reactive("Welcome to Logo Dash! Type commands like 'fd 3' or 'jp'.") #commands used from ms logo

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)  # Title argumed are out of the field
        with Vertical(id="game-layout"):
            yield Static(id="screen-render") #render from screen
            yield Static(id="console-log")
            yield Input(placeholder="Enter command (e.g., fd 5, bk 2, jp)...", id="cmd-input")
        yield Footer()

    def on_mount(self) -> None:
        self.render_map()
        self.query_one("#cmd-input").focus()

    def render_map(self) -> None:
        """Draws the combined frame of game map data and the player cube."""
        display_lines = []
        
        for y, line in enumerate(self.LEVEL_MAP):
            render_line = ""
            for x, char in enumerate(line):
                if x == self.player_x and y == self.player_y:
                    render_line += "[b][yellow]■[/][/]" 
                else:
                    if char == "#":
                        render_line += "[white]█[/]" 
                    elif char == "^":
                        render_line += "[red]▲[/]" 
                    else:
                        render_line += " " 
            display_lines.append(render_line)
            
        self.query_one("#screen-render", Static).update("\n".join(display_lines))

    def watch_player_x(self, new_x: int) -> None:
        self.render_map()

    def watch_player_y(self, new_y: int) -> None:
        self.render_map()

    def watch_console_msg(self, msg: str) -> None:
        # Watcher syntax to match textual rules
        self.query_one("#console-log", Static).update(f"> {msg}")

    def action_reset(self) -> None:
        self.player_x = 2
        self.player_y = 9
        self.console_msg = "Game Reset. Try planning your movements carefully!"

    def check_collisions(self) -> None:
        if self.player_x < 0: self.player_x = 0
        if self.player_x >= self.MAP_WIDTH: self.player_x = self.MAP_WIDTH - 1
        
        current_tile = self.LEVEL_MAP[self.player_y][self.player_x]
        
        if current_tile == "^":
            self.console_msg = "[blink][red]CRASHED! Press R key to reset.[/][/]"
            self.notify("You exploded on a spike!", severity="error") #if u do this mistake then u are dead 
        elif current_tile == "#":
            self.player_y -= 1
            self.console_msg = "Blocked by terrain feature!" # to block wall passing

    def execute_command(self, raw_cmd: str) -> None:
        parts = raw_cmd.strip().lower().split()
        if not parts:
            return

        cmd = parts[0]
        steps = 1
        if len(parts) > 1 and parts[1].isdigit():
            steps = int(parts[1])

        if cmd == "fd" or cmd == "forward":
            self.player_x += steps
            self.console_msg = f"Moved forward {steps} blocks."
            if self.LEVEL_MAP[self.player_y + 1][self.player_x] == ".":
                self.player_y = 9
                
        elif cmd == "bk" or cmd == "back":
            self.player_x -= steps
            self.console_msg = f"Moved backward {steps} blocks."
            if self.LEVEL_MAP[self.player_y + 1][self.player_x] == ".":
                self.player_y = 9

        elif cmd == "jp" or cmd == "jump":
            self.player_y -= 2
            self.player_x += 3
            self.console_msg = "Executed jump vector!"
            if self.LEVEL_MAP[self.player_y + 1][self.player_x] != "#":
                self.player_y = 9
                
        else:
            self.console_msg = f"[red]Unknown command:[/] '{cmd}'. Use fd, bk, or jp." # to filter real commands from badones

        self.check_collisions()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value:
            self.execute_command(event.value)
            self.query_one("#cmd-input", Input).value = ""

if __name__ == "__main__":
    LogoDashApp().run()
    MAP_HEIGHT = 12
    
    LEVEL_MAP = [
        "............................................................", #dis one for za mapps
        "............................................................",
        "............................................................",
        "............................................................",
        "............................................................",
        "............................................................",
        "............................................................",
        "............................######..........................",
        "............................................................",
        "......................^^..................^^................",
        "############################################################",
        "############################################################",
    ]

    player_x = reactive(2)
    player_y = reactive(9)  
    console_msg = reactive("Welcome to Logo Dash! Type commands like 'fd 3' or 'jp'.")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)  # Title argumed are out of the field
        with Vertical(id="game-layout"):
            yield Static(id="screen-render")
            yield Static(id="console-log")
            yield Input(placeholder="Enter command (e.g., fd 5, bk 2, jp)...", id="cmd-input")
        yield Footer()

    def on_mount(self) -> None:
        self.render_map()
        self.query_one("#cmd-input").focus()

    def render_map(self) -> None:
        """Draws the combined frame of game map data and the player cube."""
        display_lines = []
        
        for y, line in enumerate(self.LEVEL_MAP):
            render_line = ""
            for x, char in enumerate(line):
                if x == self.player_x and y == self.player_y:
                    render_line += "[b][yellow]■[/][/]" 
                else:
                    if char == "#":
                        render_line += "[white]█[/]" 
                    elif char == "^":
                        render_line += "[red]▲[/]" 
                    else:
                        render_line += " " 
            display_lines.append(render_line)
            
        self.query_one("#screen-render", Static).update("\n".join(display_lines))

    def watch_player_x(self, new_x: int) -> None:
        self.render_map()

    def watch_player_y(self, new_y: int) -> None:
        self.render_map()

    def watch_console_msg(self, msg: str) -> None:
        # Watcher syntax to match textual rules
        self.query_one("#console-log", Static).update(f"> {msg}")

    def action_reset(self) -> None:
        self.player_x = 2
        self.player_y = 9
        self.console_msg = "Game Reset. Try planning your movements carefully!" #post reset command screen

    def check_collisions(self) -> None:
        if self.player_x < 0: self.player_x = 0
        if self.player_x >= self.MAP_WIDTH: self.player_x = self.MAP_WIDTH - 1
        
        current_tile = self.LEVEL_MAP[self.player_y][self.player_x]
        
        if current_tile == "^":
            self.console_msg = "[blink][red]CRASHED! Press R key to reset.[/][/]"
            self.notify("You exploded on a spike!", severity="error") #explosion here
        elif current_tile == "#":
            self.player_y -= 1
            self.console_msg = "Blocked by terrain feature!" # to prevent wall golpig 

    def execute_command(self, raw_cmd: str) -> None:
        parts = raw_cmd.strip().lower().split()
        if not parts:
            return

        cmd = parts[0]
        steps = 1
        if len(parts) > 1 and parts[1].isdigit():
            steps = int(parts[1])

        if cmd == "fd" or cmd == "forward":
            self.player_x += steps
            self.console_msg = f"Moved forward {steps} blocks."
            if self.LEVEL_MAP[self.player_y + 1][self.player_x] == ".":
                self.player_y = 9
                
        elif cmd == "bk" or cmd == "back":
            self.player_x -= steps
            self.console_msg = f"Moved backward {steps} blocks."
            if self.LEVEL_MAP[self.player_y + 1][self.player_x] == ".":
                self.player_y = 9

        elif cmd == "jp" or cmd == "jump":
            self.player_y -= 2
            self.player_x += 3
            self.console_msg = "Executed jump vector!"
            if self.LEVEL_MAP[self.player_y + 1][self.player_x] != "#":
                self.player_y = 9
                
        else:
            self.console_msg = f"[red]Unknown command:[/] '{cmd}'. Use fd, bk, or jp."

        self.check_collisions()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value:
            self.execute_command(event.value)
            self.query_one("#cmd-input", Input).value = ""

if __name__ == "__main__":
    LogoDashApp().run()