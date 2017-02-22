#---------------------------------
# Prints the half pyramid at the end of 
# the first level in Super Mario.
#----------------------------------

import cs50

def main():
    #----------------------------------
    # Asks user for height of pyramid.
    #----------------------------------
    while True:
        print("Height: ", end="")
        height = cs50.get_int()
        if height > 0 and height < 23:
            break
    
    #----------------------------------    
    # Prints the pyramid according to user's input.
    #----------------------------------
    for row in range(height):
        for space in range(height-row):        # print 'decreasingly' blank tiles first
            print(" ", end="")
        for block in range(row+1):             # print hash tiles
            print("#", end="")
        print("#")
        

if __name__ == "__main__":
    main()


            