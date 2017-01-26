/**
 * rename helpers.c /!\
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
 
#include "helpers.h"
 
/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
 
    int mid_pt = n/2, start_pt = 0 ;           //only evaluates values after that point. (and yeah, mid_pt is redundant in that function)
    while( start_pt <= n )                      //else, value isn't in array
    {
        if( values[mid_pt] == value )
        {
            return true;
        }
        else if( values[mid_pt] < value )
        {
            start_pt = mid_pt + 1;              //mid_pt has been evaluated already, +1
            mid_pt = ( start_pt + n ) / 2;
        }
        else if( values[mid_pt] > value )
        {
            n = mid_pt - 1;                     //mid_pt has been evaluated already, -1
            mid_pt = ( start_pt + n ) / 2;
        }
    }
   
    return false;
}
/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    for( int i = 0 ; i < n ; i++ )
    {
        int min_index;                           // assumes the smallest value is at first index
        min_index = i;
       
        for(int j = i+1 ; j < n ; j++ )          //evaluates the smallest unsorted value in the array
        {
            if( values[j] < values[min_index])   //if i+1+1 is smaller than i+1 etc...
            {
               min_index = j;                    //keeps index of the smallest value in mind
            }
        }
       
        int sw = values[min_index];              //swapping the two values (at i and at the index of the smallest value)
        values[min_index] = values[i];
        values[i] = sw;
    }
    return;
}