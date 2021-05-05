#! env/python3
import random


class Hand:
    def __init__(self):
        self._value = 1
        self._state = 'in_game'
        
    def attackHand(self, t_hand):
        assert self._state == 'in_game' and t_hand._state == 'in_game', 'unavalable_hand'
        self._value = (self._value + t_hand._value) % 10
        if self._value == 0:
            self._state = 'finished'
            
        
class Player:
    def __init__(self):
        self._score = 0
        self._hands = {}
        self._hands['l'] = Hand()
        self._hands['r'] = Hand()
        
    @property
    def _avalable_hands(self):
        return dict(filter(lambda kv: kv[1]._state == 'in_game', self._hands.items()))
    def attack(self, opponent, source: str, target: str):
        assert source in self._hands.keys() and target in self._hands.keys(), 'unavalable_choice'
        s_hand = self._hands[source.lower()]
        t_hand = opponent._hands[target.lower()]
        try:
            s_hand.attackHand(t_hand)
            if s_hand._state == 'finished':
                self._score += 1
                s_hand._state = 'waiting'
        except AssertionError as ae:
            raise ae
        
    
def input_move(pl: Player, op: Player):
    s, t = input().split(' ')
    pl.attack(op, s, t)
    
    
def random_move(pl: Player, op: Player):
    s = random.choice(list(pl._avalable_hands.keys()))
    t = random.choice(list(op._avalable_hands.keys()))
    print(s, t, '---Opponent')
    pl.attack(op, s, t)
    
def display_table(pl, op):
    print('******Opponent******')
    print('   L            R   ')
    print('   {}            {}   '.format(op._hands['l']._value, op._hands['r']._value))
    print('')
    print('   {}            {}   '.format(pl._hands['l']._value, pl._hands['r']._value))
    print('   L            R   ')
    print('*********You********')
    
def main():
    pl = Player()
    op = Player()
    while True:
        display_table(pl, op)
        try:
            input_move(pl, op)
            if pl._score >= 2:
                print('player win!')
                break
        except AssertionError as ae:
            print('invalid move!')
            continue
        display_table(pl, op)
        random_move(op, pl)
        if op._score >= 2:
            print('cpu win!')
            break
    return


if __name__ == '__main__':
    main()