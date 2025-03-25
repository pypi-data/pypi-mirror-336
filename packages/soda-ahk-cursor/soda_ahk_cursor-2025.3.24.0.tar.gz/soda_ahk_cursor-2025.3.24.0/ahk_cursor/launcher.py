from ahk_cursor.gen import gen, script
import os
from ahk_cursor.autostart import create


def launcher():
    gen()
    # os.startfile(CURRENT.joinpath("stop.ahk"))
    create(script)
    os.startfile(str(script))


if __name__ == "__main__":
    launcher()
