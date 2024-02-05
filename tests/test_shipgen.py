import sys

sys.path.append(".")

import procgen.shipgen

if __name__ == "__main__":
    ship = procgen.shipgen.Ship(0)

    print(ship.show())
