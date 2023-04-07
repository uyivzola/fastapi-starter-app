def add(num1:int, num2:int=2):
    return num1+num2

def subtract(num1:int, num2:int=2):
    return num1-num2
def multiply(num1:int, num2:int=2):
    return num1*num2
def divide(num1:int, num2:int=2):
    return num1/num2
def power(num1:int, num2:int=2):
    return num1**num2
def root(num1:int, num2:int=2):
    return num1**(1/num2)


class BankAccount():
    def __init__(self,starting_balance=0):
        self.balance=starting_balance
    def deposit(self,amount):
        self.balance+=amount
    def withdraw(self,amount):
        self.balance-=amount
    def collect_interest(self):
        return self.balance*1.01