#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define N 515000
void linearsearch(int a[], int b);
int main()
{
        int a[N];
        clock_t start, end;
        double time_total;
        int i=0, b;
        start = clock();
        for(i=0;i<N;i++)
            {
                a[i] = i+1;
            }
        printf("Enter the value to search in array.\n");
        scanf("%d", &b);
        linearsearch(a, b);
        end = clock();
        time_total = ((double)(end-start)/CLOCKS_PER_SEC);
        printf("Total processing time is %4f seconds.\n", time_total);
        return 0;
}
void linearsearch(int a[], int b)
{
	int i=0, c=0;
	for(i=0;i<N;i++)
    {
        if(a[i]==b)
        {
            printf("Value found at %dth index.\n", i);
            c++;
        }
    }
    if(c==0)
    {
        printf("Value not found.\n");
        return;
    }
}
