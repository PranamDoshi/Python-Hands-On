#!/bin/python3

import math
import os
import random
import re
import sys

def MinimumDepositError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value

def MinimumBalanceError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value

def Bank_ATM(balance,choice,amount):
    if balance < 500:
        raise ValueError('As per the Minimum Balance Policy, Balance must be at least 500')
    if choice == 1:
        if amount < 2000:
            raise MinimumDepositError('The Minimum amount of Deposit should be 2000.')
        else:
            balance += amount
            print('Updates Balance Amount: ', balance)
    elif choice == 2:
        if (balance - amount) < 500:
            raise MinimumBalanceError('You cannot withdraw this amount due to Minimum Balance Policy')
        else:
            balance -= amount
            print('Updated Balance Amount: ', balance)
        
if __name__ == '__main__':
    
    bal = int(input())
    ch = int(input())
    amt = int(input())
    
    try:
        Bank_ATM(bal,ch,amt)
    
    
    except ValueError as e:
        print(e)
    except MinimumDepositError as e:
        print(e)
    except MinimumBalanceError as e:
        print(e)




