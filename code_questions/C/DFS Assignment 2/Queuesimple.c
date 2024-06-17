#include<stdio.h>
#include<stdlib.h>
# define N 5
void insert(int Q[], int* F, int* R, int V);
int delete(int Q[], int* F, int* R);
int main()
{
	int Q[N];
	int f, r, a, i, b;
	f = r = -1;
	for(i=0;i<N;i++)
	{
		printf("Enter the number to add into queue.\n");
		scanf("%d", &a);
		insert(Q, &f, &r, a);
	}
	for(i=0;i<N;i++)
	{
		b = delete(Q, &f, &r);
		printf("The deleted number is %d.\n", b);
	}
	return 0;
}
void insert(int Q[], int* F, int* R, int V)
{
	if((*R)>=N-1)
	{
		printf("Queue is full.\n");
		exit(-1);
	}
	else
	{
		(*R)++;
		Q[*R] = V;
		if((*F)==-1)
		{
			(*F) = 0;
		}
	}
}
int delete(int Q[], int* F, int* R)
{
	int B;
	if((*R)==-1)
	{
		printf("Queue is empty!!\n");
		exit(-1);
	}
	else
	{
		B = Q[*F];
		(*F)++;
		if((*F)==N)
		{
			(*R) = -1;
			(*F) = -1;
		}
	}
	return B;
}
/*  Enter the number to add into queue.
1
Enter the number to add into queue.
2
Enter the number to add into queue.
3
Enter the number to add into queue.
4
Enter the number to add into queue.
5
The deleted number is 1.
The deleted number is 2.
The deleted number is 3.
The deleted number is 4.
The deleted number is 5.*/
