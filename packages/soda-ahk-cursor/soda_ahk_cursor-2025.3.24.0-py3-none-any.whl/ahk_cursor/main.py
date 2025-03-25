from pathlib import Path
from multiprocessing import Process
import multiprocessing
import time
from fastapi import FastAPI

from ahk_cursor.stop import stop
from ahk_cursor.move_cursor import main as move_cursor
from ahk_cursor.gen import gen
from ahk_cursor.check_running import check_running


# sending checking reuslts
queue_status = multiprocessing.Queue()
# signals
queue_signals = multiprocessing.Queue()

CURRENT = Path(__file__).resolve().parent


def check_running_loop(queue: multiprocessing.Queue, queue2: multiprocessing.Queue):
    while True:
        x = check_running()
        if x == -1:
            queue.put("stopped")
        else:
            queue.put("running")

        if not queue2.empty():
            sig = queue2.get()
            print(sig)
            if sig == "shutdown":
                break
        time.sleep(1.2)


queue4 = multiprocessing.Queue()


def server(queue_signals, queue4):
    app = FastAPI()

    @app.get("/force_run")
    def hello_world():
        queue_signals.put("force_run")
        return "111"

    @app.get("/shutdown_server")
    def shutdown():
        queue_signals.put("shutdown")
        queue4.put("shutdown")
        return "222"

    import uvicorn

    uvicorn.run(app, port=12345)


def server_checker(queue_status, queue_signals, queue4):
    p = Process(target=server, args=(queue_signals, queue4))
    p.start()

    while True:
        if queue4.empty():
            time.sleep(0.5)
        else:
            p.terminate()
            queue_signals.put("shutdown")
            break


def main():
    stop()

    gen()

    t2 = Process(target=move_cursor, args=[queue_status, queue_signals])
    t2.start()

    t3 = Process(target=server_checker, args=[queue_status, queue_signals, queue4])
    t3.start()

    t = Process(
        target=check_running_loop,
        args=(
            queue_status,
            queue_signals,
        ),
    )
    t.start()
    t.join()


if __name__ == "__main__":
    main()
