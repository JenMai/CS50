    /*
     * Prints the half pyramid at the end of the first level in Super Mario.
     */

#include<stdio.h>
#include<cs50.h>

int main(void)
{
    /*
     * Asks user for height of pyramid.
     */
    int height;
    do
    {
        printf( "Height: " );
        height = get_int();
    }
    while(height < 0 || height > 23);
    
    /*
     * Prints the pyramid according to user's input.
     */
    
    for (int row = 0 ; row < height; ++row)                 //for each row
        {
            for (int space = row ; space < height; ++space) // print 'decreasingly' blank tiles first
            {
                printf( " " );
            }
            for (int hash = row ; hash >= 0; --hash)        // print 'increasingly' hash tiles
            {
                printf( "#" );
            }

            printf( "#\n" );                                //pyramid has one extra column of tiles
        }
    
}
