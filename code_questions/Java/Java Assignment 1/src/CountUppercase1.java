import java.util.Scanner;
public class CountUppercase1
{
    public static void main(String args[])
    {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter a String to count Uppercase letters....\n");
        String s = input.nextLine();
        int count = 0;
        for(int i = 0; i < s.length(); i++)
        {
            char c = s.charAt(i);
            int ASCII = (int) c;
            if(ASCII >= 65 && ASCII <= 90)
            {
                count += 1;
            }
        }
        System.out.print("There are " + count + " number of Uppercase letters in the given string....\n");
    }
}
