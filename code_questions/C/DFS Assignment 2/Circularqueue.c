#include<stdio.h>
#include<stdlib.h>
#define N 5
void insert(int dq[], int* F, int* R, int val);
int delete(int dq[], int* F, int* R);
int main()
{
	int dq[N];
	int f, r, a, i, b;
	f = r = -1;
	for(i=0;i<N;i++)
	{
		printf("Enter the number to insert in queue.\n");
		scanf("%d", &a);
		insert(dq, &f, &r, a);
	}
	for(i=0;i<N;i++)
	{
		b = delete(dq, &f, &r);
		printf("The deleted number from queue is %d.\n", b);
	}
	return 0;
}
void insert(int dq[], int* F, int* R, int val)
{
	if((((*R)+1)%N)==(*F))
	{
		printf("Queue is Full!!\n");
		exit(-1);
	}
	else
	{
		(*R) = ((*R) + 1) % N;
		dq[*R] = val;
		if((*F)=-1)
		{
			(*F) = 0;
		}
	}
}
int delete(int dq[], int* F, int* R)
{
	int B;
	if((*F)==-1)
	{
		printf("Queue is empty!!\n");
		exit(-1);
	}
	else
	{
		B = dq[*F];
		if((*F)==(*R))
		{
			(*F) = (*R) = -1;
		}
		(*F) = ((*F)+1)%N;
	}
	return B;
}
/*Enter the number to insert in queue.
1
Enter the number to insert in queue.
2
Enter the number to insert in queue.
3
Enter the number to insert in queue.
4
Enter the number to insert in queue.
5
The deleted number from queue is 1.
The deleted number from queue is 2.
The deleted number from queue is 3.
The deleted number from queue is 4.
The deleted number from queue is 5.*/
