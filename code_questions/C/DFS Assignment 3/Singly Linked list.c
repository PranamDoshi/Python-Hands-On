#include <stdio.h>
#include <stdlib.h>
struct Node{
    int value;
    struct Node* next;
};
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

    if(H == NULL)
    {
         newNode->next = newNode;
         H = newNode;
    }

    else
    {
         newNode->next = H;
         temp = H;

         while(temp->next != H)
            temp = temp->next;

         temp->next = newNode;
         H = newNode;
    }
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
     while(temp->next != H)
            temp = temp->next;
     temp->next = newNode;
     newNode->next = H;
    }
return H;
}
struct Node* InsertInOrderedList(struct Node* H,int val)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    struct Node* temp = H;

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
         return H;
    }
    if(val < H->value)
    {
        newNode->next = H;
        temp = H;
        while(temp->next != H)
            temp = temp->next;

        temp->next = newNode;
        H = newNode;
        return H;
    }
    temp = H;
    while(temp->next != H && (temp->next)->value < val)
       {
            temp = temp->next;
       }
    if(temp->next == H)
    {
        temp->next = newNode;
        newNode->next = H;
        return H;
    }
        newNode->next = temp->next;
        temp->next = newNode;
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
    while(temp->next != H && temp->value != v)
        temp = temp->next;

    if(temp->next == H)
    {
         if(temp->value == v)
             {
               temp->next = newNode;
               newNode->next = H;
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
         while(temp->next != H)
            temp = temp->next;

         temp->next = newNode;
        return H;
    }
    while(temp->next != H && (temp->next)->value != v)
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
         if(temp->next == H)
    {
        H = NULL;
        free(temp);
        return H;
    }
        nodeToDeletedNode = H;
        while(temp->next != H)
            temp = temp->next;

        temp->next = H->next;
        H = H->next;
        free(nodeToDeletedNode);

        return H;
    }
    while((temp->next)->next != H && (temp->next)->value != val)
        temp = temp->next;

    if((temp->next)->next == H)
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
   	if(H == NULL)
        printf("\t   List is empty!!\n");

    else
    {
        temp = H->next;
        printf("%d\n",H->value);
	   while(temp!= H)
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
        temp = H->next;
        printf("%d\n",H->value);
	   while(temp!= H)
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
            printf("\t   Welcome to Circular List Editor!!\n");
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
               h = InsertInOrderedList(h,val);
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
/*           Welcome to Circular List Editor!!
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
           Welcome to Circular List Editor!!
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
4
           Welcome to Circular List Editor!!
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
4

           Welcome to Circular List Editor!!
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
4

Enter how many values you want to add
1
Enter the element
23
           Welcome to Circular List Editor!!
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
23
4

           Welcome to Circular List Editor!!
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
23

Enter how many values you want to add
1
Enter the element
45
           Welcome to Circular List Editor!!
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
23
45
4

           Welcome to Circular List Editor!!
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
45
Enter the element
23
           Welcome to Circular List Editor!!
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
4

           Welcome to Circular List Editor!!
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
56
Enter the number
7
Enter the number
89
Enter the number
2

2
7
56
89

           Welcome to Circular List Editor!!
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
