
from {{PROJECT_SLUG}}.interfaces.http.app import create_app


def test_create_app() -> None:
    app = create_app()
    assert app.title == {{PROJECT_NAME_LITERAL}}
