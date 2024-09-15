/*
File_name: resonite.h
Project: test
Description: a helpfull header file for resonite containing some useful functions and variables
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
FILE *fp;
int add(int a, int b)
{
    return a + b;
}

int sub(int a, int b)
{

    return a - b;
}

int mul(int a, int b)
{
    return a * b;
}

int mod(int a, int b)
{
    return a % b;
}

int power(int a, int b)
{
    int result = 1;
    for (int i = 0; i < b; i++)
    {
        result *= a;
    }
    return result;
}

int factorial(int a)
{
    int result = 1;
    for (int i = 1; i <= a; i++)
    {
        result *= i;
    }
    return result;
}

int isPrime(int a)
{
    if (a <= 1)
    {
        return 0;
    }
    for (int i = 2; i < a; i++)
    {
        if (a % i == 0)
        {
            return 0;
        }
    }
    return 1;
}

int isEven(int a)
{
    if (a % 2 == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

int isOdd(int a)
{
    if (a % 2 != 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

int isPositive(int a)
{
    if (a > 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

int isNegative(int a)
{
    if (a < 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

void clear()
{
    printf("[H");
}



void open(char *filename)
{
    fp = fopen(filename, "r");
}

void close()
{
    fclose(fp);
}

void read()
{
    char c;
    while ((c = fgetc(fp)) != EOF)
    {
        printf("%c", c);
    }
}

void write(char *text)
{
    fprintf(fp, "%s", text);
}

void writeLine(char *text)
{
    fprintf(fp, "%s\n", text);
}

void writeInt(int num)
{
    fprintf(fp, "%d", num);
}

void writeFloat(float num)
{
    fprintf(fp, "%f", num);
}

void writeDouble(double num)
{
    fprintf(fp, "%lf", num);
}

void writeChar(char c)
{
    fprintf(fp, "%c", c);
}

void writeBool(int b)
{
    if (b == 1)
    {
        fprintf(fp, "true");
    }
    else
    {
        fprintf(fp, "false");
    }
}

void get_request(char *url)
{
    char command[100];
    sprintf(command, "curl %s", url);
    system(command);
}

void post_request(char *url, char *data)
{
    char command[100];
    sprintf(command, "curl -X POST %s -d %s", url, data);
    system(command);
}

void put_request(char *url, char *data)
{
    char command[100];
    sprintf(command, "curl -X PUT %s -d %s", url, data);
    system(command);
}

void delete_request(char *url)
{
    char command[100];
    sprintf(command, "curl -X DELETE %s", url);
    system(command);
}