import json, os

DIR = os.path.dirname(__file__)
TASKS_PATH = os.path.join(DIR, "tasks.json")

def load_tasks():
    with open(TASKS_PATH) as f:
        return json.load(f)