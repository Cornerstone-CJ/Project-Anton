from typing import Dict, Callable, Union, List, Set
from random import randrange

def format_str(string: str) -> str:
    '''Uses bit operations to convert the first letter to uppercase'''
    chars: List[str] = list(string)
    chars[0] = chr(ord(chars[0]) & ~32)

    return "".join(chars) 


def play_human(values: set) -> str:
    move: str = input("Enter either Rock, Paper or Scissors: ").lower() 
    while move not in values:
        print("Enter a valid move")
        move = input("Enter either Rock, Paper or Scissors: ").lower() 
    
    return move 


def random_ai(values: list) -> str:
    index: int = randrange(3)

    return values[index]


def display(scores: List[int], val1: str, val2: str) -> None:
    print()
    print(f"Player 1 played {format_str(val1)}")
    print(f"Player 2 played {format_str(val2)}")
    print()
    print(f"Player 1 -->  {scores[0]}     {scores[1]}  <-- Player 2")


def game(limit: int, two_players: bool = False) -> None:
    func_map: Dict[str, Callable] = {
    "human" : play_human,
    "computer" : random_ai
    } 

    moves: Dict[str, str] = {
        "rock" : "scissors",
        "scissors" : "paper",
        "paper" : "rock"
    }

    moves_set: set = {v for v in moves}
    moves_list: list = [v for v in moves]
    values: Union[Set[str], List[str]] = moves_set if two_players else moves_list

    over: bool = False
    scores: list = [0,0]
    p1: str = "human"
    p2: str = "human" if two_players else "computer"
 
    while not over:
        print()

        # player 1 
        val1: str = func_map[p1](moves_set)

        # player 2 
        val2: str = func_map[p2](values)

        if moves[val1] == val2:
            scores[0] += 1
        elif moves[val2] == val1:
            scores[1] += 1

        # display scores 
        display(scores, val1, val2)

        # check if game over 
        if max(scores) == limit:
            over = True 

    print()
    if scores[0] > scores[1]:
        print("Winner is player 1")
    else:
        print("Winner is player 2")


if __name__ == '__main__':
    import re 
    pattern: str = (r'[0-9]+')
    val: str = input("Set score limit (for example 10): ")
    
    while not re.match(pattern, val):
        print("Please enter a number")
        val = input("Set score limit (for example 10): ")

    limit: int = int(val)

    if int(input("How many players? (1 or 2): ")) == 2:
        game(limit, two_players = True)
    else:
        game(limit)
    