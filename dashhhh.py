from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Input
from textual.reactive import reactive


class LogoDashApp(App):

 
    #for interested devvs only :D

    #I got inspiration of this game form the games i used to play a long before like mario, geometry dash,
    #minecraft etc. This game is made for terminal and it works like mario and has character from geometry 
    #dash ofc to reduce the complexity. Oh yea i used concept from old days ms logo, sheesh brings back memory 
    #from 5th grade in computer lab. I used commands like fd, jp and since like im using concept from games 
    #like minecraft and geometry dash i used system of blocks for measurement like fd 3 makes it moves 3 blocks.

# title herez
    TITLE = "LOGO DASH"
#hmm
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

    BINDINGS = [
        ("q", "quit", "Quit Game"), #keybindz for quitting
        ("r", "reset", "Reset Position"),#keybindz for quitting
    ]

    MAP_WIDTH = 60 #map specification width
    MAP_HEIGHT = 12#map specification height 

    LEVEL_MAP = [  # Za actual mappp
        "............................................................",
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
    console_msg = reactive(
        "Welcome to Logo Dash!."
    )

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="game-layout"):
            yield Static(id="screen-render")
            yield Static(id="console-log")
            yield Input(
                placeholder="Enter command (e.g., fd 5, bk 2, jp)...", #command palette
                id="cmd-input",
            )

        yield Footer()

    def on_mount(self) -> None:
        self.render_map()
        self.query_one("#cmd-input", Input).focus()

    def render_map(self) -> None:
        """Render the map and player."""

        display_lines = []

        for y, line in enumerate(self.LEVEL_MAP):
            render_line = ""

            for x, char in enumerate(line):
                if x == self.player_x and y == self.player_y:
                    render_line += "[b][yellow]■[/][/]"
                elif char == "#":
                    render_line += "[white]█[/]"
                elif char == "^":
                    render_line += "[red]▲[/]"
                else:
                    render_line += " "

            display_lines.append(render_line)

        self.query_one("#screen-render", Static).update(
            "\n".join(display_lines)
        )

    def watch_player_x(self, _: int) -> None:
        self.render_map()

    def watch_player_y(self, _: int) -> None:
        self.render_map()

    def watch_console_msg(self, msg: str) -> None:
        self.query_one("#console-log", Static).update(f"> {msg}")

    def action_reset(self) -> None:
        self.player_x = 2
        self.player_y = 9
        self.console_msg = (
            "Game reset. Try planning your movements carefully!"
        )

    def is_valid_position(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.MAP_WIDTH
            and 0 <= y < self.MAP_HEIGHT
        )

    def get_tile(self, x: int, y: int) -> str:
        if not self.is_valid_position(x, y):
            return "#"
        return self.LEVEL_MAP[y][x]

    def apply_gravity(self) -> None:
        """Drop player if there is no platform beneath."""

        below_y = self.player_y + 1

        if below_y < self.MAP_HEIGHT:
            if self.get_tile(self.player_x, below_y) == ".":
                self.player_y = 9

    def check_collisions(self) -> None:
        self.player_x = max(0, min(self.player_x, self.MAP_WIDTH - 1))
        self.player_y = max(0, min(self.player_y, self.MAP_HEIGHT - 1))

        current_tile = self.get_tile(self.player_x, self.player_y)

        if current_tile == "^":
            self.console_msg = (
                "[blink][red]CRASHED! Press R to reset.[/][/]"
            )
            self.notify(
                "You exploded on a spike!",
                severity="error",
            )

        elif current_tile == "#":
            self.player_y = max(0, self.player_y - 1)
            self.console_msg = "Blocked by terrain feature!" #to make players actually stay and not get out of the map

    def execute_command(self, raw_cmd: str) -> None:
        parts = raw_cmd.strip().lower().split()

        if not parts:
            return

        cmd = parts[0]

        steps = 1
        if len(parts) > 1 and parts[1].isdigit():
            steps = int(parts[1])

        if cmd in ("fd", "forward"): #to move ahead
            self.player_x += steps
            self.console_msg = f"Moved forward {steps} blocks."

        elif cmd in ("bk", "back"): #to move back
            self.player_x -= steps
            self.console_msg = f"Moved backward {steps} blocks."

        elif cmd in ("jp", "jump"): # to jump ofc
            self.player_y = max(0, self.player_y - 2)
            self.player_x += 3
            self.console_msg = "Executed jump vector!"

        else:
            self.console_msg = (
                f"[red]Unknown command:[/] '{cmd}'. "
                "Use fd, bk, or jp."
            )
            return

        self.check_collisions()
        self.apply_gravity()
        self.check_collisions()

    def on_input_submitted(
        self,
        event: Input.Submitted,
    ) -> None:
        if event.value:
            self.execute_command(event.value)
            self.query_one("#cmd-input", Input).value = ""


if __name__ == "__main__":
    LogoDashApp().run()