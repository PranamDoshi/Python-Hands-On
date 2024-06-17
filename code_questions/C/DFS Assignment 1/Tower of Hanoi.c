#include<stdio.h>
void transferinorder(char P, char R, char Q, int A);
int main()
{
    int a;
    printf("Enter the number of plates to transfer from p to r.\n");
    scanf("%d", &a);
    transferinorder('A','C','B', a);
    return 0;
}
void transferinorder(char P, char R, char Q, int A)
{
    if(A==1)
    {
        printf("Move %d from %c to %c.\n", A, P, R);
    }
    else
    {
        transferinorder(P, Q, R, A-1);
        printf("Move %d from %c to %c.\n", A-1, P, R);
        transferinorder(Q, R, P, A-1);
    }
}
/*
Enter the number of plates to transfer from p to r.
3
Move 1 from A to B.
Move 1 from A to C.
Move 1 from C to B.
Move 2 from A to B.
Move 1 from B to A.
Move 1 from B to C.
Move 1 from C to A.
*/

