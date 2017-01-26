#include<stdio.h>
#include<cs50.h>
 
#define QUARTER 25
#define DIME 10
#define NICKEL 5
#define PENNY 1
 
int total = 0;
 
int get_coins( int x, int Y );
 
int main(void)
{
    float dollars;
                                           
    /*
     * Gets a non-negative float input from user (turns into float if integer)
     */
    printf("O hai! ");
    do
    {
        printf("How much is owed?\n");
        dollars = get_float();
    }
    while( dollars < 0 );
   
    /*
     * Gets the minimum number of coins needed
     */
    while (dollars >= 1)
    {
        total += 4;                                // 4 quarters in a dollar, removes one dollar from input
        dollars -= 1;
    }
   
    int cents = dollars * 100.01;                   //convert dollars into cents; rounds; gets an integer
 
    cents = get_coins( cents, QUARTER );
    cents = get_coins( cents, DIME );
    cents = get_coins( cents, NICKEL );
    cents = get_coins( cents, PENNY );
   
    printf("%i\n", total);                          //the total number of coins needed
 
}
 
/*
 * Gets the highest number of coin possible for quarters, then dimes...
 */
int get_coins( int x, int Y )  
{
    while( x/Y > 0 )
    {
        total += x/Y;
        x %= Y;
    }
    return x;
}