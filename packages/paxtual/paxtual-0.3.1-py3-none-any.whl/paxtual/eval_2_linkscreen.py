from textual.app import  ComposeResult, App
from textual.widgets import Static, Link, Button
from textual.screen import ModalScreen
from textual.containers import Grid
from textual import work, on

class Link_Screen(ModalScreen):

    CSS_PATH = "css_lib/confirm_screen.tcss"

    def compose(self) -> ComposeResult:
        yield Grid(
            Static("Failures detected.\nPlease click the link -->\nto record to Eval L2.", id = "question"),
            Link("Take me to Eval L2", url = "https://docs.google.com/forms/d/e/1FAIpQLScEdfy34d1eWRSKuyRcnti-MKc4FSwAb4VMN-WzO1sI1N1Lbg/viewform?usp=header",tooltip = "Click Here", id = "thing"),
            Button("Done", id = "done", variant = "primary")
            ,id = "prompt"
        )

    @on(Button.Pressed)
    @work
    async def back_to_thing(self, event: Button.Pressed):
        if event.button.id == "done":
            self.dismiss()


    