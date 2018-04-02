#!/usr/bin/python
import json, sys, hashlib

def usage():
    print """Usage:
    python find_waldo.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)

#Code Begin
def gcd(a,b):
    while b != 0:
        (a,b) = (b, a % b)
    return a

#TODO -- n1 and n2 share p or q?
def is_waldo(n1, n2):
    a = gcd(n1,n2)
    if a > 1:
        return True
    else:
        return False

def get_key(p, q, e):
    d = 0
    phi = (p-1) * (q-1)
    a1,a2,a3 = 1,0,phi
    b1,b2,b3 = 0,1,e

    while b3!= 1:
        quotation = a3/b3
        t1,t2,t3 = a1-quotation*b1,a2 - quotation*b2, a3 - quotation*b3
        a1,a2,a3 = b1,b2,b3
        b1,b2,b3 = t1,t2,t3
    d = b2
    if d < 0:
        d = d + phi
    return d
#TODO -- get private key of n1
def get_private_key(n1, n2, e):
    d = 0
    p = gcd(n1,n2)
    q = n1 / p
    if p*q == n1:
        d = get_key(p,q,e)
    else:
        d = -1
    return d
#Code End
def main():
    if len(sys.argv) != 2:
        usage()

    all_keys = None
    with open("keys4student.json", 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()

    pub_key = all_keys[name]
    n1 = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)
    d = 0
    waldo = "dolores"

    print "your public key: (", hex(n1).rstrip("L"), ",", hex(e).rstrip("L"), ")"

    for classmate in all_keys:
        if classmate == name:
            continue
        n2 = int(all_keys[classmate]['N'], 16)

        if is_waldo(n1, n2):
            waldo = classmate
            d = get_private_key(n1, n2, e)
            break
    
    print "your private key: ", hex(d).rstrip("L")
    print "your waldo: ", waldo


if __name__ == "__main__":
    main()
