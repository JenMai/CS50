    /*
     * Prints initials
     */

#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

int main( void )
{
    int i;
    string name = get_string();

    printf( "%c", toupper( name[0] ) );                 // prints first character of string and turn to upper case

    /*
     * Prints each character after a space (assuming only one space between words)
     */
    for(i = 0 ; name[i] != '\0'; i++)
    {
        if( name[i] == ' ' )
        {
            printf( "%c", toupper( name[i+1] ) );
        }

    }
    printf( "\n" );
}
