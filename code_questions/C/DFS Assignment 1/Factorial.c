#include<stdio.h>
int factorial(int i);
int main()
{
    int f, F;
    printf("Enter the number to find its factorials..\n");
    scanf("%d", &f);
    F = factorial(f);
    printf("The factorial of given number is %d.\n", F);
    return 0;
}
int factorial(int i)
{
    int tf, r;
    if(i==1)
    {
        r = 1;
    }
    else
    {
        tf = factorial(i-1);
        r = (i*tf);
    }
    return r;
}
/*
OUTPUT:-
Enter the number to find its factorial..
5
The factorail of given number is 120.
*/
