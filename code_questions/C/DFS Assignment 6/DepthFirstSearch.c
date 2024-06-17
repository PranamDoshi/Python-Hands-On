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
    int i,vi,vj,n,no_of_edges;
        printf("Enter number of vertices:");
        scanf("%d",&n);
            printf("Enter number of edges:");
               scanf("%d",&no_of_edges);
               for(i=0;i<no_of_edges;i++)
            {
                printf("Enter an edge(u,v):");
                scanf("%d %d",&vi,&vj);
                addEdge(graph,vi,vj);
            }
    printgraph(graph);
    DFS(graph,1);
    return 0;
    }
