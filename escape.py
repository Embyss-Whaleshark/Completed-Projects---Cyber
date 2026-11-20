import random
manor = r"""
                ( )
                    |
                .-"-.
                /     \
        _____/_______\_____
       /  _   _     _   _  \
      /  |_| |_|   |_| |_|  \
     /_______________________\

      |   _    _____    _   |
      |  |_|  |  |  |  |_|  |
      |       |  |  |       |
    __|_______|__|__|_______|__
   /___________________________\
"""
# Paste your completed Part 3 solution here before extending the game for Part 4.
# House map
#             |----------|-----------|------------|
# (unlock w/  |          | (unlock w/| *Hint      |
#  Key 2      |          |   Key 1)      Code 2*  |
#   & Puzzle) |          |           |            |
#  Front Door | Bedroom  X Bathroom  |  Garage    X   (Unlock w/
#             |          |   *Key 2* |            |     Key 3 & Code 2)
#   |----X----|---    ---|-----------|------------|
#   |         |          |  *Key 3*  | Backyard   |
#   | Kitchen   Hallway  | Secret      *rand item*|
#   |         |   *Key 1*|    Garden |            |
#   |---------|----  ----|-----------|-----  -----|-------------|
#             |          | Secret    | Shed       | Spare       |
#             |   Tunnel x     room               | Storeroom   |
#             |*Puzzle 1*|           |  *Hint*    x(Code lock 1)|
#             |----------|-----------|------------|-------------|

rooms = {
    "Bedroom": {"pathways": {"d": "Bathroom", "s": "Hallway"}, "open_with": ""},
    "Hallway": {"pathways": {"w": "Bedroom", "a": "Kitchen", "s": "Tunnel"}, "open_with": ""},
    "Bathroom": {"pathways": {"a": "Bedroom", "d": "Garage"}, "open_with": "Key 1"},
    "Kitchen": {"pathways": {"d": "Hallway", "w": "Front_Door"}, "open_with": ""},
    "Front_Door": {"pathways": {"s": "Kitchen"}, "open_with": {"Key 2", "puzzle 1"}},
    "Garage": {"pathways": {"a": "Bathroom", "d": "Back_Door"}, "open_with": ""}, 
    "Tunnel": {"pathways": {"w": "Hallway", "d": "Secret Room"}, "open_with": ""},
    "Secret Room": {"pathways": {"a": "Tunnel", "d": "Shed"}, "open_with": "puzzle 1"},
    "Shed": {"pathways": {"a": "Secret Room", "w": "Backyard", "d": "Spare Storeroom"}, "open_with": ""},
    "Spare Storeroom": {"pathways": {"a": "Shed"}, "open_with": "code 1"},
    "Backyard": {"pathways": {"a": "Secret Garden", "s": "Shed"}, "open_with": ""},
    "Secret Garden": {"pathways": {"d": "Backyard"}, "open_with": "puzzle 2"},
    "Back_Door": {"pathways": {"a": "Garage"}, "open_with": {"Key 3", "code 2"}},
}

pickable_objects = {
    "Key 1": {"location": "Hallway", "picked": False},
    "Key 2": {"location": "Bathroom", "picked": False},
    "Key 3": {"location": "Secret Garden", "picked": False},
}

puzzles = {
    "puzzle 1": {"location": "Tunnel", "solved": False, "puzzle": "01010011 01100101 01100011 01110010 01100101 01110100", "answer": "secret"},
    "puzzle 2": {"location": "Kitchen", "solved": False, "puzzle": "I have keys but no locks. I have space but no room. What am I?", "answer": "keyboard"},
}

unlock_codes = {
    "code 1": {"location": "Spare Storeroom", "code": "0826", "unlocked": False},
    "code 2": {"location": "Back_Door", "code": "2110", "unlocked": False},
}

hints = {
    "hint1": {"location": "Shed", "hint": "Code 1 is the 4 digit month/year we started the Fall Semester"},
    "hint2": {"location": "Garage", "hint": "Code 2 is the 4 digit course ID number"},
}

rand_item = ["puzzle solver", "magnet", "compass"]

item_effects = {
    "puzzle solver": "All puzzles are automatically solved",
    "magnet": "All keys have been automatically collected",
    "compass": "All codes are automatically solved"
}
random_item_picked = False

START_LOCATION = random.choice([
    room for room in rooms
    if rooms[room]["open_with"] == ""
    and "Secret" not in room
    and room not in ["Front_Door", "Back_Door"]
])

def print_location(location: str) -> None:
    if location in rooms:
        print(f'You are in the {location}.')
    else:
        print("Unknown location.")
        
def get_directions(location: str) -> dict[str, str]:
    return rooms.get(location, {}).get("pathways", {})

def find_room_by_direction(location: str, direction: str) -> str:
    if location not in rooms:
        print("Unknown location.")
        return location
    pathways = rooms.get(location, {}).get("pathways", {})
    if direction in pathways:
        return pathways[direction]
    else:
        print('Invalid direction. Try again.')
        return location

def find_random_item(location: str) -> None:
    global random_item_picked

    if location == "Backyard" and not random_item_picked:
        random_item = random.choice(rand_item)
        random_item_picked = True

        print(f"You found a {random_item}!")
        print(item_effects[random_item])

        if random_item == "puzzle solver":
            for puzzle in puzzles.values():
                puzzle["solved"] = True
        elif random_item == "magnet":
            for key in pickable_objects.values():
                key["picked"] = True
                print("The magnet has collected all 3 keys!")
        elif random_item == "compass":
            for code in unlock_codes.values():
                code["unlocked"] = True

def check_requirement(requirement: str) -> bool:
    #checks  whether the player has a required key
    if requirement in pickable_objects:
        return pickable_objects[requirement]["picked"]

    #checks whether a required puzzle is solved
    if requirement in puzzles:
        if puzzles[requirement]["solved"]:
            return True
        
        answer = input(f"Solve {requirement}: ").strip().lower()

        if answer == puzzles[requirement]["answer"]:
            puzzles[requirement]["solved"] = True
            print("Correct!! The puzzle is solved. You may continue.")
            return True
        else:
            print ("Incorrect answer. You may not pass.")
            return False

    #Checks whether a requrired code is unlocked
    if requirement in unlock_codes:
        if unlock_codes[requirement]["unlocked"]:
            return True
        code = input(f'Enter {requirement}: ').strip()

        if code == unlock_codes[requirement]["code"]:
            unlock_codes[requirement]["unlocked"] = True
            print("Correct code! You have opened the lock.")
            return True
        else:
            print("Incorrect. Try again.")
            return False

def has_key_for_room(room_id: str) -> bool:
    if room_id not in rooms:
        return False

    requirements = rooms[room_id]["open_with"]

    if requirements == "":
        return True

    # Converts a single requirement into a set
    if isinstance(requirements, str):
        requirements = {requirements}

    # Every requirement must be satisfied
    for requirement in requirements:
        if not check_requirement(requirement):
            return False

    return True

def show_hint(location: str) -> None:
    for hint in hints.values():
        if hint["location"] == location:
            print(f'Hint: {hint["hint"]}')

def explore_room(location: str) -> None:
    for key, info in pickable_objects.items():
        if info["location"] == location and not info["picked"]:
            info["picked"] = True
            print(f'You found {key}.')

def explore_puzzle(location: str) -> None:
    for name, info in puzzles.items():
        if info["location"] == location and not info["solved"]:
            print(f'You discovered {name}!')
            print(info["puzzle"])

def game_loop(location: str) -> None:
    """
    Main game loop handling room navigation.
    Parameters:
    location (str): The starting location of the player.
    The function continuously prints the current location, retrieves possible directions,
    and prompts the player to choose a direction to move. The loop continues until the 
    player decides to exit by entering 'x'. The location is updated based on the player's 
    chosen direction.
    The function relies on the following helper functions:
    - print_location(location): Prints the current location.
    - get_directions(location): Retrieves possible directions from the current location (no printing).
    - The game loop is responsible for printing: "You can go: {<pathways dict>}" using the value returned by get_directions.
    - find_room_by_direction(location, chosen_direction): Finds the next room based on the current location and chosen direction.
    When the player exits, a message "Exited the game." is printed.
    """
    while True:    
        print_location(location)
        explore_room(location)
        find_random_item(location)
        show_hint(location)
        explore_puzzle(location)

        available_directions = get_directions(location)
        print(f"You can go: {available_directions}")
        chosen_direction = input("Where do you want to go? ('x' to exit) ").lower()
        if chosen_direction  == 'x':
            print("Exited the game.")
            break
        
        next_room = find_room_by_direction(location, chosen_direction)
        if next_room == location:
            continue

        if  has_key_for_room(next_room):
            location = next_room

            if location == "Front_Door" or location == "Back_Door":
                print("You have escaped!")
                print("Congratulations!! You escaped... Don't come back")
                break
        else:
            print(f"You cannot enter this room yet... Go find {rooms["open_with"]} then come back.")


def start_game() -> None:
    """
    Start the game.

    This function initializes the Escape Game by printing the game title to the console.
    It serves as the entry point for the game.
    """

    print("         Lakewood Manor: Grandma's Secret           ")
    
    print(manor)
    print("After grandma's funeral, a letter arrived at your house... 'There's something in my manor. First one to find it keeps the manor.")
    print("You head to the manor, as you walk into the front yard, a random trap door opens, dropping you into a random room of the house.")
    print("All the doors leading out are locked.")
    print("You must find the secrets of the manor to get out.")
    print()


if __name__ == "__main__":
    start_game()
    game_loop(START_LOCATION)