#include<stdio.h>
int s[20];
int top = -1;
void push(int a)
{
        s[top++] = a;
}
int pop()
{
        return s[top--];
}
int main()
{
        char postfix[20];
        char *pix;
        int m1,m2,m3,num;
        printf("Enter the postfix expression :\n");
        scanf("%s",postfix);
        pix = postfix;
        while(*pix != '\0')
        {
            if(isdigit(*pix))
            {
                num = *pix - 48;
                push(num);
            }
            else
            {
                m1 = pop();
                m2 = pop();
                switch(*pix)
                {
                    case '+':
                    {
                        m3 = m1 + m2;
                        break;
                    }
                    case '-':
                    {
                        m3 = m2 - m1;
                        break;
                    }
                    case '*':
                    {
                        m3 = m1 * m2;
                        break;
                    }
                    case '/':
                    {
                        m3 = m2 / m1;
                        break;
                    }
                }
                push(m3);
            }
                pix++;
        }
        printf("The result of expression %s  =  %d\n",postfix,pop());
        return 0;
}
/*Enter the postfix expression :
abc*+
The result of expression abc*+  =  3721
*/
