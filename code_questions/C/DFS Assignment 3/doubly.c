#include<stdio.h>
#include<stdlib.h>

struct list{
int value;
struct list * lptr;
struct list * rptr;
};

void iaf(struct list**l,struct list**r,int val){

struct list*newnode;
newnode=(struct list*)malloc(sizeof(struct list));
newnode->value=val;
if(*l==NULL){
newnode->lptr=NULL;
newnode->rptr=NULL;
*l=*r=newnode;
}

else{
newnode->lptr=NULL;
newnode->rptr=*l;
(*l)->lptr=newnode;
(*l)=newnode;
}
}

void iae(struct list**l,struct list**r,int val){
struct list*newnode;
newnode=(struct list*)malloc(sizeof(struct list));
newnode->value=val;
if(*l==NULL){
newnode->lptr=NULL;
newnode->rptr=NULL;
(*l)=*r=newnode;
}
else{
newnode->lptr=*r;
newnode->rptr=NULL;
(*r)->rptr=newnode;
*r=newnode;
}
}

void iio(struct list**l,struct list**r,int val)
{
struct list *newnode;
newnode=(struct list*)malloc(sizeof(struct list));
newnode->value=val;
if(*l==NULL){
newnode->lptr=NULL;
newnode->rptr=NULL;
*l=*r=newnode;
}

if(val<((*l)->value))
{
newnode->lptr=NULL;
newnode->rptr=*l;
(*l)=newnode;
}
if(val>((*r)->value))
{
newnode->rptr=NULL;
newnode->lptr=*r;
(*r)=newnode;
}
struct list*temp=*l;
while((temp->value)<val)
temp=temp->rptr;

newnode->value=val;
newnode->lptr=temp->lptr;
newnode->rptr=temp;
(temp->lptr)->rptr=newnode;
temp->lptr=newnode;
}

void insertafter(struct list**l,struct list**r,int val,int v){
struct list * newnode,*temp;
newnode=(struct list*)malloc(sizeof(struct list));
newnode->value=val;
temp=*l;
while(temp->rptr!=NULL && temp->value!=v)
temp=temp->rptr;
if(temp->value==v)
{
newnode->lptr=temp;
temp->rptr=newnode;
newnode->rptr=temp->rptr;
(temp->rptr)->lptr=newnode;
}
else printf("No match found Sorry:(\n");
}

void insertbefore(struct list**l,struct list**r,int val,int v){
struct list*newnode,*temp;
newnode=(struct list*)malloc(sizeof(struct list));
newnode->value=val;
temp=*l;
while(temp->rptr!=NULL && temp->value!=v)
temp=temp->rptr;
if(temp->value==v){
newnode->rptr=temp;
newnode->lptr=temp->lptr;
(temp->lptr)->rptr=newnode;
temp->lptr=newnode;

}
else printf("No match found Sorry!:(\n");

}

void daf(struct list **l,struct list**r){
struct list*ntd;
if(*l==NULL)
printf("\nlist is empty\n"); exit(-1);
if(*l==*r)
{
ntd=*l;
free(ntd);
*l=*r=NULL;
}
else{
ntd=*l;
*l=ntd->rptr;
(*l)->lptr=NULL;
free(ntd);
}
}

void dal(struct list**l,struct list**r){
struct list*ntd;
if(*r==NULL){
printf("list is empty\n");exit (-1);
}
if(*l==*r){
ntd=*l;
free(ntd);
*l=*r=NULL;
}
else{
ntd=*r;
*r=ntd->lptr;
free(ntd);
}
}


void dsn(struct list**l,struct list**r,int val){
struct list * ntd;
if(val==(*l)->value)
{
ntd=*l;
(*l)=(*l)->rptr;
free(ntd);
}
if(val==(*r)->value) {
ntd=*r;
*r=(*r)->lptr;
free(ntd);
}
struct list * temp;
temp=*l;
while(temp->rptr!=NULL && temp->value != val)
temp=temp->rptr;
ntd=temp;
(temp->lptr)->rptr=temp->rptr;
(temp->rptr)->lptr=temp->lptr;
free(ntd);
}


void display(struct list**l){
while((*l)->rptr!=NULL)
{printf("%d\n",(*l)->value);
(*l)=(*l)->rptr;
}
printf("%d\n",(*l)->value);
}
void main(){
struct list*l,*r;
l=r=NULL;
iae(&l,&r,60);
display(&l);
}
