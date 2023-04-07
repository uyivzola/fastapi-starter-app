from app.calculations import add, subtract, multiply, divide, power, root, BankAccount
import pytest



@pytest.mark.parametrize("num1,num2,expected",[
    (1,3,4),
    (2,4,6),
    (10,20,30),
    (40,40,80),
])
def test_app(num1,num2,expected):
    assert add(num1,num2) == expected


def test_subtract():
    assert subtract(10, 2) == 8


def test_multiply():
    assert multiply(3, 5) == 15


def test_divide():
    assert divide(6,3) == 2


def test_power():
    assert power(3, 2) == 9


def test_root():
    assert root(9, 2) == 3

def test_bank_set_initial_amout():
    bank_account=BankAccount(30)
    assert bank_account.balance==30

def test_bank_default_amout():
    bank_account=BankAccount()
    assert bank_account.balance==0

def test_bank_deposit_amout():
    bank_account=BankAccount(30)
    bank_account.deposit(20)   
    assert bank_account.balance==50
    
def test_bank_withdraw_amout():
    bank_account=BankAccount(30)
    bank_account.withdraw(20)   
    assert bank_account.balance==10

    
def test_bank_collect_interest():
    bank_account=BankAccount(30)
    bank_account.collect_interest()   
    assert bank_account.balance==33
