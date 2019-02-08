import numpy as np
import pandas as pd

import re

# Read files
bfn = pd.read_csv("black_female_names.csv")
hfn = pd.read_csv("hispanic_female_names.csv")
wfn = pd.read_csv("white_female_names.csv")

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

delims = '[' + "".join(list(delims)) + ' ]'
print(delims)
#############


def tokenizeName(row):

    results = re.split(delims, row['first name'].lower().strip())
    results += re.split(delims, row['last name'].lower().strip())
    return results
 

def name2Vector(tokens):

    # Remove possible empty whitespace tokens
    tokens = [ tok for tok in tokens if tok.strip() != '']
    
    # If name composed of more than 4 pieces, just keep
    # first name, middle, possible last 2 names
    if len(tokens) > 4: 
        tokens = [ tokens[0], tokens[1], tokens[-2], tokens[-1] ]


    char2int = { chr(i) : i - 97 for i in range(97, 97 + 26) }


    alphabet_size = len(char2int)
    cutoff = 6  # Only first 6 charactes of each name will be encoded
    result = np.zeros(4*cutoff*alphabet_size)
    
    for tok in tokens:
        for i,c in enumerate(tok):
            
            # First letter of each name token will have more weight
            weight = 1
            if i ==0:
                weight = 3
            
            result[ alphabet_size*i + char2int[c] ] = weight
        
    return result

#
def angle(u,v):

    return u.dot(v) / np.sqrt(u.dot(u) * v.dot(v))




