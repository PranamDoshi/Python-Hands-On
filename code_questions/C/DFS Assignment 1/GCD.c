#include<stdio.h>
#include<math.h>
int findgcd(int p, int q);
int main()
{
    int m, n, G;
    printf("Enter two numbers to find GCD of it..(m>n)\n");
    scanf("%d%d", &m, &n);
    G = findgcd(m, n);
    printf("The GCD of given numbers is %d.\n", G);
    return 0;
}
int findgcd(int p, int q)
{
    int i=0, g;
    if(p%q==0)
    {
        return q;
    }
    else
    {
        g = (p-q);
        return(findgcd(max(g,q),min(g,q)));
    }
}
int max(int p,int q)
{
    if(p>q)
    {
        return p;
    }
    else
    {
        return q;
    }
}
int min(int p, int q)
{
    if(p<q)
    {
        return p;
    }
    else
    {
        return q;
    }
}
/*
OUTPUT:-
Enter two numbers to find GCD of it..(m>n)
18
12
The GCD of given numbers is 6.
*/
