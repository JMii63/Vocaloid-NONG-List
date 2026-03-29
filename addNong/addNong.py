import json
import re
from pathlib import Path
from rich import print_json
from time import time

def inputNotEmpty(prompt: str) -> str:
    while True:
        userInput = input(f"{prompt}: ")
        if not userInput or userInput.isspace():
            print("Please do not put an empty value, ty :)")
            continue

        return userInput

def inputNum(prompt: str) -> int:
    while True:
        userInput = inputNotEmpty(prompt)
        if not userInput.isdigit():
            print("Please put a valid number")
            continue

        return int(userInput)

def inputYesNo(prompt: str) -> bool:
    while True:
        userInput = inputNotEmpty(f"{prompt} (y/n)")
        userInput = userInput.lower()

        if userInput == "y":
            return True
        elif userInput == "n":
            return False
        else:
            print("Please put a valid input (y/n)")

def main() -> None:
    name = inputNotEmpty("Song Name")
    author = inputNotEmpty("Song Author")
    url = inputNotEmpty("Download URL")
    startOffset = inputNum("Start Offset")
    replaces: list[int] = []

    while True:
        print("Songs IDs this NONG will replace:")
        if replaces:
            for r in replaces:
                print(r, end=" ") # Doesn't print any newline at the end
            print() # Prints a newline

            addMore = inputYesNo("Do you want to add another song ID?")
            if not addMore:
                break

        newReplacement = inputNum("Song ID to replace")
        replaces.append(newReplacement)

    id = re.sub(r"[^a-zA-Z0-9 ]", "", name.lower())
    id = id.replace(" ", "-")

    data = {
        "name": name,
        "artist": author,
        "startOffset": startOffset,
        "url": url,
        "songs": replaces
    }

    print("\nThis will add the following NONG to the index:")
    print_json(json.dumps(data))

    addToIndex = inputYesNo("Do you want to continue?")
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
            print("Could not find index file")
        except json.JSONDecodeError as e:
            print(f"Could not decode JSON: e")

if __name__ == '__main__':
    main()