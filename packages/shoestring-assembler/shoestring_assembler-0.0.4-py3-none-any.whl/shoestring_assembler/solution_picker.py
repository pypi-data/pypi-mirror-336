from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, OptionList, Label, Markdown
from textual.widgets.option_list import Option
from textual import on

import urllib.request
import yaml

INSTRUCTIONS_MULTI_PROVIDER = """
### Select which solution you want to download.
Use the `up` and `down` arrows to move up and down each provider's list.

Use `tab` and `shift + tab` to move between providers.

Use `Enter` to select the solution you want.

Press `q` to exit.
"""

INSTRUCTIONS_SINGLE_PROVIDER = """
### Select which solution you want to download.
Use the `up` and `down` arrows to move up and down the list.

Use `Enter` to select the solution you want.

Press `q` to exit.
"""


class SolutionList(OptionList):
    def __init__(self, *content, provider=None, solution_list={}, **kwargs):
        super().__init__(*content, **kwargs)
        self.solution_list = solution_list
        self.provider = provider

    def on_mount(self):
        for index, solution in enumerate(self.solution_list):
            self.add_option(Option(solution["name"], id=f"{self.provider}@{index}"))
        return super().on_mount()


class SolutionPickerApp(App):

    def __init__(self, provider_list, **kwargs):
        super().__init__(**kwargs)
        self.provider_list = provider_list

    BINDINGS = [("q", "exit", "Exit")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Markdown(INSTRUCTIONS_MULTI_PROVIDER if len(self.provider_list["providers"]) > 1 else INSTRUCTIONS_SINGLE_PROVIDER)
        for tag, values in self.provider_list["providers"].items():
            yield Label(values["name"])
            yield SolutionList(provider=tag, solution_list=values["solutions"])

    def on_mount(self):
        self.title = "Select a Shoestring Solution"

    def action_exit(self) -> None:
        self.exit()

    @on(OptionList.OptionSelected)
    def handle_selected(self, event):
        id = event.option.id
        provider, index = id.split("@")
        result = self.provider_list["providers"][provider]["solutions"][int(index)]
        self.exit(result)


if __name__ == "__main__":
    # fetch solution list
    with urllib.request.urlopen(
        "https://github.com/DigitalShoestringSolutions/solution_list/raw/refs/heads/main/list.yaml"
    ) as web_in:
        content = web_in.read()
        provider_list = yaml.safe_load(content)
    result = SolutionPickerApp(provider_list).run()
    print(result)
