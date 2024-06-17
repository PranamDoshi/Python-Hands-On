#include<stdio.h>
#include<stdlib.h>
struct eq
{
    int power;
    int co;
    struct eq* ptr;
};
int main()
{
    struct eq *fp1, *fp2;
    int e, p, c, f;
    fp1 = 0;
    fp2 = 0;
    printf("Enter 1-To Enter in Eq 1 \n2-To Enter in Eq 2\n");
    scanf("%d", &e);
    switch(e)
    {
    case 1:
    {
        printf("Enter 0-To end adding\n 1-To add one more element\n");
        scanf("%d", &f);
        switch(f)
        {
        case 0:
        {
            exit(-1);
        }
        case 1:
        {
            printf("Enter the power and co-efficient of eq 1 eements\n");
            scanf("%d %d", &p, &c);
            insert_poly(fp1, c, p);
        }
    }
    }
    case 2:
    {
        printf("Enter 0-To end adding\n 1-To add one more element\n");
        scanf("%d", &f);
        switch(f)
        {
        case 0:
        {
            exit(-1);
        }
        case 1:
        {
            printf("Enter the power and co-efficient of eq 1 eements\n");
            scanf("%d %d", &p, &c);
            insert_poly(fp2, c, p);
        }
        }
    }
    }
    addition(fp1, fp2);
    return 0;
}
struct eq* insert_poly(struct eq *fp, int c, int p)
{
    struct eq *eq3;
    eq3=(struct eq*)malloc(sizeof(struct eq));
    if(eq3==NULL)
    {
        printf("MEMORY ALLOCATION FAILED\n");
        exit(-1);
    }
    struct eq *temp;
    temp->coeff=c;
    temp->power=p;
    if(fp==NULL || p<fp->power)
    {
        eq3->ptr=fp;
        fp=eq3;
        return fp;
    }
    temp=fp;
    while(temp->ptr!=NULL && (temp->ptr)->power<p)
        temp=temp->ptr;
    if(temp->ptr==NULL || (temp->ptr)->power>p)
    {
		eq3->ptr=temp->ptr;
		temp->ptr=eq3;
        return h;
	}
}
struct eq* addition(struct eq *fp1, struct eq *fp2)
{
    struct eq *fp, temp1, temp2;
    temp1 = fp1;
    temp2 = fp2;
    if(temp1==NULL || temp2==NULL)
    {
        printf("Equations are NULL!!!\n");
        exit(-1);
    }
    while(temp1->ptr!=NULL)
    {
        while(temp2->ptr!=NULL)
        {
            if(temp1->power==temp2->power)
            {
                insert_poly(fp, temp1->power);
                temp2 = temp2->ptr;
            }
        }
        temp1 = temp1->ptr;
    }
    display(fp);
    return 0;
}
void display(struct eq *fp)
{
    struct node* temp;
	temp = fp;
	while((temp->ptr)!=NULL)
	{
		printf("%d\t", temp->value);
		temp = temp->rptr;
	}
}
