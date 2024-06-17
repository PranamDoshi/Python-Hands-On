#include<stdio.h>
#include<stdlib.h>
#include<time.h>
void binarysearch(int A[], int a);
# define N 515
int main()
{
	int A[N];
	clock_t start, end;
	double time_total;
	int i, a;
            for(i=0;i<N;i++)
			{
				A[i] = i+1;
            }
            for(i=0;i<N;i++)
            {
                printf("%d\n", A[i]);
            }
            printf("Enter the value to search in array.\n");
			scanf("%d", &a);
            start = clock();
            binarysearch(A, a);
    end = clock();
    time_total = ((double)(end-start)/CLOCKS_PER_SEC);
    printf("Total time takes is %4f seconds.\n", time_total);
}
void binarysearch(int A[], int a)
{
	int low, mid, high;
	low = 0;
	high = N-1;
	while(low<=high)
	{
		mid = (low+high)/2;
		if(A[mid]==a)
		{
			printf("Value found at index %d.\n", mid);
			return;
		}
		else if(A[mid]>a)
        {
            high = mid -1;
        }
        else
		{
		    low = mid + 1;
		}
    }
        printf("NOT Found.\n");
		return;
}
