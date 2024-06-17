#include<stdio.h>
#include<stdlib.h>
#include<time.h>
void insertionsort(int a[]);
#define N 1000000
void insertionsort(int a[])
{
	int i, j, key, k;
	for(i=1;i<N;i++)
	{
		key = a[i];
		for(j = i-1;j>=0;j--)
		{
			if(a[j]>key)
            {
                a[j+1] = a[j];
                a[j] = key;
            }
            else
                break;
        }
	}
    printf("\n");
	for(i=0;i<N;i++)
    {
        printf("%d\n", a[i]);
    }
}
void main()
{
	int a[N], i;
    clock_t start, end;
    double total_time;
    start= clock();
	for(i=0;i<N;i++)
	{
		a[i] = N-i;
	}
	for(i=0;i<N;i++)
    {
        printf("%d\n", a[i]);
    }
	insertionsort(a);
    end = clock();
    total_time = ((double)(end-start)/CLOCKS_PER_SEC);
    printf("Total processing time is %4f seconds.\n", total_time);
}

