/*
 * Recursive practice with increasing level of difficulty in c#
*/



public class Program
{
    public static void Main(String[] args)
    {
       var program = new Program();
       var input1 = 5;
       var result = program.CalculateSumOfAllNonNegativeNumbers(input1); 
       Console.WriteLine(result);
    }
    // Easy - Write a recursive function that takes input n and computes the sum of all non negative numbers 
    // Bonus - print a triangle of of n using recursion
    private int CalculateSumOfAllNonNegativeNumbers(int input)
    {
        if (input == 0)
        {
            return 0;
        }
        else
        {
            return input + CalculateSumOfAllNonNegativeNumbers(input-1);
        }
    }
}
