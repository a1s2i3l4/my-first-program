
import random

# Game data
player_health = 100
player_inventory = []
cave_rooms = {
    'entrance': {'description': 'You are at the cave entrance.', 'exits': ['north', 'east']},
    'north': {'description': 'You are in a dark room.', 'exits': ['south', 'west']},
    'east': {'description': 'You found a treasure!', 'exits': ['west']},
    'dragon_room': {'description': 'You see a fierce dragon!', 'exits': ['north']}
}

# Game loop
while True:
    # Get player input
    command = input('> ').lower()

    # Handle movement
    if command in ['north', 'south', 'east', 'west']:
        current_room = cave_rooms['entrance']
        if command in current_room['exits']:
            current_room = cave_rooms[command]
            print(current_room['description'])
        else:
            print("You can't go that way!")

    # Handle treasure collection
    elif command == 'take treasure':
        if 'treasure' in current_room:
            player_inventory.append('treasure')
            print("You collected a treasure!")

    # Handle dragon battle
    elif command == 'fight dragon':
        if 'dragon' in current_room:
            player_health -= 20
            print("You fought the dragon and lost 20 health!")
            if player_health <= 0:
                print("Game over!")

    # Handle invalid input
    else:
        print("Invalid command!")

