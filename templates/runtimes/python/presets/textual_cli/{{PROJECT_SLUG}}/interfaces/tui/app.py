
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Static


class DashboardApp(App[None]):
    TITLE = {{PROJECT_NAME_LITERAL}}
    SUB_TITLE = "Textual cockpit baseline"
    BINDINGS = [
        Binding("q", "quit", "Sair"),
        Binding("r", "notify_refresh", "Refresh"),
    ]
    CSS = """
    Screen {
        align: center middle;
        background: #132726;
    }

    #hero {
        width: 72;
        padding: 1 2;
        border: round #4fd3d0;
        background: #1a2f2e;
        color: #edf4ef;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(
            "Preencha a fonte de dados operacional antes de crescer a TUI.\n"
            "Use doctor para smoke e mantenha a regra de negocio fora da interface.",
            id="hero",
        )
        yield Footer()

    def action_notify_refresh(self) -> None:
        self.notify("refresh manual", timeout=1.5)


def build_app() -> DashboardApp:
    return DashboardApp()
