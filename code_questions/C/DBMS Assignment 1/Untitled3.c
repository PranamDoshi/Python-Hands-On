#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define Buffer 1500
int countOccurrences(FILE *fptr, const char *word);
int main()
{
    FILE *fpointer;
    char word[50];
    int count;
    printf("Enter word to search in file:\n");
    scanf("%s", word);
    fpointer = fopen("News_Final.csv", "r");
    if (fpointer == NULL)
    {
        printf("Unable to open file.\n");
    }
    count = wordcounter(fpointer, word);
    printf("The word %s is found %d times in News_Final file.\n", word, count);
    fclose(fpointer);
    return 0;
}
int wordcounter(FILE *fpointer, const char *word)
{
    char fb[Buffer];
    char *pos;
    int index, count;
    count = 0;
    while ((fgets(fb, Buffer, fpointer)) != NULL)
    {
        index = 0;
        while ((pos = strstr(fb + index, word)) != NULL)
        {
            index = (pos - fb) + 1;
            count++;
        }
    }
    return count;
}
