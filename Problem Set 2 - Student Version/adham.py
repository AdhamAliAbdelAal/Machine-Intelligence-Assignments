import copy
temp ={
    'a':set([1,2,3]),
    'b':set([1,2,3]),
    'c':set([1,2,3]),
    'd':set([1,2,3]),
} 

temp2 = copy.deepcopy(temp)

temp2['a'] -= set([1,2])

print(temp)

print(temp2)

# to solve the problem, you should call the solve function with a problem instance and print the resul

