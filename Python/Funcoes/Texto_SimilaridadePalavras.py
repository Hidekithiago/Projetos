from difflib import SequenceMatcher 
def similar(str1, str2): 
    return SequenceMatcher(None, str1, str2).ratio() 
test_string1 = 'Geeksforgeeks'
test_string2 = 'Geeks'
res = similar(test_string1, test_string2) 
print ("The similarity between 2 strings is : " + str(res)) 

def similar(str1, str2): 
    str1 = str1 + ' ' * (len(str2) - len(str1)) 
    str2 = str2 + ' ' * (len(str1) - len(str2)) 
    return sum(1 if i == j else 0 
               for i, j in zip(str1, str2)) / float(len(str1)) 
test_string1 = 'Geeksforgeeks'
test_string2 = 'Geeks4geeks'
res = similar(test_string1, test_string2) 
print ("The similarity between 2 strings is : " + str(res)) 

