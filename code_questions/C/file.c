#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int wordsearch(FILE* fptr, char word[])
{
    char ch, str[20];
    int i, n = 0, count = 0, j=0;
    while(1)
    {
        ch = fgetc(fptr);
        printf("%c\t", ch);
        if(ch == EOF)
            break;
        else if(ch == ' ' || ch == ',' || ch == '.' || ch == '\'' || ch == '\n' || ch == '-' || ch == '\(')
        {
            if(strlen(word) == n)
            {
                for(i = 0;i < strlen(word); i++)
                {
                    if(str[i] == word[i])
                        continue;
                    else
                        break;
                }
                if(i == strlen(word) || i+1 == strlen(word))
                    count++;
            }
            n = 0;
        }
        else
        {
            j++;
            if(j>3)
            {
                str[n] = ch;
                n++;
            }
        }
    }
    return count;
}

int main()
{
	FILE* fptr;
	char word[20], count;
	fptr = fopen("C:/Users/pranav1/Desktop/trial.txt", "r");
	if(fptr == NULL)
	{
		printf("Unable to open file.\n");
		exit(-1);
	}
	printf("\t\tFile opened successfully....\n");
	printf("Enter the word to search in the file.\n");
	scanf("%s", word);
	count = wordsearch(fptr, word);
	printf("\n");
	printf("The word '%s' is found '%d' times in the given file.\n", word, count);
	fclose(fptr);
	return 0;
}
