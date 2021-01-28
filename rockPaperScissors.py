from typing import Dict, List, Set, Optional, Match
from random import randrange
import re 
import anton 
import sys 
from termcolor import colored 


def format_str(string: str) -> str:
    '''Uses bit operations to convert the first letter to uppercase'''
    chars: List[str] = list(string)
    chars[0] = chr(ord(chars[0]) & ~32)

    return "".join(chars) 


def play_human(values: set) -> Optional[str]:
    move = anton.Commands().lower()
    if move == "quit":
        return None
    while move not in values:
        anton.speak("Sorry can you say that again")
        move = anton.Commands().lower()
        if move == "quit":
            return None
    return move 


def random_ai(values: list) -> str:
    index: int = randrange(3)

    return values[index]


def display(scores: List[int], val1: str, val2: str) -> None:
    print()
    print(f"Player 1 played {format_str(val1)}")
    print(f"Player 2 played {format_str(val2)}")
    print()
    print(colored(f"Player 1 -->  {scores[0]}     {scores[1]}  <-- Player 2", color="magenta"))


def display_gui(scores: List[int], val1: str, val2: str) -> None:
    pass 

def game(limit: int) -> None:

    anton.speak('''To play the game say either rock, paper or scissors each round. 
    The winner is the first to reach the limit''')

    anton.speak("You may begin")

    moves: Dict[str, str] = {
        "rock" : "scissors",
        "scissors" : "paper",
        "paper" : "rock"
    }

    moves_set: Set[str] = {v for v in moves}
    moves_list: List[str] = [v for v in moves]
  
    over: bool = False
    scores: list = [0,0]

    while not over:
        print()

        # player 1 
        val1: Optional[str] = play_human(moves_set) 
        if val1 is None:
            break  

        # player 2 
        val2: str = random_ai(moves_list)

        if moves[val1] == val2:
            scores[0] += 1
        elif moves[val2] == val1:
            scores[1] += 1

        # display scores 
        display(scores, val1, val2)
        display_gui(scores, val1, val2)

        # check if game over 
        if max(scores) == limit:
            over = True 

    print()

    if scores[0] > scores[1]:
        print(colored("Winner is player 1", color = "green"))
        anton.speak("Game over. The winner is player 1") 
    elif scores[1] > scores[0]:
        print(colored("Winner is player 2", color = "green"))
        anton.speak("Game over. The winner is player 2")
    else:
        print(colored("Draw!", color = "green"))
        anton.speak("Game over. It is a draw")
    
if __name__ == '__main__':
    pattern: str = (r'([0-9]+){1}')
    anton.speak("How many rounds would you like?")
    val: str = anton.Commands()
    if val == "quit":
        sys.exit()
    match: Optional[Match[str]] = re.match(pattern, val)
    while not match or match.group(0) == '0':
        anton.speak("Please say a valid number of rounds")
        val = anton.Commands()
        match = re.match(pattern, val)

    limit: int = int(match.group(0))

    game(limit)

  
    