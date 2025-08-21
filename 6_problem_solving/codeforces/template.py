# from collections import defaultdict,Counter
# from os import path
# import sys
# from collections import defaultdict
# import math
# import logging
# logging.basicConfig(
#     filename='app.log',  # Log file name
#     level=logging.INFO,   # Log level
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     filemode='w'  # 'w' means overwrite; 'a' (default) means append
# )
 
# def int_inp():
#     return int(input())
# def mul_inp():
#     return map(int,input().split())
# def arr_inp():
#     return list(map(int,input().split()))
 
 
# def is_prime(n):
#     prime_flag = 0
    
#     if(n > 1):
#         for i in range(2, int(math.sqrt(n)) + 1):
#             if (n % i == 0):
#                 prime_flag = 1
#                 break
#         if (prime_flag == 0):
#             return True 
#         else:
#             return False
#     else:
#         return False
 
# def factor(x):
    
#     result = []
#     i = 1
    
#     while i*i <= x:
        
#         if x % i == 0:
#             result.append(i)
            
#             if x//i != i: 
#                 result.append(x//i)
#         i += 1
    
#     return sorted(result)
 
 
# def prime_factors(x):
    
#     result = []
#     i = 1
    
#     while i*i <= x:
        
#         if x % i == 0:
#             result.append(i)
#         i += 1
    
#     return sorted(result)
 
# import heapq
 
# def mex(arr):
 
#     # Sort the array
#     arr=sorted(arr)
#     N=len(arr)
#     mex = 0
#     for idx in range(N):
#         if arr[idx] == mex:
 
#             # Increment mex
#             mex += 1
 
#     # return mex as answer
#     return mex
# from collections import deque
 
 
# from bisect import bisect_right
# import bisect
# def isPowerOfTwo(n):
#     if (n == 0):
#         return False
#     while (n != 1):
#             if (n % 2 != 0):
#                 return False
#             n = n // 2
             
#     return True
# def countOfElements(arr, x):
#     i = bisect_right(arr, x)
#     return i
# def dist(x,y):
#     return (x**2+y**2)
 
# import math
 
# #  Calculates the binomial coefficient nCr using the logarithmic formula
# def nCr(n, r):
#     # If r is greater than n, return 0
#     if r > n:
#         return 0
     
#     # If r is 0 or equal to n, return 1
#     if r == 0 or n == r:
#         return 1
#     # Initialize the logarithmic sum to 0
#     res = 0
     
#     # Calculate the logarithmic sum of the numerator and denominator using loop
#     for i in range(r):
#         # Add the logarithm of (n-i) and subtract the logarithm of (i+1)
#         res += math.log(n-i) - math.log(i+1)
#     # Convert logarithmic sum back to a normal number
#     return round(math.exp(res))
 
# import heapq
 
 
# import heapq
# def lucky(s):
#     if len(s)%2==0:
#         n=len(s)//2 
#         if sum(map(int,list(s[:n])))==sum(map(int,list(s[n:]))):
#             return True
#     return False 
# def func(a,b,c):
#     if (abs(b-c))%2==1:
#         print(0,end=" ")
#     else:
#         if a+abs(b-c)>=(abs(b-c)//2):
#             print(1,end=" ")
#         else:
#             print(0,end=" ")
 
# def first(arr, low, high, x, n):
#     if(high >= low):
#         mid = low + (high - low) // 2
#         if((mid == 0 or x > arr[mid - 1]) and arr[mid] == x):
#             return mid
#         elif(x > arr[mid]):
#             return first(arr, (mid + 1), high, x, n)
#         else:
#             return first(arr, low, (mid - 1), x, n)
 
#     return -1
 
# MOD=10**9+7
# def check(n):
 
#     while n>0: 
#         if n%10==0 or n%10==1:
#             n=n//10
#         else:
#             return False 
#     return True
# def setBitNumber(n):
#     if (n == 0):
#         return 0
 
#     msb = 0
#     n = int(n / 2)
 
#     while (n > 0):
#         n = int(n / 2)
#         msb += 1
 
#     return (1 << msb)
# def fibonacci(n):
#     a = 0
#     b = 1
#     if n < 0:
#         print("Incorrect input")
#     elif n == 0:
#         return a
#     elif n == 1:
#         return b
#     else:
#         for i in range(2, n+1):
#             c = a + b
#             a = b
#             b = c
#         return b
 
 
# def check(mid,n,m,arr):
#     sum=0
#     for i in range(n):
#         sum+=(min(mid,arr[i]))
#     return sum<=m
 
# def smallest_number_greater_than_b(a, b, k):
#     if k <= 0:
#         raise ValueError("k must be a positive integer")
    
#     # Calculate the smallest integer m such that a + m * k > b
#     diff = b - a
#     if diff < 0:
#         # If a is already greater than b, return a
#         return a
    
#     # Compute the smallest m that satisfies the condition
#     m = math.ceil(diff / k)
    
#     # Calculate and return the smallest number greater than b
#     result = a + m * k
#     return result
# def check(mid,n,k,a):
#     b=True 
#     for i in range(n):
#         if mid>=a[i]:
#             if ((mid-a[i])//k)%2!=0:
#                 b=False
#                 break 
 
#         else:
#             b=False
#             break 
#     return b
 
# import heapq
# from collections import deque
# def mod_inverse(x, mod):
#     # Fermat's Little Theorem: x^(mod-2) % mod is the modular inverse of x
#     return pow(x, mod - 2, mod)
# yes="YES"
# no="NO"
# alphabets="abcdefghijklmnopqrstuvwxyz"
# def array_gcd(a):
#     gcd=a[0]
#     for i in range(1,len(a)):
#         gcd=math.gcd(gcd,a[i]) 
#     return gcd
# import heapq 
 
# def check(arr):
#     n=len(arr)
#     for i in range(n-5):
#         if arr[i:i+5]==sorted(arr[i:i+5]):
#             return True
#         if arr[i:i+5]==sorted(arr[i:i+5],reverse=True):
#             return True
#     return False
# def solution(iter):
#     n=int_inp()
#     a=arr_inp()
#     b=arr_inp()
 
#     x,y= 0,0 
#     for i in range(n):
#         if a[i]>b[i]:
#             x+=(a[i]-b[i])
#         else:
#             y+=(b[i]-a[i])
#     print(x+1)
 
 
 
 
    
    
 
 
 
    
    
 
    
# if(path.exists('input.txt')):
#         sys.stdin = open('input.txt', 'r')
#         sys.stdout =open('output.txt','w')
# for _ in range(int_inp()):
    