from myhdl import ConcatSignal, always_comb, block, Signal, instances, intbv
from adder import half_adder, full_adder
from gates import and_gate
from adder_nbit import adder_nbit

@block
def multiplier_nbit(mult, a, b):

    cout_ls = [Signal(bool()) for i in range(6)]
    sum_ls = [Signal(bool()) for i in range(6)]
    and_out = [Signal(bool()) for i in range(16)]

    mult4 = Signal(intbv(0))

    and_gate0 = and_gate(and_out[0], a(0), b(0))
    and_gate1 = and_gate(and_out[1], a(1), b(0))
    and_gate2 = and_gate(and_out[2], a(2), b(0))
    and_gate3 = and_gate(and_out[3], a(3), b(0))
    and_gate4 = and_gate(and_out[4], a(0), b(1))
    and_gate5 = and_gate(and_out[5], a(1), b(1))
    and_gate6 = and_gate(and_out[6], a(2), b(1))
    and_gate7 = and_gate(and_out[7], a(3), b(1))
    and_gate8 = and_gate(and_out[8], a(0), b(2))
    and_gate9 = and_gate(and_out[9], a(1), b(2))
    and_gate10 = and_gate(and_out[10], a(2), b(2))
    and_gate11 = and_gate(and_out[11], a(3), b(2))
    and_gate12 = and_gate(and_out[12], a(0), b(3))
    and_gate13 = and_gate(and_out[13], a(1), b(3))
    and_gate14 = and_gate(and_out[14], a(2), b(3))
    and_gate15 = and_gate(and_out[15], a(3), b(3))
    
    half_adders0 = half_adder(cout_ls[0], sum_ls[0], and_out[2], and_out[5])
    full_adders0 = full_adder(cout_ls[1], sum_ls[1], and_out[3], and_out[6], and_out[9])
    full_adders1 = full_adder(cout_ls[2], sum_ls[2], and_out[7], and_out[10], and_out[13])

    half_adders1 = half_adder(cout_ls[3], sum_ls[3], cout_ls[0], sum_ls[1])
    half_adders2 = half_adder(cout_ls[4], sum_ls[4], cout_ls[1], sum_ls[2])
    full_adders2 = full_adder(cout_ls[5], sum_ls[5], cout_ls[2], and_out[11], and_out[14])

    s1 = [cout_ls[5], cout_ls[4], cout_ls[3], sum_ls[3], sum_ls[0], and_out[1], and_out[0]]
    s2 = [and_out[15], sum_ls[5], sum_ls[4], and_out[12], and_out[8], and_out[4], Signal(bool(0))]

    s1 = ConcatSignal(*s1)
    s2 = ConcatSignal(*s2)
    
    adder_8 = adder_nbit(mult4, s1, s2)

    @always_comb
    def multiplier():
        mult.next = mult4

    return instances()