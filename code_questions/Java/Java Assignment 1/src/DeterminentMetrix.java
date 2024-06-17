import java.util.Scanner;
public class DeterminentMetrix 
{
    public static void main(String args[])
    {
        Scanner input = new Scanner(System.in);
        double metrix[][] = new double[3][3];
        double ar[] = new double[9];
        System.out.print("Enter the number to add into the metrix...\n");
        for(int i = 0; i < 9; i++)
        {
            ar[i] = input.nextDouble();
        }
        int i = 0;
        for(int a = 0; a < 3; a++)
        {
            for(int b = 0; b<3; b++)
            {
                metrix[a][b] = ar[i];
                i++;
            }
        }
        for(int a = 0; a < 3; a++)
        {
            for(int b = 0; b<3; b++)
            {
                System.out.print(metrix[a][b] + "\t");
            }
            System.out.println();
        }
        double dmin;
        dmin = ar[0]*((ar[8]*ar[4])-(ar[5]*ar[7])) - ar[1]*((ar[3]*ar[8])-(ar[5]*ar[6])) + ar[2]*((ar[3]*ar[7])-(ar[4]*ar[6]));
        System.out.print("Determinent of the given metrix is " + dmin + "\n");
    }
}