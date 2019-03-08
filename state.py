from __future__ import annotations

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
        tcod.event.K_CLEAR,
    )
    DIR_KEYS = {
        tcod.event.K_LEFT: (-1, 0),
        tcod.event.K_RIGHT: (1, 0),
        tcod.event.K_UP: (0, -1),
        tcod.event.K_DOWN: (0, 1),
        tcod.event.K_HOME: (-1, -1),
        tcod.event.K_END: (-1, 1),
        tcod.event.K_PAGEUP: (1, -1),
        tcod.event.K_PAGEDOWN: (1, 1),

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
    CANCEL_KEYS = [
        tcod.event.K_BACKSPACE,
        tcod.event.K_ESCAPE,
    ]
    PICKUP_KEYS = [
        ord("g"),
        ord(","),
    ]

    def on_enter(self) -> None:
        g.model.zone.simulate()

    def on_draw(self) -> None:
        g.model.zone.render(g.console)
        self.draw_ui()
        tcod.console_flush()

    def draw_ui(self) -> None:
        ui_console = tcod.console.Console(20, 20, order="F")
        ui_console.draw_rect(0, 0, 1, ui_console.height, ord("│"))
        ui_console.draw_rect(1, ui_console.height - 1,
                             ui_console.width, 1, ord("─"))
        ui_console.draw_rect(0, ui_console.height - 1, 1, 1, ord("└"))
        ui_console.print(1, 0, f"Time: {g.model.zone.tqueue.time}")
        ui_console.print(1, 1, f"Pos: {g.model.player.location.xyz}")
        room_name = g.model.zone.room_types[
            g.model.zone.data["room_id"][g.model.player.location.xyz]
        ]
        ui_console.print(1, 2, f"{room_name}")

        ui_console.blit(g.console, g.console.width - ui_console.width, 0,
                        bg_alpha=0.9)

        log_console = tcod.console.Console(80, 10, order="F")
        log_console.draw_rect(0, 0, log_console.width, 1, ord("─"))
        log_console.draw_rect(log_console.width - 1, 1,
                              1, log_console.height, ord("│"))
        log_console.draw_rect(log_console.width - 1, 0, 1, 1, ord("┐"))
        y = log_console.height
        for log in reversed(g.model.log):
            y -= log_console.get_height_rect(0, y, 0, 0, log)
            if y < 0:
                break
            log_console.print_rect(0, y, 0, 0, log)

        log_console.blit(g.console, 0, g.console.height - log_console.height,
                         bg_alpha=0.9)

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        assert g.model.controlled
        player = g.model.controlled
        if event.sym in self.DIR_KEYS:
            actions.Bump(player, (*self.DIR_KEYS[event.sym], 0)).invoke()
        elif event.sym in self.WAIT_KEYS:
            actions.Wait(player).invoke()
        elif event.sym in self.CANCEL_KEYS:
            actions.ReturnControlToPlayer(player).invoke()
        elif event.sym in self.PICKUP_KEYS:
            actions.PickupGeneral(player).invoke()
        else:
            print(event)
        g.model.zone.simulate()
