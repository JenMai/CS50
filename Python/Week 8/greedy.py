#---------------------------------
# Gives the fewest coins possibles for a given amount
#----------------------------------

import cs50

QUARTER = 25
DIME = 10
NICKEL = 5
PENNY = 1

def main():
    
    #---------------------------------
    # Gets a non-negative float input from user.
    #----------------------------------
    
    print("O hai! ", end="")
    
    while True:
        print("How much is owed?")
        dollars = cs50.get_float()
        if dollars > 0:
            break
    
    #---------------------------------
    # Gets the coins from largest to tiniest value.
    #----------------------------------
    
    total = 0
    
    dollars = round(dollars, 2) * 100
    dollars = int(dollars)

    total += dollars // QUARTER
    dollars %= QUARTER
    
    total += dollars // DIME
    dollars %= DIME
    
    total += dollars // NICKEL
    dollars %= NICKEL
    
    total += dollars // PENNY
    dollars %= PENNY
    
    print("{}".format(total))
    
if __name__ == "__main__":
    main()
