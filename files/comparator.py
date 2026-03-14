from myhdl import ConcatSignal, always_comb, block, delay, Signal, instances, intbv, instance
from adder_nbit import adder_nbit
import random

@block
def comparator_nbit(cmp, a, b):

    s = Signal(intbv(0))
    comp_1s = Signal(intbv(0))
    comp_2s = Signal(intbv(0))

    comp_adder = adder_nbit(comp_2s, comp_1s, Signal(intbv(1)))
    signed_adder = adder_nbit(s, a, comp_2s)

    @always_comb
    def complement_2s():
        comp_1s.next = ~b

    @always_comb
    def concatenate_4bit():
        if s(7) == 0:
            cmp.next = a
        elif s(7) == 1:
            cmp.next = b

    return instances()

cout, sum, a, b = [Signal(intbv(0)) for i in range(4)]

@block
def test_cmp():

    cmp1 = comparator_nbit(sum, a, b)

    @instance
    def stimulus():
        
        print("a b =================== sum")
        for i in range(80):
            a.next, b.next = intbv(random.randrange(-64, 63)), intbv(random.randrange(-64, 63))
            yield delay(10)
            print("%s %s ================== %s" % (int(a), int(b), int(sum[8:].signed())))

    return cmp1, stimulus

if __name__ == '__main__':
    tb = test_cmp()
    tb.run_sim()
