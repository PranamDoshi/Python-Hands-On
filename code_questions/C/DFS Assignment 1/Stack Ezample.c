#include<stdio.h>
#include<stdlib.h>
#define N 20
void Push(char s[], int *top, char p);
void Change(char s[], int top, char c, int q);
char Read(char s[], int top, int q);
char Pop(char s[], int *top);
int main()
{
    char s[N];
    int X,P, top = -1;
    char V, b;
    for(P='A';P<='T';P++)
    {
        Push(s, &top, P);
    }
    Change(s, top, 'r', 3);
    V = Read(s, top, 3);
    printf("The 3rd element from top is %c.\n", V);
    for(X=0;X<=N;X++)
    {
        b = Pop(s, &top);
        printf("%c\n", b);
    }
    return 0;
}
void Push(char s[], int *top, char p)
{
    if((*top)<N-1)
    {
        (*top)++;
        s[*top] = p;
    }
    else
    {
        printf("Stack Overflow..\n");
        exit(-1);
    }
}
void Change(char s[], int top, char c, int q)
{
    if(top-q+1>=0)
    {
        s[top-q+1] = c;
    }
    else
    {
        printf("Not found any such element!!\n");
        exit(-1);
    }
}
char Read(char s[], int top, int q)
{
    char z;
    if(top-q+1>=0)
    {
        z = s[top-q+1];
        return z;
    }
    else
    {
        printf("Not found such element to read!!\n");
        exit(-1);
    }
}
char Pop(char s[], int *top)
{
    char ch;
    if((*top)>=0)
    {
        ch = s[*top];
        (*top)--;
    }
    else
    {
        printf("Stack is empty..\n");
        exit(-1);
    }
    return ch;
}
/*
OUTPUT:-
The 3rd element from top is r.
T
S
r
Q
P
O
N
M
L
K
J
I
H
G
F
E
D
C
B
A
Stack is empty..*/
