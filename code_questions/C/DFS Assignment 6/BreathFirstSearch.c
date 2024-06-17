 #include<stdio.h>
#include<stdlib.h>
#define N 10

struct node
{
int vertex;
struct node *ptr;
};

struct Graph
{
	int numvertices;
	int *visited;
	struct node **AdjList;
};
struct node* createnode(int v)
{
struct node* newNode;
newNode=(struct node *)malloc(sizeof(struct node));
newNode->vertex=v;
newNode->ptr=NULL;
return newNode;
}

struct Graph* creategraph(int vertices)
{
int i;
	struct Graph* newgraph;
newgraph=(struct Graph *)malloc(sizeof(struct Graph));
newgraph->numvertices=vertices;
newgraph->visited=malloc(vertices * sizeof(int));
newgraph->AdjList=malloc(vertices * sizeof(struct node));
for(i=0;i<vertices;i++)
{
newgraph->visited[i]=0;
newgraph->AdjList[i]=NULL;
}
return newgraph;
}

void DFS(struct Graph * graph, int vertex)
{
struct node *adjList=graph->AdjList[vertex];
struct node *temp=adjList;
	int connectedvertex;
graph->visited[vertex]=1;

while(temp!=NULL)
{
connectedvertex=temp->vertex;
if(graph->visited[connectedvertex]==0)
{
temp=temp->ptr;
}
}
}

void addEdge(struct Graph *graph,int source,int dest)
{
struct node *newNode=createnode(dest);
newNode->ptr=graph->AdjList[source];
graph->AdjList[source]=newNode;

newNode=createnode(source);
newNode->ptr=graph->AdjList[dest];
graph->AdjList[dest]=newNode;
}

void printgraph(struct Graph*graph)
{
int v;
for(v=1;v<=graph->numvertices;v++)
{
struct node *temp=graph->AdjList[v];
printf("\n Adjacency List of vertex %d \n ",v);
while(temp)
{
printf("%d ->",temp->vertex);
temp=temp->ptr;
}
printf("\n");
}
}

int main()
{
struct Graph*graph=creategraph(8);
addEdge(graph,1 ,2 );
addEdge(graph,1 ,3 );
addEdge(graph,2,4 );
addEdge(graph,2,5 );
addEdge(graph,3,6 );
addEdge(graph,3 ,7 );
addEdge(graph,4 ,8 );
addEdge(graph,5 ,8 );
addEdge(graph,6 ,8 );
addEdge(graph,7 ,8 );
printgraph(graph);
DFS(graph,1);
return 0;
}
