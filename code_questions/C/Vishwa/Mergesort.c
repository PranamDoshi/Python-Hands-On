#include<stdio.h>
#include<stdlib.h>
#define N 1000000
int Merge(int ls[], int low, int mid, int high)
{
	int *L1, *L2;
	int N1, N2, i, j, k, v;
	N1 = mid-low+1;
	N2 = high-mid;
	L1 = (int *)malloc(sizeof(int)*(N1+1));
	L2 = (int *)malloc(sizeof(int)*(N2+1));
	if(L1 == NULL || L2 == NULL)
	{
		printf("Malloc Failed!!!\n");
		exit(-1);
	}
	for(i = 0;i<N1;i++)
	{
		L1[i] = ls[low+i];
		printf("L1:- %d\n",L1[i]);
	}
	L1[i] = RAND_MAX;
	for(j = 0;j<N2;j++)
	{
		L2[j] = ls[mid+1+j];
		printf("L2:- %d\n",L2[j]);
	}
	L2[j] = RAND_MAX;
	i=j=0;
	for(k = low;k<high + 1;k++)
	{
		if(L1[i]<=L2[j])
		{
			ls[k]=L1[i];
			i++;
		}
		else
		{
			ls[k]=L2[j];
			j++;
		}
	}
	for(v=0;v<N;v++)
    {
        printf("%d\n", ls[v]);
    }
}
void Mergesort(int ls[], int low, int high)
{
	int mid;
	if(low<high)
	{
		mid=(low+high)/2;
		printf("low:- %d,  mid:- %d,  high:- %d\n",low, mid, high);
		Mergesort(ls, low, mid);
		printf("low1:- %d,  mid1:- %d,  high1:- %d\n",low, mid+1, high);
		Mergesort(ls, mid+1, high);
		Merge(ls, low, mid, high);
    }
}
void main()
{
	int ls[N],i;
	for(i=0;i<N;i++)
	{
		ls[i]=N-i;
	}
	for(i=0;i<N;i++)
    {
        printf("VALUES:- %d\n", ls[i]);
    }
	Mergesort(ls, 0, N-1);
}
