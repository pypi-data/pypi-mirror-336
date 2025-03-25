from textual.app import App, ComposeResult
from textual.widgets import Label, SelectionList, Button
from textual.widgets.selection_list import Selection
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual import work, on
import pandas as pd
from paxterms import PaxTerms

class FailedSerialSelectionScreen(ModalScreen):
    
    CSS_PATH = "poll.tcss"

    def __init__(self, df: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.df = df

    
    def create_selections(self) -> list[Selection]:
        selections = []
        for serial_number in self.df["serialNo"]:
            term = PaxTerms(serial_number)
            selections.append(Selection(prompt=f"{term.modelName} {serial_number}",value=serial_number))
        return selections
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            SelectionList(*self.create_selections()),
            Button("Complete", variant="primary", id = "complete", classes = "button")
        )
    
    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = "Select any terminal that failed testing or configuration:"
        self.query_one(SelectionList).border_subtitle = "Press Complete when done."
    
    def get_failed_serials(self) -> dict[str, str]:
        """Returns a dictionary of serial numbers and their pass/fail status."""
        selection_list = self.query_one(SelectionList)
        selected_values = selection_list.selected
        results = {}

        for serial_number in self.df["serialNo"]:
            if serial_number in selected_values:
                results[serial_number] = "Fail"
            else:
                results[serial_number] = "Pass"
        return results

    
    @on(Button.Pressed)
    @work
    async def complete(self, event: Button.Pressed) -> None:
        if event.button.id == "complete":

            results = self.get_failed_serials()
            self.app.notify(f"\nResults:{results}")

                        
class Fail_App(App):

    @work
    async def on_mount(self): 
        data = {"serialNo": ["0822896086", "1850858327", "2270003282", "1240424282", "1340030727"]}
        df = pd.DataFrame(data)
        await self.push_screen_wait(FailedSerialSelectionScreen(df))


if __name__ == "__main__":

    app = Fail_App()
    app.run()