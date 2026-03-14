from myhdl import ConcatSignal, always_comb, block, delay, Signal, instances
from gates import and_gate, or_gate, xor_gate, and_gate_3input, and_gate_4input, and_gate_5input, or_gate_3input, or_gate_4input, or_gate_5input

@block
def cla_4bit(sum, a, b, cin):

    g = [Signal(bool()) for i in range(4)]
    p = [Signal(bool()) for i in range(4)]
    c = [Signal(bool()) for i in range(4)]
    s = [Signal(bool()) for i in range(4)]
    
    and_outs = [Signal(bool()) for i in range(10)]

    cout = Signal(bool())

    and_gate0 = and_gate(g[0], a(0), b(0))
    and_gate1 = and_gate(g[1], a(1), b(1))
    and_gate2 = and_gate(g[2], a(2), b(2))
    and_gate3 = and_gate(g[3], a(3), b(3))

    xor_gate0 = xor_gate(p[0], a(0), b(0))
    xor_gate1 = xor_gate(p[1], a(1), b(1))
    xor_gate2 = xor_gate(p[2], a(2), b(2))
    xor_gate3 = xor_gate(p[3], a(3), b(3))

    and_gate4 = and_gate(and_outs[0], p[0], cin)

    and_gate5 = and_gate(and_outs[1], p[1], g[0])
    and_gate6 = and_gate_3input(and_outs[2], p[1], p[0], cin)
    
    and_gate7 = and_gate(and_outs[3], p[2], g[1])
    and_gate8 = and_gate_3input(and_outs[4], p[2], p[1], g[0])
    and_gate9 = and_gate_4input(and_outs[5], p[2], p[1], p[0], cin)
    
    and_gate10 = and_gate(and_outs[6], p[3], g[2])
    and_gate11 = and_gate_3input(and_outs[7], p[3], p[2], g[1])
    and_gate12 = and_gate_4input(and_outs[8], p[3], p[2], p[1], g[0])
    and_gate13 = and_gate_5input(and_outs[9], p[3], p[2], p[1], p[0], cin)

    or_gate0 = or_gate(c[1], g[0], and_outs[0])
    or_gate1 = or_gate_3input(c[2], g[1], and_outs[1], and_outs[2])
    or_gate2 = or_gate_4input(c[3], g[2], and_outs[3], and_outs[4], and_outs[5])
    or_gate3 = or_gate_5input(cout, g[3], and_outs[6], and_outs[7], and_outs[8], and_outs[9])

    xor_gate4 = xor_gate(s[0], p[0], cin)
    xor_gate5 = xor_gate(s[1], p[1], c[1])
    xor_gate6 = xor_gate(s[2], p[2], c[2])
    xor_gate7 = xor_gate(s[3], p[3], c[3])

    s = s + [cout]
    
    sum4 = ConcatSignal(*reversed(s)) 

    @always_comb
    def list2intbv():
        sum.next = sum4

    return instances()
