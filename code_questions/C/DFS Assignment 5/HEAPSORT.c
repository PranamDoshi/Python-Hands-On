#include<stdio.h>
#include<stdlib.h>
#define N 100
void display(int heap[], int size)
{
	int i;
	for(i=0;i<size;i++)
		printf("%d\n", heap[i]);
}
void heapsort(int heap[], int size)
{
	int temp, s=size, parent, child;
	if(size==0)
	{
		printf("Heap is empty\n");
		return ;
	}
	while(s>0)
	{
		temp=heap[0];
		heap[0]=heap[s-1];
		heap[s-1]=temp;
		s--;
		temp=heap[0];
		parent=0; child=1;
		while(child<s)
		{
			if(child+1<s && heap[child]<heap[child+1])
				child++;
			if(heap[parent]>heap[child])
				break;
			heap[parent]=heap[child];
			heap[child]=temp;
			parent=child;
			child=(2*parent)+1;
		}
	}
	display(heap, size);
}
void insert(int heap[], int size, int item)
{
	int i;
	i=size-1;
	printf("size:- %d\n", size);
	while(i>0 && item>heap[(i-1)/2])
	{
	    printf("heap[(i-1)/2]:- %d", heap[(i-1)/2]);
		heap[i]=heap[(i-1)/2];
		i=(i-1)/2;
	}
	heap[i]=item;
	for(i=0;i<size;i++)
	{
		printf("array:- %d\n", heap[i]);
	}
}
int main()
{
	int heap[N], size=0, item, ans;
	while(1)
	{
		if(size<N)
		{
			printf("Enter elements(-1 to exit):- ");
			scanf("%d", &item);
		}
		else
		{
			printf("NO SPACE\n");
			exit(-1);
		}
		if(item==-1)
			break;
        size++;
        insert(heap, size, item);
	}
	heapsort(heap, size);
	return 0;
}

