#include<stdio.h>
#include<inttypes.h>
#include<time.h>
#define N 10000
double avg(double sort[100])
{
    double sum = 0;
    int i;
    for(i=0;i<100;i++)
    {
        sum = sum + sort[i];
    }
    return (sum/100);
}
void bubblesort(int A[N])
{
    int c, d, swap;
    intmax_t a = 0;
    for (c = 0 ; c < N - 1; c++)
    {
        for (d = 0 ; d < N - c - 1; d++)
        {
            if (A[d] > A[d+1])
            {
                swap   = A[d];
                A[d]   = A[d+1];
                A[d+1] = swap;
                a++;
            }
        }
    }
    printf("\n");
    printf("Sorted list in ascending order:\n");
    for (c = 0; c < N; c++)
        printf("%d\t", A[c]);
    printf("\n");
    printf("Number of exchanges are %ju.\n", a);
}
void insertionsort(int B[N])
{
    int n, m, d, t;
    intmax_t p = 0;
    for (m = 1 ; m <= N - 1; m++)
    {
        d = m;
        while ( d > 0 && B[d-1] > B[d])
        {
            p++;
            t      = B[d];
            B[d]   = B[d-1];
            B[d-1] = t;
            d--;
        }
    }
    printf("\n");
    printf("Sorted list in ascending order:\n");
    for (m = 0; m <= N - 1; m++)
    {
        printf("%d\t", B[m]);
    }
    printf("\n");
    printf("Number of exchanges are %ju.\n", p);
}
int main()
{
    int A[N], B[N], i, n = 0;
    clock_t start, end;
    double total_bubb[100], bubb;
    double total_inst[100], inst;
    for(i=0;i<N;i++)
    {
        A[i] = N - i;
    }
    for(i=0;i<N;i++)
    {
        B[i] = A[i];
    }
    for(i=0;i<N;i++)
    {
        printf("%d\t", A[i]);
    }
    while(n<100)
    {
        printf("\n");
        start = clock();
        bubblesort(A);
        end = clock();
        total_bubb[n] = ((double) (end - start)) / CLOCKS_PER_SEC;
        printf("\n");
        start = clock();
        insertionsort(B);
        end = clock();
        total_inst[n] = ((double) (end - start)) / CLOCKS_PER_SEC;
        printf("\n");
        n++;
    }
    bubb = avg(total_bubb);
    inst = avg(total_inst);
    printf("Time taken by bubble sort is %f.\n", bubb);
    printf("Time taken by insertion sort is %f.\n", inst);
}
