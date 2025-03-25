import requests


def stop():
    try:
        r = requests.get("http://localhost:12345/shutdown_server", timeout=0.5)
    except Exception as e:
        print("timeout", e)
    else:
        print(r.content)


if __name__ == "__main__":
    stop()
