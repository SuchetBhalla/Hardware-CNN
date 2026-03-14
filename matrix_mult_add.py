#low, high= 0, 1
inactive, active= 0, 1

from myhdl import *
from multiplier import multiplier_nbit
from adder_nbit import adder_nbit
import random

@block
def buffer(a, b, clk, enable, reset):
    
    #Trigger: This buffer is triggered by the negative-edge of the clock-signal
    #A sequential circuit requires a 'reset' [signal]
    @always_seq(clk.negedge, reset= reset)
    def job():
        if enable == active:
            a.next= b
    
    return job

@block
def test():
    
    #INTIALIZATION
    #1
    reset= ResetSignal(0, active= 1, isasync= True)
    enable= Signal(bool(0))
    
    #2
    clk= Signal(bool(0))
    half_period= 10
    @always(delay( half_period ))
    def clk_driver():
        clk.next= not clk
      
    #3.a.
    rows= 5
    columns= 4
    stride= 1
    
    #3.b. creating a random matrix
    size_of_matrix= columns*rows
    matrix= [Signal(intbv(i)[4:0]) for i in range(size_of_matrix)]
    
    #4. Ports [i.e., variables]
    #input
    i1, i2, i3, i4, i5, i6, i7, i8, i9=  [Signal(intbv(0)[4:])  for i in range(9)]
    #output
    o1, o2, o3, o4, o5, o6, o7, o8, o9=  [Signal(intbv(0)[4:])  for i in range(9)]
    #END of INTIALIZATION
    
    #Nine buffers
    b1= buffer(o1, i1, clk, enable, reset)
    b2= buffer(o2, i2, clk, enable, reset)
    b3= buffer(o3, i3, clk, enable, reset)
    b4= buffer(o4, i4, clk, enable, reset)
    b5= buffer(o5, i5, clk, enable, reset)
    b6= buffer(o6, i6, clk, enable, reset)
    b7= buffer(o7, i7, clk, enable, reset)
    b8= buffer(o8, i8, clk, enable, reset)
    b9= buffer(o9, i9, clk, enable, reset)
    
    #add your code here
    kernel= [Signal(intbv(1)[4:]), Signal(intbv(5)[4:]), Signal(intbv(10)[4:]), \
            Signal(intbv(0)[4:]), Signal(intbv(1)[4:]), Signal(intbv(2)[4:]), \
                Signal(intbv(3)[4:]), Signal(intbv(0)[4:]), Signal(intbv(1)[4:])]

    product= [Signal(intbv(0)[8:]), Signal(intbv(0)[8:]), Signal(intbv(0)[8:]), \
            Signal(intbv(0)[8:]), Signal(intbv(0)[8:]), Signal(intbv(0)[8:]), \
                Signal(intbv(0)[8:]), Signal(intbv(0)[8:]), Signal(intbv(0)[8:])]

    addition = [Signal(intbv(0)) for i in range(8)]

    m1 = multiplier_nbit(product[0], o1, kernel[0])
    m2 = multiplier_nbit(product[1], o2, kernel[1])
    m3 = multiplier_nbit(product[2], o3, kernel[2])
    m4 = multiplier_nbit(product[3], o4, kernel[3])
    m5 = multiplier_nbit(product[4], o5, kernel[4])
    m6 = multiplier_nbit(product[5], o6, kernel[5])
    m7 = multiplier_nbit(product[6], o7, kernel[6])
    m8 = multiplier_nbit(product[7], o8, kernel[7])
    m9 = multiplier_nbit(product[8], o9, kernel[8])

    adder1 = adder_nbit(addition[0], product[0], product[1])
    adder2 = adder_nbit(addition[1], addition[0], product[2])
    adder3 = adder_nbit(addition[2], product[3], product[4])
    adder4 = adder_nbit(addition[3], addition[2], product[5])
    adder5 = adder_nbit(addition[4], product[6], product[7])
    adder6 = adder_nbit(addition[5], addition[4], product[8])
    adder7 = adder_nbit(addition[6], addition[1], addition[3])
    adder8 = adder_nbit(addition[7], addition[6], addition[5])


    #Trigger: This hardware is triggered by the negative-edge of the clock-signal
    @instance
    def job():
        
        #In the first cycle, I want to "flush" (the contents of) the buffer
        reset.next= active
        print("Time elapsed %2d : Buffers have been reset" % now())
        
        yield clk.negedge
        
        #In the second cycle, I want to "enable" the buffer
        reset.next= inactive
        enable.next= active
        print("Time elapsed %2d : Buffers have been enabled" % now())
        print('-'*63)
        print('-'*63)
        
        #In each cycle, 4 elements from the matrix are transferred into a buffer.
        
        #Why have I written the following expression within "range()"? Because range() does not accept variable arguments
        for r in range( *{'start': 0,'stop': (rows-2),'step': stride}.values() ):
            for c in range( *{'start': 0,'stop': (columns-2),'step': stride}.values() ):

                i1.next= matrix[r*columns +c]
                i2.next= matrix[r*columns + (c+1)]
                i3.next= matrix[r*columns + (c+2)]
                
                i4.next= matrix[(r+1)*columns + c]
                i5.next= matrix[(r+1)*columns + (c+1)]
                i6.next= matrix[(r+1)*columns + (c+2)]
                
                i7.next= matrix[(r+2)*columns + c]
                i8.next= matrix[(r+2)*columns + (c+1)]
                i9.next= matrix[(r+2)*columns + (c+2)]
                
                #Return to the caller on the next trigger/cycle
                yield clk.negedge
        
        #To update the last 'transfer', this instruction is necessary.
        yield clk.negedge
        
        #Disables the buffer
        enable.next= inactive
        
        print('-'*63)
        print('-'*63)
        print("Time elapsed %d nsec: Buffers have been disabled" % now())
        
        #once the for loop completes, abort the simulation
        raise StopSimulation()
        
    
    
    
    @instance
    def show():
        
        #Return (to caller) when 'Reset' changes from high to low (active to inactive)
        yield reset.negedge
        
        print("\n(o1, o2, o3)\n")
        while True:
            print("Product, O, Kernel")
            #Removing this line creates a "forever-loop"
            yield clk.negedge

            #If I don't delay, then I lose data
            yield delay(1)
            
            print("Time elapsed %d nsec" % now())
            print("(%2d, %2d, %2d)" % (product[0], o1, kernel[0]))
            print("(%2d, %2d, %2d)" % (product[1], o2, kernel[1]))
            print("(%2d, %2d, %2d)" % (product[2], o3, kernel[2]))
            print("(%2d, %2d, %2d)" % (product[3], o4, kernel[3]))
            print("(%2d, %2d, %2d)" % (product[4], o5, kernel[4]))
            print("(%2d, %2d, %2d)" % (product[5], o6, kernel[5]))
            print("(%2d, %2d, %2d)" % (product[6], o7, kernel[6]))
            print("(%2d, %2d, %2d)" % (product[7], o8, kernel[7]))
            print("(%2d, %2d, %2d)" % (product[8], o9, kernel[8]))
            print("(%2d)" % (addition[7]))

            
    
    return instances()

inst= test()
inst.config_sim(trace=True)
inst.run_sim()