#include<stdio.h>
#include<stdlib.h>

struct student
{
	char name[30];
	int age;
	struct student *ptr;
};

void Print(struct student *initial);
int main()
{
	struct student *First;
	struct student *Last;
	struct student *Initial=0;
	char c;
	int i=0;
	do
	{
	First = (struct student*)malloc(sizeof(struct student));
	printf("Enter the name and age of the student.\n");
	scanf(" %s %d", &First->name, &First->age);
	First->ptr=NULL;
	if(Initial==0)
	{   //printf("aaa\n");
		Initial=First;
		Last=First;
	}
	else
	{
		Last->ptr=First;
		Last = First;
	}
	printf("Do you want to add one more student?(y/n)\n");
	scanf(" %c",&c);

	i++;
	}
	while(c=='y'||c=='Y');
	Print(Initial);
	return 0;
}
void Print(struct student *initial)
{
	printf("Your given entries are displayed below:\n");
	printf("Name--age\n");
	while(initial!=NULL)
	{
		printf("\n%s--%d", initial->name, initial->age);
		initial = initial->ptr;
	}
}
