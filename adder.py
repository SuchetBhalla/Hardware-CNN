from myhdl import always_comb, block

@block
def full_adder(cout, sum, a, b, cin):


    @always_comb
    def full_add():
        sum.next = a ^ b ^ cin
        cout.next = (a and b) or ((a ^ b) and cin)

    return full_add

@block
def half_adder(cout, sum, a, b):

    @always_comb
    def half_add():
        sum.next = a ^ b
        cout.next = (a and b)

    return half_add

