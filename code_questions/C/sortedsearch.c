#include<stdio.h>
#include<stdlib.h>
void insertsort(int A[]);
#define N 100000
int i, A[N];
int main()
{

	for(i=0;i<N;i++)
	{
		A[i] = N-i;
		insertsort(A);
	}
}
void insertsort(int A[])
{
	int i, j, key;
	for(i=0;i<N;i++)
	{
		key = A[i];
		for(j=i-1;j>=0;j--)
		{
			if(A[j]>key)
				A[j+1] = A[j];
			else
				break;
		}
		A[j+1] = key;
	}
}
