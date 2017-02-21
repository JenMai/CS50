/*
 * Ciphers a text according to a key
 */

#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main( int argc, string argv[] )
{
    /*
     * Checks if user only entered one argument (key) after launch command
     */
    
    if( argc > 2 )
    {
        printf( "Usage: ./vigenere k\n" );
        return 1;
    }
    if ( argc == 1 )
    {
        printf( "Usage: ./vigenere k\n" );
        return 1;
    }

    string k = argv[1];
    int m = strlen(k);
    
    /*
     * Checks if user entered only alphabetical chars after launch command.
     */
    for( int j = 0; j < m; )
    {
        if( isalpha( k[j] ) )
        {
            j++;
        }
        else
        {
            printf( "Usage: ./vigenere k\n" );
            return 1;
        }
    }
    
    printf( "plaintext: " );
    string p = get_string();
    
    printf( "ciphertext: " );
    
    /*
     * Ciphers and print one character at a time in p.
     */
    for( int i = 0, j = 0, n = strlen(p); i < n ; i++)
    {
        if( islower( k[j] ) )
        {
            k[j] = toupper( k[j] );                             // match char's cases in key to facilitate ciphering
        }

        if( isalpha( p[i] ) )                                   // cipher/ key char's change only if p (plain) is alphabetical.
        {
            
            if( isupper( p[i] ) )
            {
                p[i] = (( p[i] - 65) + (k[j] - 65)) % 26;       //converts ASCII value (A=65) to alphabetical (A=0) to fit modulo
                printf( "%c", p[i] + 65 );                      // converts back to ascii value
                j++;
            }

            if( islower( p[i]) )
            {
                p[i] = ((p[i]- 97) + (k[j] - 65)) % 26;         // lower cases are (ASCII value of uppercase) + 32
                printf( "%c", p[i] + 97 );
                j++;
            }
            
            if( j % m == 0 )                                    // start back to the first char of the key
            {
                j = 0;
            }
            
        }
        else
        {
            printf( "%c", p[i] );
        }
    }
    
    printf( "\n" );
    
}
