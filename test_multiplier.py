from myhdl import always, instance, block, Signal, delay, intbv, bin, instances
from multiplier import multiplier_nbit
import random

mult, a, b = [Signal(intbv(0)) for i in range(3)]

@block
def test_multiplier():

    mult1 = multiplier_nbit(mult, a, b)

    @instance
    def stimulus():
        
        print("a b =================== mult")
        for i in range(80):
            a.next, b.next = intbv(random.randrange(-8, 7)), intbv(random.randrange(-8, 7))
            yield delay(10)
            print("%s %s ================== %s" % (int(a), int(b), int(mult[4:].signed())))

    return instances()

tb = test_multiplier()
tb.run_sim()