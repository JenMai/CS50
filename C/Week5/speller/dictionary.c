/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

#include "dictionary.h"

/*
 * Nodes for trie
 */

typedef struct node
{
    bool is_word;
    struct node* alpha_child[27];
}
node;
node *alpha_root; //keep track of the trie's root.

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // TODO
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 * load function assumes dictionary is only made of lower cases and apostrophes, and each word is separated by a new line.
 */
bool load(const char *dictionary)
{
    FILE *fptr;
    
    fptr = fopen(dictionary, "r");                                //open and read dictionary
    
    if (fptr == NULL)
    {
        return false;
    }
    
    alpha_root = malloc(sizeof(node));                            //assign memory to root
    node *trav = alpha_root;                                      //pointer travelling through arrays of pointers
    int c = fgetc(fptr);                                          // keep track of the char pointed (its ASCII value)
    int i = c - 'a';                                              // hashcode for each letter + apostrophe
    
    for (; c != EOF; c = fgetc(fptr))                             // iterate through each char in dictionary until EOF
    {
        if (isalpha(c))
        {
            i = c - 'a';
            if (trav->alpha_child[i] == NULL)                     //if trav points to NULL (no pointer previously generated)
            {
                trav->alpha_child[i] = malloc(sizeof(node));      // allocate memory to node
                trav = trav -> alpha_child[i];                    // go to that node for next loop
            }
            else                                                  // if trav points to an existing node (letter encountered in that branche)
            {
                trav = trav -> alpha_child[i];
            }
        }
        
        else if (c == '\'')                                       // same with apostrophe
        {
            i = 27;
            if (trav->alpha_child[i] == NULL)
            {
                trav->alpha_child[i] = malloc(sizeof(node));
                trav = trav -> alpha_child[i];
            }
            else
            {
                trav = trav -> alpha_child[i];
            } 
        }
        
        else                                                     // new line reached, end of the word
        {
            trav -> is_word = true;
            trav = alpha_root;
        }
    }
    
        if (ferror(fptr))                                       // ensure no problem occured before any return value.
        {
            fclose(fptr);
            return false;
        }
        
        else
        {
            fclose(fptr);
            return true;
        }
}


/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // TODO
    return 0;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // TODO
    return false;
}
