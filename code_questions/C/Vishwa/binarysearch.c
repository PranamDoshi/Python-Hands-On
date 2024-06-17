#include<stdio.h>
#include<stdlib.h>
#include<time.h>
void binarysearch(int a[], int b);
# define N 515
int main()
{
	int a[N];
	clock_t start, end;
	double time_total;
	int i, b;
	start = clock();
            for(i=0;i<N;i++)
			{
				a[i] = i+1;
            }
            for(i=0;i<N;i++)
            {
                printf("%d\n", a[i]);
            }
            printf("Enter the value to search in array.\n");
			scanf("%d", &b);
            binarysearch(a, b);
    end = clock();
    time_total = ((double)(end-start)/CLOCKS_PER_SEC);
    printf("Total time takes is %4f seconds.\n", time_total);
}
void binarysearch(int a[], int b)
{
	int low, mid, high;
	low = 0;
	high = N-1;
	while(low<=high)
	{
		mid = (low+high)/2;
		if(a[mid]==b)
		{
			printf("Value found at index %d.\n", mid);
			return;
		}
		else if(a[mid]>b)
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
