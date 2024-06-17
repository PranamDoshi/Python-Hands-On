#include<stdio.h>
#include<time.h>
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
    int i, n, t1 = 0, t2 = 1, nt, k;
    clock_t start, end;
    double total_itet, total_rect;
    printf("Enter the number of terms...\n");
    scanf("%d", &n);
    printf("Iterative Way:-\n");
    start = clock();
    for(i = 1; i <= n;i++)
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
    for(k = 1;k <= n;k++)
    {
        printf("%d\t", Fibonacci(i));
        i++;
    }
    printf("\n");
    end = clock();
    total_rect = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken is %4f.\n", total_rect);
}
