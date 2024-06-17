#include<stdio.h>
#include<time.h>
float factorial(float N)
{
    float temp;
    if(N == 0 || N == 1)
        return 1;
    temp = N * factorial(N-1);
    return temp;
}
int Fibonacci(int i)
{
    if(i == 0)
        return 0;
    else if(i == 1)
        return 1;
    else
        return (Fibonacci(i-1) + Fibonacci(i-2));
}
int main()
{
    float n, n1 = 1, n2, m;
    int i, p, t1 = 0, t2 = 1, nt, k;
    clock_t start, end;
    double total_itet, total_rect;
    double total_itet1, total_rect1;
    printf("\t\tFibonacci Series :-\n");
    printf("Enter the number of terms...\n");
    scanf("%d", &p);
    printf("Iterative Way:-\n");
    start = clock();
    for(i = 1; i <= p;i++)
    {
        printf("%d\t", t1);
        nt = t1 + t2;
        t1 = t2;
        t2 = nt;
    }
    printf("\n");
    end = clock();
    total_itet = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken is %4f.\n", total_itet);
    printf("\n");
    printf("Recursive Way....\n");
    i = 0;
    start = clock();
    for(k = 1;k <= p;k++)
    {
        printf("%d\t", Fibonacci(i));
        i++;
    }
    printf("\n");
    end = clock();
    total_rect = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken is %4f.\n", total_rect);
    printf("\t\tFactorials :-\n");
    printf("Enter the number to find factorial of it....\n");
    scanf("%f", &n);
    printf("Iterative Way :-\n");
    start = clock();
    for(m = 1;m <= n;m++)
    {
        n1 = n1*m;
    }
    end = clock();
    total_itet1 = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Answer is %f.\n", n1);
    printf("Time taken is %4f.\n", total_itet);
    printf("Recursive Way :-\n");
    printf("Enter the number to find factorial of it....\n");
    scanf("%f", &n);
    start = clock();
    n2 = factorial(n);
    end = clock();
    total_rect1 = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Answer is %f.\n", n2);
    printf("Time taken is %f.\n", total_rect);
}
