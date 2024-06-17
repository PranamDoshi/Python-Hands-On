#include<stdio.h>
char s[20];
int top = -1;
void push(char a)
{
        s[++top] = a;
}
char pop()
{
    if(top == -1)
    {
        return -1;
    }
    else
     {
        return s[top--];
     }
}
int priority(char a)
{
    if(a == '(')
        return 0;
    if(a == '+' || a == '-')
        return 1;
    if(a == '*' || a == '/')
        return 2;
}
int main()
{
    char infix[20];
    char *imf, a;
    printf("Enter the expression :\n");
    scanf("%s",infix);
    imf = infix;
    while(*imf != '\0')
    {
        if(isalnum(*imf))
            printf("%c",*imf);
        else if(*imf == '(')
            push(*imf);
        else if(*imf == ')')
        {
            while((a = pop()) != '(')
                printf("%c", a);
        }
        else
        {
            while(priority(s[top]) >= priority(*imf))
            printf("%c",pop());
            push(*imf);
        }
        imf++;
    }
    while(top != -1)
    {
        printf("%c",pop());
    }
}
/*Enter the expression :
a+b*c^(d-e*f)+g/h
abcdef*-^*+gh/+
*/
