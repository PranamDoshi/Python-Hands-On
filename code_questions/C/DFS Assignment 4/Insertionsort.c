#include<stdio.h>
#include<stdlib.h>
#include<time.h>
void insertionsort(int A[]);
#define N 1000000
void insertionsort(int A[])
{
	int i, j, key, k;
	for(i=1;i<N;i++)
	{
		key = A[i];
		for(j = i-1;j>=0;j--)
		{
			if(A[j]>key)
            {
                A[j+1] = A[j];
                A[j] = key;
            }
            else
                break;
        }
	}
    printf("\n");
	for(i=0;i<N;i++)
    {
        printf("%d\n", A[i]);
    }
}
void main()
{
	int A[N], i;
    clock_t start, end;
    double total_time;
	for(i=0;i<N;i++)
	{
		A[i] = N-i;
	}
	for(i=0;i<N;i++)
    {
        printf("%d\n", A[i]);
    }
    start= clock();
	insertionsort(A);
    end = clock();
    for(i=0;i<N;i++)
    {
        printf("%d\n", A[i]);
    }
    total_time = ((double)(end-start)/CLOCKS_PER_SEC);
    printf("Total processing time is %4f seconds.\n", total_time);
}

