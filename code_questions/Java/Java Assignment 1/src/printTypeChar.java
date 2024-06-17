import java.util.Scanner;
public class printTypeChar 
{
    public static void main(String args[])
    {
        Scanner cr = new Scanner(System.in);
        System.out.print("Enter any character to check its case.....\n");
        char c = cr.next().charAt(0);
        int ASCII = c;
        if(ASCII >= 65 && ASCII <= 90)
        {
            System.out.print("Entered value is UPPERCASE.....\n");
        }
        else if(ASCII >= 97 && ASCII <= 122)
        {
            System.out.print("Entered value is LOWERCASE....\n");
        }
        else 
        {
            System.out.print("Entered value is not alphabetic character....\n");
        }
    }
}
