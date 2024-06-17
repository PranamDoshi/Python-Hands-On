#include<stdio.h>
#include<stdlib.h>
struct node
{
	int value;
	struct node* lptr;
	struct node* rptr;
};
int main()
{
	struct node *l, *r;
	l = r = NULL;
	orderinsert(&l, &r, 20);
	orderinsert(&l, &r, 25);
	orderinsert(&l, &r, 15);
	orderinsert(&l, &r, 5);
	show(l);
	return 0;
}
int orderinsert(struct node** l, struct node** r, int val)
{
	struct node *newnode, *temp;
	temp->lptr = (*l);
	temp->rptr = (*r);
	newnode = (struct node*)malloc(sizeof(struct node));
	if(newnode==NULL)
	{
		printf("Malloc failed!!\n");
		exit(-1);
	}
	newnode->value = val;
	do
	{
	if(temp==NULL)
	{
		newnode->lptr = NULL;
		newnode->rptr = NULL;
		temp = newnode;
		(temp->rptr) = newnode;
	}
	else if((temp->value)<=val)
	{
		newnode->lptr = temp;
		newnode->rptr = NULL;
			(temp->rptr) = newnode;		
	}
	else if((temp->value)>=val)
	{
		newnode->lptr = NULL;
		newnode->rptr = temp;
		temp = newnode;
		(temp->rptr) = newnode->rptr;		
	}
	temp = (temp->rptr)->rptr;		
	}
	while((temp->rptr)->rptr!=NULL);
}
void show(struct node* l)
{
	struct node* temp;
	temp = (l);		
	while((temp->rptr)!=NULL)
	{
		printf("%d\t", temp->value);		
		temp = temp->rptr;
	}
}
