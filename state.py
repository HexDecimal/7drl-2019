import tcod.event

import actions
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
        g.console.print(0, 0, "Hello zone!")


class Game(State):
    WAIT_KEYS = (
        tcod.event.K_PERIOD,
        tcod.event.K_KP_5,
    )
    DIR_KEYS = {
        tcod.event.K_LEFT: (-1, 0),
        tcod.event.K_RIGHT: (1, 0),
        tcod.event.K_UP: (0, -1),
        tcod.event.K_DOWN: (0, 1),
        tcod.event.K_PAGEUP: (-1, -1),
        tcod.event.K_PAGEDOWN: (-1, 1),
        tcod.event.K_HOME: (1, -1),
        tcod.event.K_END: (1, 1),

        tcod.event.K_KP_4: (-1, 0),
        tcod.event.K_KP_6: (1, 0),
        tcod.event.K_KP_8: (0, -1),
        tcod.event.K_KP_2: (0, 1),
        tcod.event.K_KP_7: (-1, -1),
        tcod.event.K_KP_1: (-1, 1),
        tcod.event.K_KP_9: (1, -1),
        tcod.event.K_KP_3: (1, 1),

        ord("h"): (-1, 0),
        ord("l"): (1, 0),
        ord("k"): (0, -1),
        ord("j"): (0, 1),
        ord("y"): (-1, -1),
        ord("b"): (-1, 1),
        ord("u"): (1, -1),
        ord("n"): (1, 1),
    }

    def on_enter(self) -> None:
        g.zone.simulate()

    def on_draw(self) -> None:
        g.zone.render(g.console)
        self.draw_ui()
        super().on_draw()

    def draw_ui(self) -> None:
        ui_console = tcod.console.Console(20, g.console.height, order="F")
        ui_console.draw_rect(0, 0, 1, ui_console.height, ord("│"))
        ui_console.print(1, 0, f"Time: {g.zone.tqueue.time}")
        ui_console.print(1, 1, f"Pos: {g.player.location.xyz}")

        ui_console.blit(g.console, g.console.width - ui_console.width, 0,
                        bg_alpha=0.9)

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        assert g.zone.player
        player = g.zone.player
        if event.sym in self.DIR_KEYS:
            actions.Bump(player, (*self.DIR_KEYS[event.sym], 0)).invoke()
        elif event.sym in self.WAIT_KEYS:
            actions.Wait(player).invoke()
        else:
            print(event)
        g.zone.simulate()
