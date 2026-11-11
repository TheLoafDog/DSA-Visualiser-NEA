"""Headless smoke test: the main window builds and runs an event-loop tick."""


def test_app_builds_and_ticks(display):
    import Main

    app = Main.App()
    try:
        app.update()
        assert app.main_page.winfo_exists()
    finally:
        app.destroy()
