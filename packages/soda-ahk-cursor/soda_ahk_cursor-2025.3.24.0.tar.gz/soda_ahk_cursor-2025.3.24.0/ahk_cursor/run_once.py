import requests

try:
    r = requests.get("http://localhost:12345/force_run")
except requests.Timeout:
    print("timeout")
else:
    print(r.content)