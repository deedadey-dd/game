import random
import time
import math


Amounts = [0.5, 1, 5, 10, 25, 50, 75, 100, 150, 250, 500, 750, 1000, 1250, 1500, 1700, 2000, 2300, 2500, 2700, 3000, 3500, 4000, 4500, 5000]
Numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, ]
Game_Dict = {}

def reset_game(prices):
    random.shuffle(prices)


reset_game(Amounts)
print(Amounts)

game_amounts = Amounts

first_draw = int(input(f'Select a number 1 - 25 which you believe holds the 5,000.00:\n{Numbers[:5]}\n{Numbers[5:10]}\n{Numbers[10:15]}\n{Numbers[15:20]}\n{Numbers[20:25]}'))

print(f'You selected {first_draw}. Now you have to reveal 6 enteries.')
Numbers[first_draw - 1] = 'X'

def next_draw(reps):

    for x in range(reps):
        new_draw = int(input(f'Which number will you want to reveal next?\n{Numbers}\n'))

        print(f'You have chosen to reveal {new_draw}\n And the amount is ...')
        time.sleep(2)
        print('...')
        time.sleep(2)
        print('...')
        time.sleep(2)
        # print('...')
        # time.sleep(2)
        # print('...')
        # time.sleep(2)
        print(f'{Amounts[new_draw - 1]}')
        Numbers[new_draw - 1] = 'X'

        game_amounts.remove(Amounts[new_draw - 1])


next_draw(6)

def present_offer(x):
    ev = math.sum(game_amounts)/(len(game_amounts))
    offer = ev * x

print('Alright Alright You are on your way there.\n However, we have an offer for you to consider')

print('This is hte last line')

