import java.util.Scanner;
public class Solution_1Darray_Traversing {
        public static boolean canWin(int leap, int[] game) {
        // Return true if you can win the game; otherwise, return false.
        boolean[] visited = new boolean[game.length];
        for(boolean b:visited){
            b = false;
        }
        int i = 0;
        while(i <= (game.length - 1)){
            if(i + leap >= game.length){
                return true;
            }
            else{
                if(game[i  + leap] == 0 && visited[i + leap] == false){
                    visited[i] = true;
                    i = i + leap;
                }
                else if(game[i + 1] == 0 && visited[i + 1] == false){
                    visited[i] = true;
                    i = i + 1;
                }
                else if(i - 1 >= 0){
                    if(game[i - 1] == 0 && visited[i - 1] == false){
                        visited[i] = true;
                        i = i - 1;
                    }
                    else{
                        return false;
                    }
                }
                else{
                    return false;
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int q = scan.nextInt();
        while (q-- > 0) {
            int n = scan.nextInt();
            int leap = scan.nextInt();
            scan.nextLine();
            int[] game = new int[n];
            for (int i = 0; i < n; i++) {
                game[i] = scan.nextInt();
            }
            scan.nextLine();

            System.out.println( (canWin(leap, game)) ? "YES" : "NO" );
        }
        scan.close();
    }
}