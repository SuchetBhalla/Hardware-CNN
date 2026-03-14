from myhdl import instance, block, Signal, delay, intbv, bin
from adder import full_adder, half_adder

@block
def test_adder():

    cout, sum, a, b, cin = [Signal(bool()) for i in range(5)]

    adder1 = full_adder(cout, sum, a, b, cin)

    @instance
    def stimulus():
        
        print("a b cin=================== sum cout")
        input_value = intbv(0)
        for i in range(4):
            # a.next, b.next = [int(_) for _ in bin(input_value, width=2)]
            a.next, b.next, cin.next = (True, False, False)
            yield delay(10)
            input_value += 1
            print("%s %s %s ================== %s %s" % (a, b, cin, sum, cout))

    return adder1, stimulus

tb = test_adder()
tb.run_sim()