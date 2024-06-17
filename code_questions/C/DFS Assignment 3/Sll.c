#include<stdio.h>
#include<stdlib.h>
struct node
{
    int value;
    struct node *ptr;
};
struct node *insert_at_front(struct node *h, int v)
{
    struct node *newnode;
    newnode=(struct node *)malloc(sizeof(struct node));
    if(newnode==NULL)
    {
        printf("MEMORY ALLOCATION FAILED\n");
        exit(-1);
    }
    else
    {
        newnode->value=v;
        newnode->ptr=h;
        h=newnode;
        return h;
    }
}
struct node *insert_at_end(struct node *h, int v)
{
    struct node *newnode, *temp;
    newnode=(struct node *)malloc(sizeof(struct node));
    if(newnode==NULL)
    {
        printf("MEMORY ALLOCATION FAILED\n");
        exit(-1);
    }
    newnode->value=v;
    if(h==NULL)
    {
        newnode->ptr=NULL;
        h=newnode;
    }
    temp=h;
    while(temp->ptr!=NULL)
        temp=temp->ptr;
    if(temp->ptr==NULL)
    {
        newnode->ptr=NULL;
        temp->ptr=newnode;
    }
    return h;
}
struct node *insert_in_ordered_list(struct node *h, int v)
{
    struct node *newnode, *temp;
    newnode=(struct node *)malloc(sizeof(struct node));
    if(newnode==NULL)
    {
        printf("MEMORY ALLOCATION FAILED\n");
        exit(-1);
    }
    newnode->value=v;
    if(h==NULL || v<h->value)
    {
        newnode->ptr=h;
        h=newnode;
        return h;
    }
    temp=h;
    while(temp->ptr!=NULL && (temp->ptr)->value<v)
        temp=temp->ptr;
    if(temp->ptr==NULL || (temp->ptr)->value>v)
    {
		newnode->ptr=temp->ptr;
		temp->ptr=newnode;
        return h;
	}
}
struct node *insert_before(struct node *h, int v, int a)
{
    struct node *newnode, *temp;
    newnode=(struct node *)malloc(sizeof(struct node));
    if(newnode==NULL)
    {
        printf("MEMORY ALLOCATION FAILED\n");
        exit(-1);
    }
    if(h->ptr==NULL && h->value!=v)
    {
        printf("NODE NOT FOUND\n");
        exit(-1);
    }
    if(h->value==v)
    {
        h=insert_at_front(h, a);
        return h;
    }
    temp=h;
    while(temp->ptr!=NULL && (temp->ptr)->value!=v)
        temp=temp->ptr;
    if(temp->ptr==NULL)
    {
        printf("NODE NOT FOUND\n");
        exit(-1);
    }
    else
    {
        newnode->value=a;
        newnode->ptr=temp->ptr;
        temp->ptr=newnode;
        return h;
    }
}
struct node *insert_after(struct node *h, int v, int a)
{
    struct node *newnode, *temp;
    newnode=(struct node *)malloc(sizeof(struct node));
    if(newnode==NULL)
    {
        printf("MEMORY ALLOCATION FAILED\n");
        exit(-1);
    }
    if(h->ptr==NULL && h->value!=v)
    {
        printf("NODE NOT FOUND\n");
        exit(-1);
    }
    if(h->value==v)
    {
        h=insert_at_end(h, a);
        return h;
    }
    temp=h;
    while(temp->ptr!=NULL && temp->value!=v)
        temp=temp->ptr;
    if(temp->ptr==NULL && temp->value!=v)
    {
        printf("NODE NOT FOUND\n");
        exit(-1);
    }
    else
    {
        newnode->value=a;
        newnode->ptr=temp->ptr;
        temp->ptr=newnode;
        return h;
    }
}
void display(struct node *h)
{
    struct node *temp=h;
    if(temp==NULL)
    {
        printf("EMPTY LIST\n");
    }
    while(temp->ptr!=NULL)
    {
        printf("%d\n", temp->value);
        temp=temp->ptr;
    }
    if(temp->ptr==NULL)
    printf("%d\n", temp->value);
}
struct node *delete_front(struct node *h)
{
    struct node *ntd;
    if(h==NULL)
    {
        printf("EMPTY LIST\n");
        exit(-1);
    }
    else
    {
        ntd=h;
        h=h->ptr;
        free(ntd);
        return h;
    }
}
struct node*delete_end(struct node *h)
{
    struct node *ntd, *temp;
    if(h==NULL)
    {
        printf("EMPTY LIST\n");
        exit(-1);
    }
    if(h->ptr==NULL)
    {
        ntd=h;
        h=NULL;
        free(ntd);
        return h;
    }
    temp=h;
    while((temp->ptr)->ptr!=NULL)
        temp=temp->ptr;
    if((temp->ptr)->ptr==NULL)
    {
        ntd=temp->ptr;
        temp->ptr=NULL;
        free(ntd);
        return h;

    }
}
struct node *delete(struct node *h, int v)
{
    struct node *temp=h;
    struct node *ntd;
    if(h==NULL)
    {
        printf("EMPTY LIST\n");
        exit(-1);
    }
    if(h->value==v)
    {
        ntd=h;
        h=h->ptr;
        free(ntd);
        return h;
    }
    while(temp->ptr!=NULL && (temp->ptr)->value!=v)
        temp=temp->ptr;
    if(temp->ptr==NULL)
    {
        printf("ELEMENT NOT FOUND\n");
        exit(-1);
    }
    else
    {
        ntd=temp->ptr;
        temp->ptr=ntd->ptr;
        free(ntd);
        return h;
    }
}
void main()
{
    struct node *head, *head1;
    int a,c,v,x,d,val;
    head=NULL;
    head1=NULL;
    while(c!=-1)
    {
        printf("Enter\n 1 - To Insert in Front\n 2 - To Insert at End\n");
        printf(" 3 - To Insert in Ordered List\n 4 - To insert before a node with value\n");
        printf(" 5 - To insert after a node with value\n 6 - To display\n 7 - To delete\n 0 - To exit\n");
        scanf("%d", &c);
        switch(c)
        {
            case 0:
                c=-1;
                break;

            case 1:
                printf("Enter the Value:- ");
                scanf("%d", &v);
                head=insert_at_front(head, v);
                break;

            case 2:
                printf("Enter the Value:- ");
                scanf("%d", &v);
                head=insert_at_end(head, v);
                break;

            case 3:
                printf("Enter the Value:- ");
                scanf("%d", &v);
                head1=insert_in_ordered_list(head1, v);
                break;

            case 4:
                printf("Enter the value of the node:- ");
                scanf("%d", &v);
                printf("Enter the value which is to be inserted before a node of value %d:- ", v);
                scanf("%d", &val);
                head=insert_before(head, v, val);
                break;

            case 5:
                printf("Enter the value of the node:- ");
                scanf("%d", &v);
                printf("Enter the value which is to be inserted after a node of value %d:- ", v);
                scanf("%d", &val);
                head=insert_after(head, v, val);
                break;

            case 6:
                    printf("Enter 1 - Simple List  2 - Ordered List\n");
                    scanf("%d", &x);
                    switch(x)
                    {
                        case 1:
                            printf("The list is:-\n");
                            display(head);
                            break;

                        case 2:
                            printf("The list is:-\n");
                            display(head1);
                            break;

                        default:
                            printf("ENTER VALID CHOICE\n");
                            break;
                    }
                break;

            case 7:
                printf(" 1 - Delete from Simple List\n 2- Delete from Ordered List\n");
                scanf("%d", &a);
                switch(a)
                {
                    printf("Enter the value:- ");
                    scanf("%d", &v);
                    case 1:
                        printf("Enter\n 1 - To delete from front\n 2 - To delete from end\n 3 - To delete a node with value\n");
                        scanf("%d", &d);
                        switch(d)
                        {
                            case 1:
                                head=delete_front(head);
                                break;

                            case 2:
                                head=delete_end(head);
                                break;

                            case 3:
                                printf("Enter the value:- ");
                                scanf("%d", &v);
                                head=delete(head, v);
                                break;

                            default:
                                printf("ENTER VALID CHOICE\n");
                                break;
                        }
                        break;

                    case 2:
                        printf("Enter 1 - To delete from front\n 2 - To delete from end\n 3 - To delete a node with value\n");
                        scanf("%d", &d);
                        switch(d)
                        {
                            case 1:
                                head1=delete_front(head1);
                                break;

                            case 2:
                                head1=delete_end(head1);
                                break;

                            case 3:
                                printf("Enter the value:- ");
                                scanf("%d", &v);
                                head1=delete(head1, v);
                                break;

                            default:
                                printf("ENTER VALID CHOICE\n");
                                break;
                        }
                        break;

                    default:
                        printf("ENTER VALID CHOICE\n");
                        break;
                }
                break;

            default:
                printf("ENTER VALID INPUT\n");
                break;
        }
    }
}
/*
Enter
 1 - To Insert in Front
 2 - To Insert at End
 3 - To Insert in Ordered List
 4 - To insert before a node with value
 5 - To insert after a node with value
 6 - To display
 7 - To delete
 0 - To exit
1
Enter the Value:- 23
Enter
 1 - To Insert in Front
 2 - To Insert at End
 3 - To Insert in Ordered List
 4 - To insert before a node with value
 5 - To insert after a node with value
 6 - To display
 7 - To delete
 0 - To exit
4
Enter the value of the node:- 23
Enter the value which is to be inserted before a node of value 23:- 10
Enter
 1 - To Insert in Front
 2 - To Insert at End
 3 - To Insert in Ordered List
 4 - To insert before a node with value
 5 - To insert after a node with value
 6 - To display
 7 - To delete
 0 - To exit
6
Enter 1 - Simple List  2 - Ordered List
1
The list is:-
10
23
Enter
 1 - To Insert in Front
 2 - To Insert at End
 3 - To Insert in Ordered List
 4 - To insert before a node with value
 5 - To insert after a node with value
 6 - To display
 7 - To delete
 0 - To exit
4
Enter the value of the node:- 23
Enter the value which is to be inserted before a node of value 23:- 45
Enter
 1 - To Insert in Front
 2 - To Insert at End
 3 - To Insert in Ordered List
 4 - To insert before a node with value
 5 - To insert after a node with value
 6 - To display
 7 - To delete
 0 - To exit
6
Enter 1 - Simple List  2 - Ordered List
1
The list is:-
10
45
23
Enter
 1 - To Insert in Front
 2 - To Insert at End
 3 - To Insert in Ordered List
 4 - To insert before a node with value
 5 - To insert after a node with value
 6 - To display
 7 - To delete
 0 - To exit
0

Process returned -1 (0xFFFFFFFF)   execution time : 102.221 s
Press any key to continue.*/
