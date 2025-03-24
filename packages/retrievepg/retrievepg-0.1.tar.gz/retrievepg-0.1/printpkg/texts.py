# texts.py
import pyperclip as pc
def copyprint(a):
    print(a)
    pc.copy(a)
def print_txt1():
    a="""Program:

#include <stdio.h>

void main()

{

char Operator;

float numl, num2, result = 0;

printf("Enter an Operator (+, -, *, /) :
 ");

scanf("%c", &Operator);

printf("Enter the Values for two Operands: numl and num2: 
 ");

scanf("%f%f", &numl, &num2);

switch(Operator)

{

case '+':

result = num1 + num2;break;

case '-':

result = numl -

num2;break;

case

result = num1* num2;break;

case '/:

result = num1/num2;break;

default:

printf("
 You have enetered an Invalid Operator ");

}

printf("
 The result of %f%c %f= %f", numl, Operator, num2, result);

getch();

}"""
    print(a)
    pc.copy(a)
def print_txt2():
    print("just testing")

