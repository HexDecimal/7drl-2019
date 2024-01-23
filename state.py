from __future__ import annotations

import tcod.console
import tcod.event

import actions.common
import actions.inventory
import actions.robot
import g

WAIT_KEYS = (
    tcod.event.KeySym.COMMA,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
)
DIR_KEYS = {
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_9: (1, -1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.h: (-1, 0),
    tcod.event.KeySym.l: (1, 0),
    tcod.event.KeySym.k: (0, -1),
    tcod.event.KeySym.j: (0, 1),
    tcod.event.KeySym.y: (-1, -1),
    tcod.event.KeySym.b: (-1, 1),
    tcod.event.KeySym.u: (1, -1),
    tcod.event.KeySym.n: (1, 1),
}
CANCEL_KEYS = (
    tcod.event.KeySym.BACKSPACE,
    tcod.event.KeySym.ESCAPE,
)
PICKUP_KEYS = (
    tcod.event.KeySym.g,
    tcod.event.KeySym.PERIOD,
)


class StateExit(Exception):
    pass


class State(tcod.event.EventDispatch[None]):
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
        g.context.present(g.console)

    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()


class MainMenu(State):
    def on_enter(self) -> None:
        g.console.print(0, 0, "Hello zone!")


class Game(State):
    def on_enter(self) -> None:
        g.model.zone.simulate()

    def on_draw(self) -> None:
        g.model.zone.render(g.console)
        self.draw_ui()
        g.context.present(g.console)

    def draw_ui(self) -> None:
        ui_console = tcod.console.Console(20, 20, order="F")
        ui_console.draw_rect(0, 0, 1, ui_console.height, ord("│"))
        ui_console.draw_rect(1, ui_console.height - 1, ui_console.width, 1, ord("─"))
        ui_console.draw_rect(0, ui_console.height - 1, 1, 1, ord("└"))
        ui_console.print(1, 0, f"Time: {g.model.zone.tqueue.time}")
        ui_console.print(1, 1, f"Pos: {g.model.player.location.xyz}")
        room_name = g.model.zone.room_types[g.model.zone.data["room_id"][g.model.player.location.xyz]]
        ui_console.print(1, 2, f"{room_name}")

        ui_console.blit(g.console, g.console.width - ui_console.width, 0, bg_alpha=0.9)

        log_console = tcod.console.Console(80, 10, order="F")
        log_console.draw_rect(0, 0, log_console.width, 1, ord("─"))
        log_console.draw_rect(log_console.width - 1, 1, 1, log_console.height, ord("│"))
        log_console.draw_rect(log_console.width - 1, 0, 1, 1, ord("┐"))
        y = log_console.height
        for log in reversed(g.world[None].components["log", list[str]]):
            y -= tcod.console.get_height_rect(log_console.width, log)
            if y < 0:
                break
            log_console.print_box(0, y, 0, 0, log)

        log_console.blit(g.console, 0, g.console.height - log_console.height, bg_alpha=0.9)

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        assert g.model.controlled
        player = g.model.controlled
        if event.sym in DIR_KEYS:
            actions.common.Bump(player, (*DIR_KEYS[event.sym], 0)).invoke()
        elif event.sym in WAIT_KEYS:
            actions.common.Wait(player).invoke()
        elif event.sym in CANCEL_KEYS:
            actions.robot.ReturnControlToPlayer(player).invoke()
        elif event.sym in PICKUP_KEYS:
            actions.inventory.PickupGeneral(player).invoke()
        else:
            print(event)
        g.model.zone.simulate()
