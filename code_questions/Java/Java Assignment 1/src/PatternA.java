import java.util.Scanner;
public class PatternA
{
    public static void main(String args[])
    {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter the value of n....\n");
        int n = input.nextInt();
        int m = 1;
        for(int i = 1; i < n; i++)
        {
            for(int j = n; j >= i; j--)
            {
                System.out.print(" ");
            }
            for(int k = 1; k <= m; k++)
            {
                if(i == 1 || i == ((n/2)+1))
                {
                    System.out.print("A");
                }
                else
                {
                    if(k == 1 || k == m)
                    {
                        System.out.print("A");
                    }
                    else
                    {
                        System.out.print(" ");
                    }
                }
            }
            m += 2;
            System.out.println();
        }
    }
}