// fibonachi.java

import java.util.Scanner;

public class fibonachi {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
       
        int a = 0, b = 1;
        System.out.println("Fibonacci sequence: ");
        for (int i = 0; i < 10; i++) {
            System.out.print(a + " ");
            int next = a + b;
            a = b;
            b = next;
        }
        System.out.println();
        scanner.close();
    }
}
