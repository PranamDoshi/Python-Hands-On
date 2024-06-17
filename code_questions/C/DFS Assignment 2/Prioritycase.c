#include<stdio.h>
#include<stdlib.h>
#define N 20
void insert(int Q[], int *F, int *R, int value)
{
    if((*R)+1>=N)
    {
        printf("QUEUE IS FULL\n");
        return ;
    }
    else
    {
        (*R)++;
        Q[*R]=value;
        if((*F)==-1);
            (*F)=0;
    }
}
void delete(int Q[], int *F, int *R, int c)
{
    if((*F)<=(*R))
    {
         if((*F)==(*R))
        {
            printf("The deleted element from queue %d is %d\n", c, Q[*F]);
            (*F)=(*R)=-1;
            return ;
        }
        else
        {
            printf("The deleted element from queue %d is %d\n", c, Q[*F]);
            (*F)++;
        }
    }
}
void main()
{
    int P[N], Q[N], s[N];
    int fp=-1, fq=-1, fs=-1;
    int rp=-1, rq=-1, rs=-1;
    int a=0, b=0, c=0, ch, i, val;
    printf("0 - Lowest priority queue 0.\n1 - intermediate priority queue 1.\n2 - Highest priority queue 2.\n");
    printf("Enter \n0 - to insert element queue 0.\n");
    printf("1 - to insert element in queue 1.\n");
    printf("2 - to insert element in queue 2.\n");
    printf("3 - to delete elements from all the queue.\n");
    scanf("%d", &ch);
    do
    {
        switch(ch)
        {
            case 0:
                printf("Enter the element in queue %d:- ", ch);
                scanf("%d", &val);
                insert(P, &fp, &rp, val);
                a++;
                break;

            case 1:
                printf("Enter the element in queue %d:- ", ch);
                scanf("%d", &val);
                insert(Q, &fq, &rq, val);
                b++;
                break;

            case 2:
                printf("Enter the element in queue %d:- ", ch);
                scanf("%d", &val);
                insert(s, &fs, &rs, val);
                c++;
                break;

            case 3:
                if(c==0)
                {
                    printf("QUEUE 2 IS EMPTY\n");

                }
                else
                {
                    for(i=1;i<=c;i++)
                        delete(s, &fs, &rs, 2);
                }
                if(b==0)
                {
                    printf("QUEUE 1 IS EMPTY\n");

                }
                else
                {
                    for(i=1;i<=b;i++)
                        delete(Q, &fq, &rq, 1);
                }
                if(a==0)
                {
                    printf("QUEUE 0 IS EMPTY\n");
                }
                else
                {
                    for(i=1;i<=a;i++)
                        delete(P, &fp, &rp, 0);
                }
                break;
        }
    printf("Enter \n0 - to insert element queue 0.\n");
    printf("1 - to insert element in queue 1.\n");
    printf("2 - to insert element in queue 2.\n");
    printf("3 - to delete elements from all the queue.\n");
    printf("4 - to exit\n");
    scanf("%d", &ch);
    }while(ch<4);
}
/*
0 - Lowest priority queue 0.
1 - intermediate priority queue 1.
2 - Highest priority queue 2.
Enter
0 - to insert element queue 0.
1 - to insert element in queue 1.
2 - to insert element in queue 2.
3 - to delete elements from all the queue.
0
Enter the element in queue 0:- 12
Enter
0 - to insert element queue 0.
1 - to insert element in queue 1.
2 - to insert element in queue 2.
3 - to delete elements from all the queue.
4 - to exit
1
Enter the element in queue 1:- 23
Enter
0 - to insert element queue 0.
1 - to insert element in queue 1.
2 - to insert element in queue 2.
3 - to delete elements from all the queue.
4 - to exit
2
Enter the element in queue 2:- 34
Enter
0 - to insert element queue 0.
1 - to insert element in queue 1.
2 - to insert element in queue 2.
3 - to delete elements from all the queue.
4 - to exit
3
The deleted element from queue 2 is 34
The deleted element from queue 1 is 23
The deleted element from queue 0 is 12
Enter
0 - to insert element queue 0.
1 - to insert element in queue 1.
2 - to insert element in queue 2.
3 - to delete elements from all the queue.
4 - to exit
4*/
