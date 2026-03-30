import json
import questionary
import re
import sys
from pathlib import Path
from rich import print_json, print
from time import time

STYLE = questionary.Style([
    ("question", "nobold"),
    ("answer", "nobold fg:pink"),
    ("qmark", "bold fg:purple")
]);

def notEmpty(x: str) -> bool | str:
    if len(x.strip()) == 0:
        return "Please do not put an empty value, ty :)"
    return True

def isNumber(x: str) -> bool | str:
    empty = notEmpty(x)
    if isinstance(empty, str):
        return empty

    if not x.isdigit():
        return "Please put a valid number"

    return True

def ask(*args, **kwargs) -> str:
    answer = questionary.text(*args, **kwargs, style=STYLE).ask()
    if answer is None:
        sys.exit(130)
    return answer

def askYesNo(prompt: str) -> bool:
    ok = questionary.confirm(prompt, default=False, style=STYLE).ask()
    if ok is None:
        sys.exit(130)
    return ok

def main() -> None:
    name = ask("Song Name:", validate=notEmpty)
    author = ask("Song Author:", validate=notEmpty)
    url = ask("Download URL:", validate=notEmpty)
    startOffset = ask("Start Offset:", validate=isNumber)
    replaces: list[int] = []

    while True:
        songID = ask(
            "Song IDs this NONG will replace (leave empty to finish):",
            validate=lambda x: ((len(x.strip()) > 0 and x.isdigit()) or bool(replaces)) or "Please input at least one Song ID"
        )
        if songID.strip() == "":
            break
        replaces.append(int(songID.strip()))

    id = re.sub(r"[^a-zA-Z0-9 ]", "", name.lower())
    id = id.replace(" ", "-")

    data = {
        "name": name,
        "artist": author,
        "startOffset": startOffset,
        "url": url,
        "songs": replaces
    }

    print("[bold #c585c6]![/] This will add the following NONG to the index:")
    print_json(json.dumps(data))

    addToIndex = askYesNo("Do you want to continue?")
    if addToIndex:
        try:
            file = "in-game.json"
            root = Path.cwd()
            filePath = root / file
            if not filePath.exists():
                root = root.parent
                filePath = root / file

            with open(filePath, "r+") as f:
                index = json.load(f)
                index["lastUpdate"] = int(time()) # update 'lastUpdate'
                index["nongs"]["hosted"][id] = data

                f.seek(0)
                json.dump(index, f, indent=2)
                f.truncate()
        except FileNotFoundError:
            print("[bold red]ERROR: Could not find index file[/]")
        except json.JSONDecodeError as e:
            print(f"[bold red]Could not decode JSON: e[/]")

if __name__ == '__main__':
    main()