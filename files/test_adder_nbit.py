from myhdl import instance, block, Signal, delay, intbv, bin
from adder_nbit import adder_nbit
import random
from adder_nbit import adder_nbit

cout, sum, a, b = [Signal(intbv(0)) for i in range(4)]

@block
def test_adder():

    adder1 = adder_nbit(sum, a, b)

    @instance
    def stimulus():
        
        print("a b =================== sum")
        for i in range(80):
            a.next, b.next = intbv(random.randrange(-64, 63)), intbv(random.randrange(-64, 63))
            yield delay(10)
            print("%s %s ================== %s" % (int(a), int(b), int(sum[8:].signed())))

    return adder1, stimulus

tb = test_adder()
tb.run_sim()