import random
import time
import math


Amounts = [0.5, 1, 5, 10, 25, 50, 75, 100, 150, 250, 500, 750, 1000, 1250, 1500, 1700, 2000, 2300, 2500, 2700, 3000, 3500, 4000, 4500, 5000]
Original_Amounts = [0.5, 1, 5, 10, 25, 50, 75, 100, 150, 250, 500, 750, 1000, 1250, 1500, 1700, 2000, 2300, 2500, 2700, 3000, 3500, 4000, 4500, 5000]
game_amounts = []
selected_numbers = []
Numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, ]
round = 0
offers = []
initial_pick = 0

# Shuffle the Amounts
def reset_game(prices):
    random.shuffle(prices)
    game_amounts = prices


def next_draw(reps):
    global round
    x = 0
    while x < reps:
        new_draw = int(input(f'{Numbers[:5]}\n{Numbers[5:10]}\n{Numbers[10:15]}\n{Numbers[15:20]}\n{Numbers[20:25]}\nWhich number will you want to reveal next?\n'))
        if new_draw not in selected_numbers:
            selected_numbers.append(new_draw)
            print(f'You have chosen to reveal {new_draw}\nAnd the amount is')
            time.sleep(2)
            print('...')
            time.sleep(2)
            # print('...')
            # time.sleep(2)
            # print('...')
            # time.sleep(2)
            # print('...')
            # time.sleep(2)
            print(f'{Amounts[new_draw - 1]}')
            Numbers[new_draw - 1] = 'X'

            # Original_Amounts = [x.replace(Amounts[new_draw - 1], f'--{Amounts[new_draw - 1]}--') for x in Original_Amounts]
            # print(Original_Amounts)
            
            game_amounts.remove(Amounts[new_draw - 1])
            x += 1
        
        else:
            print(f'{new_draw} has already been selected. Pick another number')
    round += 1


def present_offer(x):
    ev = sum(game_amounts)/(len(game_amounts))
    offers.append(int(ev * (random.choice(x))))

    print('Alright Alright You are on your way there.\nHowever, we have an offer for you to consider.\nThe offer is\n\n')
    time.sleep(2)
    # print('...')
    # time.sleep(2)
    # print('...')
    # time.sleep(2)
    print(f'rounds = {round}')
    print(f'game amounts{game_amounts}')
    print(f'selected number = {selected_numbers}')
    print(f'offers = {offers}')
    print(f'{offers[round - 1]}\n')

    response = input(f'Would you want to take the offer of {offers[round - 1]}? y/n?\n')
    if response.lower() == 'y':
        return False
    return True



################## START GAME ##################
reset_game(Amounts)
# print(Amounts)
game_amounts = [x for x in Amounts]



# ROUND 0
# First draw that selects an unknown amount to keep as the possible jackpot. 
# This number remains unopened till the end of the game

first_draw = int(input(f'{Numbers[:5]}\n{Numbers[5:10]}\n{Numbers[10:15]}\n{Numbers[15:20]}\n{Numbers[20:25]}\nSelect a number 1 - 25 which you believe holds the 5,000.00:\n'))
selected_numbers.append(first_draw) # this keeps records of the numbers that have been selected
print(f'You selected {first_draw}. Now you have to reveal 6 enteries.')
Numbers[first_draw - 1] = 'X' # this is for display purposes so that when a number is chosen it's place is marked by X
initial_pick = Amounts[first_draw-1]
game_amounts.remove(Amounts[first_draw - 1])


# ROUND 1
# reveal 6 numbers

next_draw(5)

# ROUND 2 - Present an offer and open 5 numbers if not accepted
if present_offer(x = [0.3, 0.34, 0.38, 0.4, 0.45, 0.5, 0.55, 0.6]):
    next_draw(5)
    
    # ROUND 3 - Present an offer and open 54 numbers if not accepted
    if present_offer(x = [0.45, 0.5, 0.54, 0.6, 0.65, 0.7]):
        next_draw(4)

        # ROUND 4 - Present an offer and open 3 numbers if not accepted
        if present_offer(x = [0.55, 0.6, 0.64, 0.68, 0.7, 0.75, 0.8]):
            next_draw(3)

            # ROUND 5 - Present an offer and open 2 numbers if not accepted
            if present_offer(x = [0.6, 0.64, 0.68, 0.7, 0.75, 0.8]):
                next_draw(2)

                # ROUND 6 - Present an offer and open 2 numbers if not accepted
                if present_offer(x = [0.65, 0.68, 0.7, 0.75, 0.8]):
                    next_draw(2)

                    # ROUND 7 - Present an offer and open 1 number if not accepted
                    if present_offer(x = [0.7, 0.75, 0.8]):
                        next_draw(1)
                        

                        # ROUND 8 - Present an offer and open 1 number if not accepted
                        if present_offer(x = [0.7, 0.75, 0.8]):
                            next_draw(1)

                            # ROUND 9 - Present an offer and open 1 number if not accepted
                            print(f'If you forfeit this offer then you are choosing to keep your initial selection.\nThis is your last chance to change your mind')
                            if present_offer(x = [0.45, 0.5, 0.54, 0.6, 0.65, 0.7]):
                                remaining_num = [x for x in Numbers if x not in selected_numbers]
                                print(f'We will now go on to reveal {remaining_num[0]}')
                                print(f'The last Amount under {remaining_num[0]} is...')
                                time.sleep(2)
                                print(f'\n{Amounts[remaining_num]}\n and your initial choice {first_draw} has...')
                                time.sleep(2)
                                print(f'...\n{Amounts[first_draw - 1]}\n')

                                # next_draw(1)


else:
    print(f'Congratulations! You have chosen to forfeit your {first_draw}\nYou have earned {offers[round - 1]}')



