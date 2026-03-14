from myhdl import ConcatSignal, always_comb, block, delay, Signal, instances, intbv
from adder import full_adder
from CLA_4bit import cla_4bit

@block
def adder_nbit(sum, a, b):

    s = [Signal(intbv(0)) for i in range(2)]
    
    cla_adders0 = cla_4bit(s[0], a(4, 0), b(4, 0), 0)
    cla_adders1 = cla_4bit(s[1], a(8, 4), b(8, 4), s[0](4))

    @always_comb
    def concatenate_4bit():
        out = list(s[1][5:]) + list(s[0][4:])
        sum4 = ConcatSignal(*out)
        sum.next = sum4

    return instances()
