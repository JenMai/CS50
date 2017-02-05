/**
 * Build stairs such as the first level of Super Mario.
 * Few edits needed (less messy loop conditions, comments)
 */

#include<stdio.h>
#include<cs50.h>

int main(void)
{
    int height;
    do
    {
        printf( "Height: " );
        height = get_int();
    }
    while(height < 0 || height > 23);
    
    for (int row = 0 ; row < height; ++row)
        {
            for (int space = row + 1 ; space < height; ++space)
            {
                printf( " " );
            }
            for (int hash = row + 1 ; hash > -1; --hash)
            {
                printf( "#" );
            }

            printf( "\n" );
        }
    
}
