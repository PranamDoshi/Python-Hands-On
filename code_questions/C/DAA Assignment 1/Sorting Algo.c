#include<stdio.h>
#include<inttypes.h>
#include<time.h>
#define N 1000
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
    double a = 0;
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
    //printf("\n");
    //printf("Sorted list in ascending order:\n");
/*    for (c = 0; c < N; c++)
        printf("%d\t", A[c]);*/
    //printf("\n");
    printf("Number of exchanges are %f.\n", a);
}
void insertionsort(int B[N])
{
    int n, m, d, t;
    double p = 0;
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
//    printf("\n");
/*    printf("Sorted list in ascending order:\n");
    for (m = 0; m <= N - 1; m++)
    {
        printf("%d\t", B[m]);
    }
    printf("\n");*/
    printf("Number of exchanges are %f.\n", p);
}
int main()
{
    int A[N], B[N], C[N], i, n = 0;
    clock_t start, end;
    double bubb;
    double inst;
    double total_buba[100], total_bubw[100], total_bubb[100];
    double total_insa[100], total_insw[100], total_insb[100];
    for(i=0;i<N;i++)
    {
        A[i] = rand();
    }
    for(i=0;i<N;i++)
    {
        C[i] = A[i];
    }
    /*for(i=0;i<N;i++)
    {
        printf("%d\t", A[i]);
    }*/
    while(n<100)
    {
    //    printf("\n");
        for(i=0;i<N;i++)
        {
            A[i] = C[i];
        }
        start = clock();
        bubblesort(A);
        end = clock();
        total_buba[n] = ((double) (end - start)) / CLOCKS_PER_SEC;
        start = clock();
        bubblesort(A);
        end = clock();
        total_bubb[n] = ((double) (end - start)) / CLOCKS_PER_SEC;
        for(i=0;i<N;i++)
        {
            B[i] = A[N-i-1];
        }
        start = clock();
        bubblesort(B);
        end = clock();
        total_bubw[n] = ((double) (end - start)) / CLOCKS_PER_SEC;
      //  printf("\n");
        for(i=0;i<N;i++)
        {
            A[i] = C[i];
        }
        start = clock();
        insertionsort(A);
        end = clock();
        total_insa[n] = ((double) (end - start)) / CLOCKS_PER_SEC;
        //printf("\n");
        start = clock();
        insertionsort(A);
        end = clock();
        total_insb[n] = ((double) (end - start)) / CLOCKS_PER_SEC;
        for(i=0;i<N;i++)
        {
            B[i] = C[N-i-1];
        }
        start = clock();
        insertionsort(B);
        end = clock();
        total_insw[n] = ((double) (end - start)) / CLOCKS_PER_SEC;
        n++;
    }
    printf("\n");
    printf("BEST CASE :-\n");
    bubb = avg(total_bubb);
    inst = avg(total_insb);
    printf("Time taken by Bubble sort is %f.\n", bubb);
    printf("Time taken by Insertion sort is %f.\n", inst);
    printf("\n");
    printf("AVG CASE :-\n");
    bubb = avg(total_buba);
    inst = avg(total_insa);
    printf("Time taken by Bubble sort is %f.\n", bubb);
    printf("Time taken by Insertion sort is %f.\n", inst);
    printf("\n");
    printf("WORST CASE :-\n");
    bubb = avg(total_bubw);
    inst = avg(total_insw);
    printf("Time taken by Bubble sort is %f.\n", bubb);
    printf("Time taken by Insertion sort is %f.\n", inst);
}
