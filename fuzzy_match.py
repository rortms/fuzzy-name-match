import numpy as np
import pandas as pd

import re

# Read files
bfn = pd.read_csv("bf_names.csv")
hfn = pd.read_csv("hf_names.csv")
wfn = pd.read_csv("wf_names.csv")

bfn = bfn[['first name', 'last name']]
hfn = hfn[['first name', 'last name']]
wfn = wfn[['first name', 'last name']]

fn = pd.concat([bfn, hfn, wfn], ignore_index=True)

########################
# Find special characters
def siftSpecial(s):
    '''
    In: string
    out: set of non-latin alphabet characters

    Example
    -------

    >>> siftSpecial("aba-sos / barn '")
    {'-', '/', "'"}

    '''
    s = s.lower()
    regulars = "[a-z ]"
    
    m = re.match("[a-z ]*", s)
    a,b = m.span() # span of first match

    if b-a != len(s): # if first match is not whole string
        # hyphen, -, must be escaped otherwise re interprets as range, e.g., [a-z]
        return set( ( c if c != '-' else '\-' for c in re.split(regulars, s) ) )


all_strings = iter(fn.apply(lambda row: row['first name'] + row['last name'], axis=1))

delims = set()

## Sifting ##
for s in all_strings:
    deli = siftSpecial(s)
    if deli is not None:
        delims.update(deli)

delims = '[' + "".join(list(delims)) + ' ' + '.' + ']'
print(delims)
#############


def tokenizeName(name, delims):
    
    tokens = re.split(delims, name.lower().strip())

    # Remove possible empty whitespace tokens or spanish 'de'
    tokens = [ tok for tok in tokens if tok.strip() != '' and tok != 'de']

    return tokens
    
 
def tokenizeRow(row):
    
    results = tokenizeName(row['first name'], delims)
    results += tokenizeName(row['last name'], delims)
    
    return results    
    
def name2Vector(tokens):
    
    # If name composed of more than 4 pieces, just keep
    # first name, middle, possible last 2 names
    if len(tokens) > 4: 
        tokens = [ tokens[0], tokens[1], tokens[-2], tokens[-1] ]


    char2int = { chr(i) : i - 97 for i in range(97, 97 + 26) }


    alphabet_size = len(char2int)
    cutoff = 6  # Only first 6 charactes of each name will be encoded
    result = np.zeros(4*cutoff*alphabet_size)
    
    for nth_token, tok in enumerate(tokens):

        # Slight edge to first name
        weight = 3 if nth_token == 0 else 2
            
        for i,c in enumerate(tok):
            
            # First letter of each name token will have more weight
            w = 1
            if i ==0:
                w = weight
            
            result[ alphabet_size*i + char2int[c] ] = w
        
    return result

#
def angle(u,v):

    return u.dot(v) / np.sqrt(u.dot(u) * v.dot(v))


#####################
# Preliminary Testing
##

long_name_idx = hfn.apply(
    
    lambda row: row['first name'] + row['last name'], axis=1)\
                   .apply(len)\
                   .idxmax()

long_name = hfn.iloc[long_name_idx]
long_name = long_name['first name'] + long_name['last name']

## Some test names
tests = [
    
    "R.C.L",
    long_name,
]


# 
def simpleTester(source_name):
    
    test_v = name2Vector(tokenizeName(source_name, delims))
    
    max_idxs = fn.apply(tokenizeRow, axis=1)\
                 .apply(name2Vector)\
                 .apply(lambda v: angle(test_v, v)).nlargest().index
    
    return fn.iloc[max_idxs]

for t in tests:
    print(simpleTester(t))
    print("----------------")
