from random import choice, randint
import re

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    arguments: list[str] = lowered.split(' ')

    try:
        if arguments[0] == 'roll':
            roll_result = get_roll(arguments[1:])
            return f'You rolled: {roll_result}'
    except ValueError:
        return 'Your argument doesn\'t follow #...d#... format!'

def get_roll(roll_input: list[str]) -> int:
    if len(roll_input) == 0:
        return randint(1,6) #1d6 is the default
    
    pattern: str = r'\d+d\d+'

    matches: re.Match[str] = re.match(pattern, roll_input[0])

    if matches:
        dice_input: list[str] =roll_input[0].split('d')
        num_dice: int = int(dice_input[0])
        dice_denomination: int = int(dice_input[1])

        running_total: int = 0
        for i in range(num_dice):
            running_total += randint(1, dice_denomination)
        
        return running_total
    else:
        raise ValueError('String does not follow #...d#... format')