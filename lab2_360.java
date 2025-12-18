package lab2_360;

import java.util.Random;
import java.util.Scanner;

public class lab2_360 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Random rand = new Random();

        System.out.print("Enter size of array: ");
        int n = sc.nextInt();

        int[] A = new int[n];
        System.out.print("Array: ");
        for (int i = 0; i < n; i++) {
            A[i] = rand.nextInt(201) - (100); // values between -100 and 100
            System.out.print(A[i] + " ");
        }
        System.out.println();

        // start clock
        long startTime = System.nanoTime();

        int[] result = maxSubSlow(A);
        int maxSum = result[0];
        int start = result[1];
        int end = result[2];

        // end clock
        long endTime = System.nanoTime();
        double elapsedTimeMs = (endTime - startTime) / 1_000_000.0;

        // output
        System.out.println("Max subarray sum = " + maxSum);
        System.out.print("Subarray: ");
        for (int i = start; i <= end; i++) {
            System.out.print(A[i] + " ");
        }
        System.out.println();
        System.out.println("Execution time = " + elapsedTimeMs + " ms");
    }

    public static int[] maxSubSlow(int[] A) {
        int maxSum = Integer.MIN_VALUE;
        int startIndex = 0, endIndex = 0;
        int n = A.length;

        for (int start = 0; start < n; start++) {
            for (int end = start; end < n; end++) {
                int sum = 0;
                for (int i = start; i <= end; i++) {
                    sum += A[i];
                }
                if (sum > maxSum) {
                    maxSum = sum;
                    startIndex = start;
                    endIndex = end;
                }
            }
        }
        return new int[]{maxSum, startIndex, endIndex};
    }
}

