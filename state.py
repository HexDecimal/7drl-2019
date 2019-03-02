import tcod.event

import g


class StateExit(Exception):
    pass


class State(tcod.event.EventDispatch):

    def activate(self) -> None:
        self.on_enter()
        try:
            while True:
                self.on_draw()
                for event in tcod.event.wait():
                    self.dispatch(event)
        except StateExit:
            pass
        finally:
            self.on_exit()

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def on_draw(self) -> None:
        tcod.console_flush()

    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()


class MainMenu(State):

    def on_enter(self) -> None:
        g.console.print(0, 0, "Hello world!")
