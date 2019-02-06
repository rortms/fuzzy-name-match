import numpy as np
import pandas as pd

from itertools import chain
import re

# Read files
bfn = pd.read_csv("black_female_names.csv")
hfn = pd.read_csv("hispanic_female_names.csv")
wfn = pd.read_csv("white_female_names.csv")

bfn = bfn[['first name', 'last name']]
hfn = hfn[['first name', 'last name']]
wfn = wfn[['first name', 'last name']]

fn = pd.concat([bfn, hfn, wfn], ignore_index=True)

#####################
# Find special characters
def siftSpecial(s):
    '''
    Example
    -------

    >>> siftSpecial("aba-sos / barn '")
    ['-', '/', "'"]

    '''
    s = s.lower()
    regulars = "[a-z ]"
    
    m = re.match("[a-z ]*", s)
    a,b = m.span() # span of first match

    if b-a != len(s): # if first match is not whole string
        return [ c for c in re.split(regulars, s) if c != '']
    

def tokenizeNames(row):

    results = re.split(delims, row['first name'].lower().strip())
    results += re.split(delims, row['last name'].lower().strip())

    # return df.apply(lambda row:
    #                 ' '.join(row['first name'].split()).lower() + \
    #                 ' ' + \
    #                 row['last name'].split()[0].lower(), axis=1)

def name2Vector(s, length):
    # chars, " ", "-", "/", "'" correspond to indices 0,1,2,3
    # the remaining 26 are alphabet letters
    char2int = { chr(i) : i - 93 for i in range(97, 97 + 26) }
    char2int[' '] = 0
    char2int['-'] = 1
    char2int['/'] = 2
    char2int["'"] = 3

    alphabet_size = len(char2int)
    result = np.zeros(length*alphabet_size)
    
    for i,c in enumerate(s):
        result[ alphabet_size*i + char2int[c] ] = 1
        
    return result

def vector2Name(v):
    
    int2char = { i - 93 : chr(i) for i in range(97, 97 + 26) }
    int2char[0] = " "
    int2char[1] = "-"
    int2char[2] = "/"
    int2char[3] = "'"

    alphabet_size = len(int2char)
    
    result = ""
    for i in range(len(v)):
        if v[i] != 0:
            result += int2char[i % alphabet_size]
    return result
    
def angle(u,v):

    return u.dot(v) / np.sqrt(u.dot(u) * v.dot(v))


# Fix Name Spacing assure lowercase
bfn_v = bfn.apply(makeNameStrings, axis=1)
hfn_v = hfn.apply(makeNameStrings, axis=1)
wfn_v = wfn.apply(makeNameStrings, axis=1)

# Explore, long and rare pattern names
print()
print(hfn_v.iloc[hfn_v.apply(len).nlargest().index])
print('-----------')
print(bfn_v.iloc[bfn_v.apply(len).nlargest().index])
print('-----------')
print(wfn_v.iloc[wfn_v.apply(len).nlargest().index])
print('-----------')

# # Fix Name Spacing assure lowercase
# bfn = makeNameStrings(bfn)
# hfn = makeNameStrings(hfn)
# wfn = makeNameStrings(wfn)


# # Consolidate/Vectorize
# fnA = pd.concat([bfn,hfn], ignore_index=True)
# fnB = wfn
# tn = fnB[2] # test name (antoinette abidin)
# fnB = pd.concat([fnB,
#            pd.Series(['a abidin',
#                       'antoinette a',
#                       'antoinette williams',
#                       'a williams'])], ignore_index=True)

# # Find max length
# mx = pd.concat([fnA,fnB], ignore_index=True).apply(len).max()


# # print(tn)
# # tv = name2Vector(tn,mx)
# # print(vector2Name(tv))

# def compare(a,b):

#     return angle(name2Vector(a,mx),
#                  name2Vector(b,mx))
#     # if a != b:
#     #     return angle(name2Vector(a,mx),
#     #                  name2Vector(b,mx))
#     # else:
#     #     return -10000
    
# closest = fnA.apply(lambda x: compare(x,tn)).nlargest()

# print(fnA[closest.index])
# # print( compare(fnB[closest_idx], tn) )
# # print(tn)
# # print(fnB[closest_idx])

