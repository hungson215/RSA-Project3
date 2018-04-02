#!/usr/bin/python
import json, sys, hashlib

def usage():
    print """Usage:
    python recover.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)

#Code begin
def modinv(n, e):
    d = 0
    a1,a2,a3 = 1,0,n
    b1,b2,b3 = 0,1,e

    while b3!= 1:
        quotation = a3/b3
        t1,t2,t3 = a1-quotation*b1,a2 - quotation*b2, a3 - quotation*b3
        a1,a2,a3 = b1,b2,b3
        b1,b2,b3 = t1,t2,t3
    d = b2
    if d < 0:
        d = d + n
    return d

#Code from stackoverflow https://stackoverflow.com/questions/356090/how-to-compute-the-nth-root-of-a-very-big-integer
def find_invpow(x,n):
    """Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    """
    high = 1
    while high ** n <= x:
        high *= 2
    low = high/2
    while low < high:
        mid = int((low + high)) // 2 + 1
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1

def recover_msg(N1, N2, N3, C1, C2, C3):
    m = 42
    n = N1*N2*N3
    n1 = N2*N3
    n2 = N1*N3
    n3 = N1*N2
    d1 = modinv(N1,n1)
    d2 = modinv(N2,n2)
    d3 = modinv(N3,n3)
    m = find_invpow((C1*n1*d1+C2*n2*d2+C3*n3*d3) % n,3)
    # your code starts here: to calculate the original message - m
    # Note 'm' should be an integer

    # your code ends here
    
    # convert the int to message string
    msg = hex(m).rstrip('L')[2:].decode('hex')
    return msg
#Code End

def main():
    if len(sys.argv) != 2:
        usage()

    all_keys = None
    with open('keys4student.json', 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()

    data = all_keys[name]
    N1 = int(data['N0'], 16)
    N2 = int(data['N1'], 16)
    N3 = int(data['N2'], 16)
    C1 = int(data['C0'], 16)
    C2 = int(data['C1'], 16)
    C3 = int(data['C2'], 16)
    
    msg = recover_msg(N1, N2, N3, C1, C2, C3)
    print msg
    
if __name__ == "__main__":
    main()
