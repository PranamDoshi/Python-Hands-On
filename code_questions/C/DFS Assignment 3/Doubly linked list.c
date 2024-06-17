#include <stdio.h>
#include <stdlib.h>
struct Node{
    int value;
    struct Node* lptr;
    struct Node* rptr;
};
struct Node* insertInOrder(struct Node** l,struct Node** r, int val)
{
	struct Node* newNode;
	struct Node* temp;
	newNode = (struct Node*)malloc(sizeof(struct Node));

	if(newNode == NULL)
	{
		printf("\t  Malloc failed!!\n");
		return;
	}

	newNode->value = val;

	if(*l == NULL)
	{				//Insert at FRONT
		newNode->lptr = NULL;
		newNode->rptr = NULL;
		*l = *r = newNode;
		return;
	}
	if((*l)->value > val)
    {
        newNode->lptr = NULL;
        newNode->rptr = (*l);
        (*l)->lptr = newNode;
        (*l) = newNode;
        return;
    }
	if(val>=(*r)->value)
	{				//Insert at END
		newNode->lptr = *r;
		newNode->rptr = NULL;
		(*r)->rptr = newNode;
		(*r) = newNode;
		return;
	}
	temp = *l;
					//Insert in b/w two nodes
	while(temp->value < val)
		temp = temp->rptr;
					//newNode is to be inserted at the left of node pointed by temp
	newNode->rptr = temp;
	newNode->lptr = temp->lptr;
	temp->lptr = newNode;
	(newNode->lptr)->rptr = newNode;
	return;
}
struct  Node* InsertAtFront(struct Node** l,struct Node** r,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp = *l;

     if(newNode == NULL)
    {
        printf("\t   Malloc failed!!\n");
        return;
    }
     newNode->value = val;
    if(*l == NULL)
    {
        newNode->lptr = NULL;
        newNode->rptr = NULL;
        (*l) = (*r) = newNode;
        return;
    }
    newNode->lptr = NULL;
    newNode->rptr = (*l);
    (*l)->lptr = newNode;
    (*l) = newNode;
    return;
}
struct Node* InsertAtEnd(struct Node** l,struct Node** r,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp;

    if(newNode == NULL)
    {
        printf("\t   Malloc failed!!\n");
        exit(-1);
    }
    newNode->value = val;
    if((*l) == NULL)
    {
         newNode->lptr = NULL;
         newNode->rptr = NULL;
         (*l) = (*r) = newNode;
         return;
    }
    (*r)->rptr = newNode;
    newNode->lptr = (*r);
    newNode->rptr = NULL;
    (*r) = newNode;
   return;
}
struct Node* InsertAfterValue(struct Node** l,struct Node** r,int v,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp = (*l);
    if(newNode == NULL)
    {
        printf("\t   Malloc failed!!\n");
        exit(-1);
    }
    newNode->value = val;

    if(v == (*r)->value)
    {
        newNode->lptr = (*r);
        newNode->rptr = NULL;
        (*r)->rptr = newNode;
        return;
    }
    while(temp->rptr != NULL && temp->value != v)
        temp = temp->rptr;

    if(temp->rptr == NULL)
              printf("\t   Couldn't find the number\n");
    else
    {
               newNode->rptr = temp->rptr;
               newNode->lptr = temp;
               temp->rptr = newNode;
               (newNode->rptr)->lptr = newNode;
    }
    return;
}
struct Node* InsertBeforeValue(struct Node** l,struct Node** r,int v,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp = (*l);
    if(newNode == NULL)
    {
        printf("\t   Malloc failed!!\n");
        exit(-1);
    }
    newNode->value = val;

   if((*l)->value == v)
	{				//Insert at FRONT
		newNode->lptr = NULL;
		newNode->rptr = *l;
		(*l)->lptr = newNode;
		(*l) = newNode;
		return;
	}
	if((*r)->value == v)
    {
        newNode->lptr = (*r)->lptr;
        newNode->rptr = (*r);
        (*r)->lptr = newNode;
        (newNode->lptr)->rptr = newNode;
        return;
    }

    while(temp->rptr != NULL && temp->value != v)
        temp = temp->rptr;

    if(temp->rptr == NULL)
    {
          printf("\t   Couldn't find the number\n");
          exit(-1);
    }

    else
    {
        newNode->lptr = temp->lptr;
        newNode->rptr = temp;
        temp->lptr = newNode;
        (newNode->lptr)->rptr = newNode;
    }
    return;
}
struct Node* Delete(struct Node** l,struct Node** r,int val)
{
	struct Node* nodeToBeDeleted;
	struct Node* temp;
	if(*l == NULL)
	{
		printf("\t  List is empty!!\n");
		return;
	}
	if((*l)->value == val)
	{
		nodeToBeDeleted = (*l);
		((*l)->rptr)->lptr = NULL;
		(*l) = (*l)->rptr;
		free(nodeToBeDeleted);
		return;
	}
	if((*r)->value == val)
    {
        nodeToBeDeleted = (*r);
        ((*r)->lptr)->rptr = NULL;
        (*r) = (*r)->lptr;
        free(nodeToBeDeleted);
        return;
    }

	temp = *l;

	while(temp->rptr != NULL && temp->value != val)
		temp = temp->rptr;

	if(temp->rptr == NULL)
	{
		printf("\t  Number not found!!\n");
		return;
	}

	else
	{
		nodeToBeDeleted = temp;
		(temp->lptr)->rptr = temp->rptr;
		(temp->rptr)->lptr = temp->lptr;
		free(nodeToBeDeleted);
		return;
	}
}
void traverse(struct Node** l,struct Node** r)
{
	struct Node* temp;
	temp = *l;

	if((*l) == NULL)
    {
        printf("\t   List is empty\n");
        return;
    }

	while(temp != NULL)
	{
		printf("%d\n",temp->value);
		temp = temp->rptr;
	}
	printf("\n");
}
void display(struct Node** l,struct Node** r)
{
	struct Node* temp;
	temp = *l;

	if((*l) == NULL)
    {
        printf("\t   List is empty\n!!");
        return;
    }

	while(temp != NULL)
	{
		printf("%d\n",temp->value);
		temp = temp->rptr;
	}
	printf("\n");
}
int main()
{
    int val,i,choice,num,v;
    struct Node* Head = NULL;
    struct Node* h = NULL;
    struct Node* L = NULL;
    struct Node* R = NULL;
    struct Node* l = NULL;
    struct Node* r = NULL;

    while(1)
    {
            printf("\t   Welcome to Singly List Editor!!\n");
    printf("\t   1.Insert at front\n   \t   2.Insert at End\n  \t   3.Insert before a value\n  \t   4.Insert after a value\n  \t   5.Delete a number\n  \t   6.Display List\n  \t   7.Traverse List\n  \t   8.Insert in order\n  \t   9.Exit\n");
    printf("\t   Enter your choice :  ");
    scanf("%d",&choice);

    switch(choice)
    {
    case 1:
       {
            printf("\nEnter how many values you want to add\n");
        scanf("%d",&num);

        for(i=1;i<=num;i++)
        {
            printf("Enter the element\n");
            scanf("%d",&val);
            Head = InsertAtFront(&L,&R,val);
        }
       }
        break;
    case 2:
         {
            printf("\nEnter how many values you want to add\n");
        scanf("%d",&num);

        for(i=1;i<=num;i++)
        {
            printf("Enter the element\n");
            scanf("%d",&val);
            Head = InsertAtEnd(&L,&R,val);
        }
       }
       break;
    case 3:
         {
            printf("Enter the value before you want to insert element\n");
            scanf("%d",&v);
            printf("\nEnter how many values you want to add\n");
            scanf("%d",&num);

        for(i=1;i<=num;i++)
        {
            printf("Enter the element\n");
            scanf("%d",&val);
            Head = InsertBeforeValue(&L,&R,v,val);
        }
       }
       break;
    case 4:
        {
            printf("Enter the value after you want to insert element\n");
            scanf("%d",&v);
            printf("\nEnter how many values you want to add\n");
            scanf("%d",&num);

        for(i=1;i<=num;i++)
        {
            printf("Enter the element\n");
            scanf("%d",&val);
            Head = InsertAfterValue(&L,&R,v,val);
        }
       }
       break;
    case 5:
        {
            printf("\nEnter how many values you want to delete\n");
            scanf("%d",&num);

        for(i=1;i<=num;i++)
        {
            printf("Enter the element\n");
            scanf("%d",&val);
            Head = Delete(&L,&R,val);
        }
       }
       break;
    case 6:
        display(&L,&R);
        break;
    case 7:
        traverse(&L,&R);
        break;
    case 8:
        {
            printf("Enter how many values you want to enter\n");
            scanf("%d",&num);
            for(i=1;i<=num;i++)
            {
                printf("Enter the number\n");
                scanf("%d",&val);
               h = insertInOrder(&l,&r,val);
            }
           display(&l,&r);
        }
        break;
    case 9:
        exit(-1);

    default:
        printf("Wrong choice\n");
    }
    }
}
/*           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  1

Enter how many values you want to add
2
Enter the element
1
Enter the element
2
           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  2

Enter how many values you want to add
1
Enter the element
45
           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  6
2
1
45

           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  3
Enter the value before you want to insert element
45

Enter how many values you want to add
1
Enter the element
33
           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  6
2
1
33
45

           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  5

Enter how many values you want to delete
2
Enter the element
1
Enter the element
2
           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  6
33
45

           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  8
Enter how many values you want to enter
4
Enter the number
22
Enter the number
45
Enter the number
6
Enter the number
78
6
22
45
78

           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  8
Enter how many values you want to enter
1
Enter the number
2
2
6
22
45
78

           Welcome to Singly List Editor!!
           1.Insert at front
           2.Insert at End
           3.Insert before a value
           4.Insert after a value
           5.Delete a number
           6.Display List
           7.Traverse List
           8.Insert in order
           9.Exit
           Enter your choice :  9

Process returned -1 (0xFFFFFFFF)*/
