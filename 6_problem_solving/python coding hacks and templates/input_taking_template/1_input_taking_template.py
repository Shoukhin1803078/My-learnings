
# tt=int(input())
# for _ in range(tt):
#     n=int(input())
#     a=list(map(int,input().split()))
#     b=list(map(int,input().split()))
#     ans=1
#     for i in range(n):
#         ans+=max(0,a[i]-b[i])
#     print(ans)










# 4
# 2
# 7 3
# 5 6
# 3
# 3 1 4
# 3 1 4
# 1
# 10
# 1
# 6
# 1 1 4 5 1 4
# 1 9 1 9 8 1






# ----------------------- Explanation of this line : a=list(map(int,input().split()))--------------------------




#--------my------------------------------------:
##### a=list(map(int,input().split()))

s=input()
s1=s.split(" ")
a=[]
for i in s1:
    a.append(i)

print(a)






#---------Chatgpt---------:




# user_input = input("Enter numbers separated by space: ")   # "5 10 15"
# parts = user_input.split(" ")                                # ["5", "10", "15"] Default = whitespace (" ")           string.split(separator, maxsplit) separator → (optional) by what you want to split. Default = whitespace (" "). maxsplit → (optional) how many splits to do. Default = no limit.
# # print(parts)
# # print(type(parts))
# # print(type(parts[0]))


# a = []   # empty list
# for p in parts:
#     a.append(int(p))  # convert each string to int and add to list

# print(a)   # [5, 10, 15]






# a = list(map(int, input().split()))
# |
# |
# |
# |

# Step-by-step breakdown:

# input() → asks user for input (a string).
# Example: "5 10 15"

# .split() → splits the string into pieces (default is space).
# "5 10 15".split() → ["5", "10", "15"]

# map(int, ...) → converts each string into an integer.
# ["5", "10", "15"] → [5, 10, 15] (but still as a map object)

# list(...) → finally turns it into a real Python list.
# Result: [5, 10, 15]








