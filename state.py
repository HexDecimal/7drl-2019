from typing import Dict, Tuple

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
        tcod.console_flush()  # type: ignore

    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()


class MainMenu(State):

    def on_enter(self) -> None:
        g.console.print(0, 0, "Hello world!")


class Game(State):
    DIR_KEYS: Dict[int, Tuple[int, int]] = {
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
        g.world.simulate()

    def on_draw(self) -> None:
        g.console.clear()
        for y in range(g.console.height):
            for x in range(g.console.width):
                if g.world[x, y, 0].contents:
                    g.console.ch[x, y] = ord('@')
        super().on_draw()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        assert g.world.player
        player = g.world.player
        if event.sym in self.DIR_KEYS:
            new_loc = player.location.get_relative(*self.DIR_KEYS[event.sym])
            player.location = new_loc
            assert player.actor
            player.actor.schedule(100)
        else:
            print(event)
        g.world.simulate()
