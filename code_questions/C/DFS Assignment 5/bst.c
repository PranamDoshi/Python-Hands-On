#include<stdio.h>
#include<stdlib.h>
struct treenode
{
	int value;
	struct treenode* l, *r;
};
void posttraverse(struct treenode* root)
{
	if(root == NULL)
	{
		return;
	}
    posttraverse(root->l);
    posttraverse(root->r);
    printf("%d\n", root->value);
}
void pretraverse(struct treenode* root)
{
	if(root == NULL)
	{
		return;
	}
    printf("%d\n", root->value);
    pretraverse(root->l);
    pretraverse(root->r);
}
void intraverse(struct treenode* root)
{
	if(root == NULL)
	{
		return;
	}
    intraverse(root->l);
    printf("%d\n", root->value);
    intraverse(root->r);
}
struct treenode* fndmin(struct treenode* rptr)
{
    while(rptr->l != NULL)
        rptr = rptr->l;
    return rptr;
}
void printGivenLevel(struct treenode* root, int level)
{
    if (root == NULL)
        return;
    if (level == 1)
        printf("%d ", root->value);
    else if (level > 1)
    {
        printGivenLevel(root->l, level-1);
        printGivenLevel(root->r, level-1);
    }
}
int height(struct treenode* node)
{
    if (node==NULL)
        return 0;
    else
    {
        int lheight = height(node->l);
        int rheight = height(node->r);
        if (lheight > rheight)
            return(lheight+1);
        else return(rheight+1);
    }
}
void printLevelOrder(struct treenode* root)
{
    int h = height(root);
    int i;
    for (i=1; i<=h; i++)
        printGivenLevel(root, i);
}
struct treenode* insert1(struct treenode *root, int val)
{
	struct treenode* temp, *newnode;
	newnode = (struct treenode*)malloc(sizeof(struct treenode));
	if(newnode==NULL)
	{
		printf("malloc failed.\n");
		exit(0);
	}
	newnode->value = val;
	newnode->l = NULL;
	newnode->r = NULL;
	if(root == NULL)
	{
		root = newnode;
		return root;
	}
	temp = root;
	while(1)
	{
		if(val < temp->value)
		{
			if(temp->l == NULL)
			{
				temp->l = newnode;
				break;
			}
		temp = temp->l;
		}
		else
		{
			if(temp->r==NULL)
			{
				temp->r = newnode;
				break;
			}
		temp = temp->r;
		}
	}
	return root;
}
struct node *insert2(struct treenode* root, int val)
{
    if(root==NULL)
    {
        struct treenode *newnode;
        newnode=(struct treenode*)malloc(sizeof(struct treenode));
        if(newnode==NULL)
        {
            printf("MEMORY ALLOCATION FAILED\n");
            exit(-1);
        }
        newnode->value = val;
        newnode->l = NULL;
        newnode->r = NULL;
        root=newnode;
        return root;
    }
    if(val<root->value)
    {
        root->l = insert2(root->l, val);
        return root;
    }
    if(val>=root->value)
    {
        root->r = insert2(root->r, val);
        return root;
    }
}
void delete1(struct treenode *root,int val)
{
    struct treenode *droot, *temp=NULL;
    while((root -> value != val) && (root != NULL))
    {
        if(val > root -> value)
        {
            temp = root;
            root = root -> r;
        }
        else if(val < root -> value)
        {
            temp = root;
            root = root ->l;
        }
    }
    printf("\n%d", root -> value);
    if(root ->value == val)
    {
        if((temp->value < root->value) && (root -> l == NULL))
        {
            temp->r = root->r;
        }
        else if((temp->value < root->value) && (root -> r == NULL))
        {
            temp->r = root->l;
        }
        else if((temp->value > root->value) && (root -> l == NULL))
        {
            temp->l = root->r;
        }
        else if((temp->value > root->value) && (root -> r == NULL))
        {
            temp->l = root->l;
        }
        else
        {
            droot= root;
            temp = root;
            root = root ->r;
            while(root ->l != NULL)
            {
                temp = root;
                root = root -> l;
            }
            temp ->l = NULL;
            droot -> value = root -> value;
            temp -> l = root ->r;
        }
        free(root);
    }
}
struct treenode* delete2(struct treenode* root, int val)
{
    struct treenode* temp, *ptr;
    if(root == NULL)
        return root;
    if(val<root->value)
        root->l = delete2(root->l, val);
    else if(val>root->value)
        root->r = delete2(root->r, val);
    else
        {
            if(root->l == NULL && root->r == NULL)
            {
                free(root);
                return NULL;
            }
            if(root->l == NULL)
            {
                temp = root->r;
                free(root);
                return temp;
            }
            if(root->r == NULL)
            {
                temp = root->l;
                free(root);
                return temp;
            }
            ptr = findmin(root->r);
            root->value = ptr->value;
            root->r = delete2(root->r, ptr->value);
        }
        return root;
}
struct treenode* clonetree(struct treenode *root)
{
    struct treenode* r1;
    r1 = (struct treenode*)malloc(sizeof(struct treenode));
    if(r1 == NULL)
    {
        printf("Malloc failed....\n");
        exit(-1);
    }
    r1->value = root->value;
    r1->l = clonetree(root->l);
    r1->r = clonetree(root->r);
    return r1;
} ;
int main()
{
	struct treenode* root1, *r1, *root2;
	int i, j, k;
	root1 = root2 = NULL;
	int v, u;
    while(1)
    {
    printf("Enter 0 for iterative insertion\n");
    printf("Enter 1 for recursive insertion\n");
    printf("Enter 2 to end insertion\n");
    scanf("%d", &j);
    switch(j)
    {
    case 0:
        {
            printf("Insert the value to add into tree.(-1 to end.)\n");
            scanf("%d", &v);
            root1 = insert1(root1, v);
            break;
        }
    case 1:
        {
            printf("Insert the value to add into tree.(-1 to end.)\n");
            scanf("%d", &v);
            root2 = insert2(root2, v);
            break;
        }
    case 2:
        {
            exit(-1);
        }
    }
    }
    printf("Enter 1 for inorder traversal\n");
    printf("2 for preorder traversal\n");
    printf("3 for postorder traversal and 0 to treminate\n");
    printf("4 for level order traversal\n");
    scanf("%d", &i);
    switch(i)
    {
    case 1:
        {
                intraverse(root1);
                intraverse(root2);
                break;
        }
    case 2:
        {
                pretraverse(root1);
                pretraverse(root2);
                break;
        }
    case 3:
        {
                posttraverse(root1);
                posttraverse(root2);
                break;
        }
    case 0:
        {
            exit(-1);
        }
    case 4:
        {
            printLevelOrder(root1);
            printLevelOrder(root2);
            break;
        }
    }
    do
    {
    printf("Enter 0 for iterative deletion\n");
    printf("Enter 1 for recursive deletion\n");
    printf("Enter 2 to end deletion\n");
    scanf("%d", &k);
    switch(k)
    {
    case 0:
        {
            printf("Enter the value to delete from tree\n");
            scanf("%d", &u);
            root1 = delete1(root1, u);
            break;
        }
    case 1:
        {
            printf("Enter the value tp delete from tree\n");
            scanf("%d", &u);
            root2 = delete2(root2, u);
            break;
        }
    case 2:
        {
            exit(-1);
        }
    }
    printf("Enter 0 for iterative deletion\n");
    printf("Enter 1 for recursive deletion\n");
    printf("Enter 2 to end deletion\n");
    scanf("%d", &k);
    }
    while(k!=2);
    printf("Enter 1 for inorder traversal\n");
    printf("2 for preorder traversal\n");
    printf("3 for postorder traversal and 0 to treminate\n");
    printf("4 for level traversal\n");
    scanf("%d", &i);
    switch(i)
    {
    case 1:
        {
                intraverse(root1);
                intraverse(root2);
                break;
        }
    case 2:
        {
                pretraverse(root1);
                pretraverse(root2);
                break;
        }
    case 3:
        {
                posttraverse(root1);
                posttraverse(root2);
                break;
        }
    case 0:
        {
            exit(-1);
        }
    case 4:
        {
            printLevelOrder(root1);
            printLevelOrder(root2);
            break;
        }
    }
    r1 = clonetree(root1);
    printf("\t\t\tClone Tree:-\n");
    printf("Enter 1 for inorder traversal\n");
    printf("2 for preorder traversal\n");
    printf("3 for postorder traversal and 0 to treminate\n");
    printf("4 for level trversal\n");
    scanf("%d", &i);
    switch(i)
    {
    case 1:
        {
                intraverse(r1);
                break;
        }
    case 2:
        {
                pretraverse(r1);
                break;
        }
    case 3:
        {
                posttraverse(r1);
                break;
        }
    case 0:
        {
            exit(-1);
        }
    case 4:
        {
            printLevelOrder(r1);
            break;
        }
    }
}
