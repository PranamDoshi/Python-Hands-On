#include<stdio.h>
#include<stdlib.h>
struct node* insertinorder(struct node* h, int val);
struct node* delete(struct node* h, int val);
void display(struct node* h);
struct node
{
	int value;
	struct node* ptr;
};
int main()
{
	struct node* H;
	int n[5], i, j;
	printf("Enter the numbers to add in linked list.\n");
	for(i=0;i<5;i++)
	{
	scanf("%d", &n[i]);
	}
	for(j=0;j<5;j++)
	{	
	H = insertinorder(H, n[j]);
	}
	printf("\n");
	printf("\n");
	display(H);	
	delete(H, 5);
	display(H);
}
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
	struct node *temp;
	temp = h;
	while(temp!=NULL)
	{
		printf("%d\n", temp->value);
		temp = temp->ptr;
	}
	
}
struct node* delete(struct node* h, int val)
{
	struct node *temp, *nd;
	temp = h;
	if(h==NULL)
	{
		printf("List empty..\n");
		exit(-1);
	}
	if(h->value==val)
	{
		nd = h;		
		h = h->ptr;
		free(nd);
		return h;
	}
	while(temp->ptr!=NULL && (temp->ptr)->value!=val)
	{
		temp = temp->ptr;
		if(temp->ptr==NULL)
		{
			printf("Not found.\n");
			return h;
		}
		else
		{
			nd = temp->ptr;
			temp->ptr = (temp->ptr)->ptr;
			free(nd);
			return h;
		}
	}	
}
