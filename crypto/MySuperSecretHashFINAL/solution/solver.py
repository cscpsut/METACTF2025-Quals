import string
from sage.all import *

chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '{}_!?'
table = {c: i for i, c in enumerate(chars)}
hash = "CHCJAJBBGD-CHCDEGDIJB-CCDBDADHBJ-CCBFCCFIED-CDABJADDBH-CCFBEGEGFD-DECAABHCGD-DCAEAAAGAH-DHCGABCDJH-DGCJIJDBHB-CCJGJBAHGB-CDAJGHCGJB-DBABFBHCDH-DBFACJADIB-CGHIJCGGFH-CGBJBFJGFD-CCFGEEEFDF-CBBBEDFCAD-DEHGFIJEFB-DDHJEHEGDJ-CECJCJACGB-CDAEECGDBD-DAAJBBDGCH-DAIACJHGEJ-BIAJEHDHBH-BHJJDBHJDJ-DFSDF"
hash = hash.split('-')
nums = []

for word in hash:
    num = "".join([str(chars.index(c)) for c in word])
    nums.append(int(num))
    
    
nums = nums[:-1]
equations = [(nums[i], nums[i+1]) for i in range(0, len(nums), 2)]
print(equations)
flag = ''

for eqs in equations:
    eq1, eq2 = eqs
    found = False
    for i in range(len(chars)):
        if found: 
            break
        for j in range(len(chars)):
            if found:
                break
            a, b = var('a'), var('b')
            es = [
                eq1 == (i**2 * a + b * a + i),
                eq2 == (j**2 * a + b * a + j)
            ]
            sols = solve(es, a, b)
            if sols:
                # print(sols)
                a_val, b_val = sols[0][0].rhs(), sols[0][1].rhs()
                
                if a_val in ZZ and b_val in ZZ and is_prime(a_val) and is_prime(b_val):
                    print(f"Found a: {a_val}, b: {b_val} for i: {i}, j: {j}")
                    flag += chars[i] + chars[j]
                    found = True
                    
    print(f"Current flag: {flag}")
print(f"Flag: {flag}")