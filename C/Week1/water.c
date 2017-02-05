/**
 * Tell the number of bottles used according to time spent in shower.
 */

#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int minutes;
    do
    {
        printf("Minutes: ");
        minutes = get_int();
    }
    while(minutes < 0);
    
    printf( "Bottles: %i\n", minutes*(196/16) );
    
}