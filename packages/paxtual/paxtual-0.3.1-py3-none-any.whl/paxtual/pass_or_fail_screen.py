from textual.app import ComposeResult
from textual.widgets import SelectionList, Button
from textual.widgets.selection_list import Selection
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual import work, on
import pandas as pd
import os
import datetime
from .paxterms import PaxTerms
from .get_wsid import get_workstation_id
from .eval_2_linkscreen import Link_Screen

class FailedSerialSelectionScreen(ModalScreen):
    
    CSS_PATH = "css_lib/poll.tcss"

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
    
    def get_failed_serials(self) -> list[dict[str, str]]:
        """Returns a list of dictionaries, each containing serial number, username, and result."""
        selection_list = self.query_one(SelectionList)
        selected_values = selection_list.selected
        username = f"{os.getlogin()}@north.com"
        wsid = get_workstation_id()
        
        results = []

        for serial_number in self.df["serialNo"]:
            results.append({
                "serialNo": serial_number,
                "username": username,
                "workstation": wsid,
                "results": "Fail" if serial_number in selected_values else "Pass",
                "date": str(datetime.datetime.today().strftime('%m.%d.%Y %H:%M:%S'))
            })
        return results

    @on(Button.Pressed)
    @work
    async def complete(self, event: Button.Pressed) -> None:
        if event.button.id == "complete":
            results = self.get_failed_serials()
            res_df = pd.DataFrame(results)
            m_df = self.df.merge(res_df, on="serialNo", how="left")

            if (m_df["results"] == "Fail").any():
                await self.app.push_screen_wait(Link_Screen())
            else:
                self.notify(str(m_df))
            self.dismiss(m_df)
