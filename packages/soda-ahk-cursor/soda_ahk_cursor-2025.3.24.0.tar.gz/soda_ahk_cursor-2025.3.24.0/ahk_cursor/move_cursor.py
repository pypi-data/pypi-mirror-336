import time
import pyautogui
from pathlib import Path
import multiprocessing

CURRENT = Path(__file__).resolve().parent


def move_cursor():
    x, y = pyautogui.position()
    for i in range(5):
        pyautogui.moveTo(x + 1, y, 0.1)
        time.sleep(0.1)
        x, y = pyautogui.position()
    for i in range(5):
        pyautogui.moveTo(x - 1, y, 0.1)
        time.sleep(0.1)
        x, y = pyautogui.position()


CURRENT.joinpath("running").write_text("a", encoding="utf8")


def move_cursor_impl():
    while True:
        try:
            move_cursor()
        except Exception as e:
            print(e)


def main(queue1: multiprocessing.Queue = None, queue2: multiprocessing.Queue = None):
    t = multiprocessing.Process(target=move_cursor_impl)
    while True:
        if queue1 is not None and queue2 is not None:
            if not queue1.empty():
                x = queue1.get_nowait()
                if x == "stopped":
                    if t.is_alive():
                        t.terminate()
                elif x == "running":
                    if not t.is_alive():
                        t = multiprocessing.Process(target=move_cursor_impl)
                        t.start()

            if not queue2.empty():
                signal = queue2.get_nowait()
                if signal == "shutdown":
                    break
                if signal == "force_run":
                    move_cursor()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
