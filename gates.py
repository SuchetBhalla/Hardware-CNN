from myhdl import always_comb, block

@block
def and_gate(out, a, b):

    @always_comb
    def and_out():
        out.next = (a and b)

    return and_out

@block
def and_gate_3input(out, a, b, c):

    @always_comb
    def and_out():
        out.next = (a and b and c)

    return and_out

@block
def and_gate_4input(out, a, b, c, d):

    @always_comb
    def and_out():
        out.next = (a and b and c and d)

    return and_out

@block
def and_gate_5input(out, a, b, c, d, e):

    @always_comb
    def and_out():
        out.next = (a and b and c and d and e)

    return and_out

@block
def or_gate(out, a, b):

    @always_comb
    def or_out():
        out.next = (a or b)

    return or_out

@block
def or_gate_3input(out, a, b, c):

    @always_comb
    def or_out():
        out.next = (a or b or c)

    return or_out

@block
def or_gate_4input(out, a, b, c, d):

    @always_comb
    def or_out():
        out.next = (a or b or c or d)

    return or_out

@block
def or_gate_5input(out, a, b, c, d, e):

    @always_comb
    def or_out():
        out.next = (a or b or c or d or e)

    return or_out

@block
def xor_gate(out, a, b):

    @always_comb
    def xor_out():
        out.next = (a ^ b)

    return xor_out