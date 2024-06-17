#include<stdio.h>
#include<stdlib.h>
#define N 10
struct node 
{
	int value;
	struct node* ptr;
};
struct node* insertinorder(struct node *h, int val)
{
	struct node *t, *temp;
	temp = h;
	t = (struct node*)malloc(sizeof(struct node));
	if(t==NULL)
	{
		printf("malloc failed!!\n");
		return h;
	}
	t->value = val;
	if(h == NULL || val<=h->value)
	{
		t->ptr = h;
		h = t;
		return h;
	}
	else
	{
		temp = h;
		while(temp->ptr != NULL && (temp->ptr)->value<val)
		{temp = temp->ptr;}
		t->ptr = temp->ptr;
		temp -> ptr = t;
		return h;
	}
}
void display(struct node* h)
{
	struct node* temp;
	temp = h;
	while(temp!=NULL)
	{	
		printf("%d\n", temp->value);
		temp = temp->ptr;
	}
}
struct node* insert(struct node* h, int val)
{
	struct node* temp;
	struct node* same;
	temp = h;
	while(temp->ptr!=NULL && (temp->ptr)->value!=val)
		temp = temp->ptr;
	same = temp->ptr;
	temp->ptr = (temp->ptr)->ptr;
	same->ptr = h;
	h = same;
	return h;
}
int main()
{
	struct node* h;
	h = NULL;
	int i, j;
	printf("Enter the value to add in the list.\n");
	scanf("%d", &j);
	for(i=0;i<N;i++)
	{
		h = insertinorder(h, i);
	}
	printf("\n");
	display(h);	
	h = insert(h, j);
	printf("\n"); 
	display(h);
}
