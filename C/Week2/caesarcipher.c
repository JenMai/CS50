#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main( int argc, string argv[] )
{
    //// user must enter only one argument (key) after launch command ////
    if( argc > 2 )
    {
        return 1;
    }
    if ( argc == 1 )
    {
        printf( "Usage: ./caesar k\n" );
        return 1;
    }

    int k = atoi( argv[1] );                                    // convert string to integer (0 if not numeric)
    
    printf( "plaintext: " );
    string p = get_string();
    
    printf( "ciphertext: " );
    
    //// cipher and print one character at a time in p ////
    for( int i = 0, n = strlen(p); i < n ; i++ )
    {
        if( isalpha( p[i] ) )                                   // cipher only if alphabetical
        {
            if( isupper( p[i] ) )
            {
                p[i] = ( ( p[i] - 65 ) + k ) % 26;              //converts ASCII value (A=65) to alphabetical (A=0) to fit modulo
                printf( "%c", p[i] + 65 );                      // converts back to ascii value
            }

            if( islower( p[i]) )
            {
                p[i] = ( ( p[i]- 97 ) + k) % 26;                // lower cases are (ASCII value of uppercase) + 32
                printf( "%c", p[i] + 97 );
            }
            
        }
        else
        {
            printf( "%c", p[i] );
        }
    }
    
    printf( "\n" );
    
}