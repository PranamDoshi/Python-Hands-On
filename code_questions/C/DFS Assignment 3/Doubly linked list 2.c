#include <stdio.h>
#include <stdlib.h>
struct Node{
    int value;
    struct Node* next;
};
struct Node* insertInOrder(struct Node* H, int val)
{
	struct Node* newNode;
	struct Node* temp;
	newNode = (struct Node*)malloc(sizeof(struct Node));

	if(newNode == NULL)
	{
		printf("\t  Malloc failed!!\n");
		return H;
	}

	newNode->value = val;

	if(H == NULL || val < H->value)
	{
		newNode->next = H;
		H = newNode;
		return H;
	}
	temp = H;

	while(temp->next != NULL && (temp->next)->value < val)
		temp = temp->next;

	newNode->next = temp->next;
	temp->next = newNode;

	return H;
}
struct  Node* InsertAtFront(struct Node* H,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp;

     if(newNode == NULL)
    {
        printf("\t   Malloc failed!!\n");
        return H;
    }

        newNode->value = val;

         newNode->next = H;
         H = newNode;
    return H;
}
struct Node* InsertAtEnd(struct Node* H,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp;

    if(newNode == NULL)
    {
        printf("\t   Malloc failed!!\n");
        exit(-1);
    }
    newNode->value = val;
    if(H == NULL)
    {
         newNode->next = newNode;
         H = newNode;
    }
    else
    {
     temp = H;
     while(temp->next != NULL)
            temp = temp->next;
     temp->next = newNode;
     newNode->next = NULL;
    }
return H;
}
struct Node* InsertAfterValue(struct Node* H,int v,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp = H;
    if(newNode == NULL)
    {
        printf("\t   Malloc failed!!\n");
        exit(-1);
    }
    newNode->value = val;

    if(v == H->value)
    {
        newNode->next = H->next;
        H->next = newNode;
        return H;
    }
    while(temp->next != NULL && temp->value != v)
        temp = temp->next;

    if(temp->next == NULL)
    {
         if(temp->value == v)
             {
               temp->next = newNode;
               newNode->next = NULL;
              }
        else
              printf("\t   Couldn't find the number\n");
    }
    else
    {
               newNode->next = temp->next;
               temp->next = newNode;
    }
    return H;
}
struct Node* InsertBeforeValue(struct Node* H,int v,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp = H;
    if(newNode == NULL)
    {
        printf("\t   Malloc failed!!\n");
        exit(-1);
    }
    newNode->value = val;

    if(v == H->value)
    {
        newNode->next = H;
        H = newNode;
        return H;
    }
    while(temp->next != NULL && (temp->next)->value != v)
        temp = temp->next;

    if(temp->next == H)
    {
         printf("\t   Couldn't find the number\n");
         return;
    }

    else
    {
        newNode->next = temp->next;
        temp->next = newNode;
    }
    return H;
}
struct Node* Delete(struct Node* H,int val)
{
    struct Node* nodeToDeletedNode;
    struct Node* temp = H;
    if(H == NULL)
    {
        printf("\t   List is empty!!\n");
        exit(-1);
    }

    if(H->value == val)
    {
        if(temp->next == NULL)
        {
        H = NULL;
        free(temp);
        return H;
        }
        nodeToDeletedNode = H;
        H = H->next;
        free(nodeToDeletedNode);

        return H;
    }
    while((temp->next)->next != NULL && (temp->next)->value != val)
        temp = temp->next;

    if((temp->next)->next == NULL)
    {
        if((temp->next)->value == val)
        {
           nodeToDeletedNode = temp->next;
           temp->next = temp->next->next;
           free(nodeToDeletedNode);
           return H;

        }
        else
        {
            printf("\t   Couldn't find the number\n");
          exit(-1);
        }

    }

    else
    {
        nodeToDeletedNode = temp->next;
        temp->next = (temp->next)->next;
        free(nodeToDeletedNode);
    }
    return H;
}
void traverse(struct Node *H)
{
    struct Node *temp = H;

    // If linked list is not empty
    if (H == NULL)
    {
        printf("\t   List is empty\n");
        return;
    }
        // Keep printing nodes till we reach the first node again
  else
    {
	   while(temp!= NULL)
	    {
		  printf("%d\n",temp->value);
		  temp = temp->next;
	    }
    }
	   printf("\n");
}
void display(struct Node* H)
{
	struct Node* temp = H;
	printf("\n");

	if(H == NULL)
        printf("\t   List is empty!!\n");

    else
    {
	   while(temp!= NULL)
	    {
		  printf("%d\n",temp->value);
		  temp = temp->next;
	    }
    }
	   printf("\n");
}
int main()
{
    int val,i,choice,num,v;
    struct Node* Head = NULL;
    struct Node* h = NULL;

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
            Head = InsertAtFront(Head,val);
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
            Head = InsertAtEnd(Head,val);
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
            Head = InsertBeforeValue(Head,v,val);
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
            Head = InsertAfterValue(Head,v,val);
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
            Head = Delete(Head,val);
        }
       }
       break;
    case 6:
        display(Head);
        break;
    case 7:
        traverse(Head);
        break;
    case 8:
        {
            printf("Enter how many values you want to enter\n");
            scanf("%d",&num);
            for(i=1;i<=num;i++)
            {
                printf("Enter the number\n");
                scanf("%d",&val);
               h = insertInOrder(h,val);
            }
            display(h);
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
4
Enter the element
1
Enter the element
2
Enter the element
3
Enter the element
4
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

4
3
2
1

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
6
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

4
3
2
1
6

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
6

Enter how many values you want to add
2
Enter the element
7
Enter the element
8
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
           Enter your choice :  4
Enter the value after you want to insert element
8

Enter how many values you want to add
9
Enter the element
23
Enter the element
4
Enter the element
5
Enter the element
7
Enter the element
8
Enter the element
2
Enter the element
3
Enter the element
45
Enter the element
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
           Enter your choice :  5

Enter how many values you want to delete
3
Enter the element
78
Enter the element
45
Enter the element
56
           Couldn't find the number

Process returned -1 (0xFFFFFFFF)*/
