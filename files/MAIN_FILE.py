#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import random

#low, high= 0, 1
inactive, active= 0, 1

from myhdl import *
from multiplier import multiplier_nbit
from adder_nbit import adder_nbit
from comparator import comparator_nbit
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
def test( matrix, rows, columns, stride ):
    
    #A. CONVOLUTION
    #INTIALIZATION
    #1.  Reset & Enable
    reset= ResetSignal(0, active= 1, isasync= True)
    enable= Signal(bool(0))
    
    #2. Generates the clock
    clk= Signal(bool(0))
    half_period= 150
    @always(delay( half_period ))
    def clk_driver():
        clk.next= not clk
      
    #3.a.Padding
    pad_rows= rows+ 2
    pad_columns= columns+2
    
    #3.b. creating a local padded matrix
    size_of_padded_matrix= pad_columns * pad_rows
    padded_matrix= [Signal(intbv(0)[4:0]) for i in range(size_of_padded_matrix)]
    
    #3.c intializing the local matrix
    for r in range(pad_rows):
        for c in range(pad_columns):
            if r < rows and c < columns:
                padded_matrix[r*pad_columns +c] = matrix[r*columns +c]
            elif r < rows and c >= columns:
                padded_matrix[r*pad_columns +c] = Signal(intbv(0)[4:0])
            elif r >= rows:
                padded_matrix[r*pad_columns +c] = Signal(intbv(0)[4:0])
    
    print("\nThe padded-matrix is")
    for r in range(0, pad_rows):
        for c in range( 0, pad_columns):
            print("%2d " % padded_matrix[r*pad_columns +c], end= "")
        print('\n')
    print("\n")
    

    #4. Ports [i.e., variables]
    #input
    i1, i2, i3, i4, i5, i6, i7, i8, i9=  [Signal(intbv(0)[4:])  for i in range(9)]
    #output
    o1, o2, o3, o4, o5, o6, o7, o8, o9=  [Signal(intbv(0)[4:])  for i in range(9)]
    #END of INTIALIZATION
    
    #5. Nine buffers
    b1= buffer(o1, i1, clk, enable, reset)
    b2= buffer(o2, i2, clk, enable, reset)
    b3= buffer(o3, i3, clk, enable, reset)
    b4= buffer(o4, i4, clk, enable, reset)
    b5= buffer(o5, i5, clk, enable, reset)
    b6= buffer(o6, i6, clk, enable, reset)
    b7= buffer(o7, i7, clk, enable, reset)
    b8= buffer(o8, i8, clk, enable, reset)
    b9= buffer(o9, i9, clk, enable, reset)
    
    #6. Defnition of Kernel
    kernel= [Signal(intbv(1)[4:]), Signal(intbv(5)[4:]), Signal(intbv(10)[4:]),             Signal(intbv(0)[4:]), Signal(intbv(1)[4:]), Signal(intbv(2)[4:]),                 Signal(intbv(3)[4:]), Signal(intbv(0)[4:]), Signal(intbv(1)[4:])]

    product= [Signal(intbv(0)[8:]), Signal(intbv(0)[8:]), Signal(intbv(0)[8:]),             Signal(intbv(0)[8:]), Signal(intbv(0)[8:]), Signal(intbv(0)[8:]),                 Signal(intbv(0)[8:]), Signal(intbv(0)[8:]), Signal(intbv(0)[8:])]

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
    
    
    #NEW
    #5.
    #creating a new matrix
    conv_matrix= [Signal(intbv(0)[16:0]) for i in range(rows * columns)]
    print("The convolution-matrix is empty.")
    for r in range(0, rows, stride):
        for c in range( 0, columns, stride):
            print("%d " % conv_matrix[r*columns +c], end= "")
    print("\n")
    print("-"*30)
    
    
    #6. Ports [i.e., variables]
    #input
    ip = Signal(intbv(0)[16:])
    #output
    op = Signal(intbv(0)[16:])
    #END of INTIALIZATION
    
    #One buffer
    bfr= buffer(op, ip, clk, enable, reset)
    #Ends here
    
    #New code
    #B. MAX. POOLING
    mp_rows= round(rows/2)
    mp_columns= round(columns/2)
    #1. Creates a local max_pool_matrix
    max_pool_matrix= [Signal(intbv(0)[17:0]) for i in range(mp_rows*mp_columns)]
    
    print("\nThe max-pool-matrix is empty.")
    for r in range(0, mp_rows):
        for c in range( 0, mp_columns):
            print("%2d " % max_pool_matrix[r*mp_columns +c], end= "")
        print('\n')
    print("\n")
    

    #2.a. 4 Ports, for selecting elements of a block
    #input
    inputs2= [Signal(intbv(0)[17:])  for i in range(4)]
    #output
    outputs2= [Signal(intbv(0)[17:])  for i in range(4)]
    #END of INTIALIZATION
    
    #2.b. Four buffers
    mp1= buffer(outputs2[0], inputs2[0], clk, enable, reset)
    mp2= buffer(outputs2[1], inputs2[1], clk, enable, reset)
    mp3= buffer(outputs2[2], inputs2[2], clk, enable, reset)
    mp4= buffer(outputs2[3], inputs2[3], clk, enable, reset)

    
    #3.a.
    representative = [Signal(intbv(0)[17:]) for i in range(3)]

    
    #3.b
    cmp1= comparator_nbit(representative[0], outputs2[0], outputs2[1])
    cmp2= comparator_nbit(representative[1], outputs2[2], outputs2[3])
    cmp3= comparator_nbit(representative[2], representative[0], representative[1])
    
    #4. Ports, to transfer result into a matrix
    #input
    ip2 = Signal(intbv(0)[17:])
    #output
    op2 = Signal(intbv(0)[17:])
    #END of INTIALIZATION
    
    #One buffer
    bfr2= buffer(op2, ip2, clk, enable, reset)
    #Ends here

    
    #Trigger: This hardware is triggered by the negative-edge of the clock-signal
    @instance
    def job_1():
        
        #In the first cycle, I want to "flush" (the contents of) the buffer
        reset.next= active
        print("Time elapsed %2d : Buffers have been reset" % now())
        
        yield clk.negedge
        
        #In the second cycle, I want to "enable" the buffer
        reset.next= inactive
        enable.next= active
        print("Time elapsed %2d : Buffers have been enabled" % now())
        print('-'*63)
        #print('-'*63)
        
        #In each cycle, 4 elements from the matrix are transferred into a buffer.
        count= 0
        stride= 1
        #Why have I written the following expression within "range()"? Because range() does not accept variable arguments
        for r in range( 0, pad_rows-2, stride):
            for c in range(0, pad_columns-2, stride ):

                i1.next= padded_matrix[r*pad_columns +c]
                i2.next= padded_matrix[r*pad_columns + (c+1)]
                i3.next= padded_matrix[r*pad_columns + (c+2)]
                
                i4.next= padded_matrix[(r+1)*pad_columns + c]
                i5.next= padded_matrix[(r+1)*pad_columns + (c+1)]
                i6.next= padded_matrix[(r+1)*pad_columns + (c+2)]
                
                i7.next= padded_matrix[(r+2)*pad_columns + c]
                i8.next= padded_matrix[(r+2)*pad_columns + (c+1)]
                i9.next= padded_matrix[(r+2)*pad_columns + (c+2)]
                
                #Return to the caller on the next trigger/cycle
                #Can I remove this yield? No.
                yield clk.negedge
                #This delay is necessary to load the correct values
                #Consequence of removing it: The first row is junk
                yield delay(1)                
                
                """
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
                """
                #New
                ip.next= addition[7]
                #The sum is being transffered to the port 'op'
                yield clk.negedge
                yield delay(1)
                
                conv_matrix[count].next= op
                count += 1
                
        
        #To update the last 'transfer', this instruction is necessary.
        yield clk.negedge
        
        #Disables the buffer
        enable.next= inactive
        
        #print('-'*63)
        #print('-'*63)
        print("Time elapsed %d nsec: Buffers have been disabled" % now())
        
        #This code DISPLAYs the output        
        print("-"*30)
        print("The convolution-matrix is")
        for r in range(0, rows, stride):
            for c in range( 0, columns, stride):
                print("%3d " % conv_matrix[r*columns +c], end= "")
            print('\n')
        print("\n")
        
        #raise StopSimulation()
        
    #return instances()
    
        reset.next= active
        print("Time elapsed %2d : Buffers have been reset" % now())
        
        yield clk.negedge
        
        reset.next= inactive
        enable.next= active
        print("Time elapsed %2d : Buffers have been enabled" % now())
        print('-'*63)
        print('-'*63)
        
        
        #In each cycle, 4 elements from the matrix are transferred into a buffer.
        count= 0
        stride= 2
        for r in range( 0, rows, stride):
            for c in range( 0, columns, stride):

                inputs2[0].next= conv_matrix[r*columns +c]
                inputs2[1].next= conv_matrix[r*columns + (c+1)]
                
                inputs2[2].next= conv_matrix[(r+1)*columns + c]
                inputs2[3].next= conv_matrix[(r+1)*columns + (c+1)]
                
                yield clk.negedge
                yield delay(1)
                
                
                print("Time elapsed %d nsec" % now())

                  
                ip2.next= representative[2]
                yield clk.negedge
                yield delay(1)
                
                max_pool_matrix[count].next= op2
                count += 1
                #yield delay(1)
        
        #To update the last 'transfer', this instruction is necessary.
        yield clk.negedge
        
        #Disables the buffer
        enable.next= inactive
        
        print('-'*63)
        print('-'*63)
        print("Time elapsed %d nsec: Buffers have been disabled" % now())
        
        #This code DISPLAYs the output        
        print("-"*63)
        print("The max_pool_matrix is")
        for r in range(0, mp_rows):
            for c in range( 0, mp_columns):
                print("%3d " % max_pool_matrix[r*mp_columns +c], end= "")
            print('\n')
        print("\n")        
    
        #once the for loop completes, abort the simulation
        raise StopSimulation()
    return instances()


# In[ ]:


#Input the matrix here
rows, columns= 4, 6
MATRIX= [Signal(intbv(random.randrange(8))[4:0]) for i in range(rows*columns)]
#MATRIX= [Signal(intbv(-2)[4:0]) for i in range(rows*columns)]
stride= 1

print("The matrix is")
for r in range(0, rows, stride):
    for c in range( 0, columns, stride):
        print("%2d " % MATRIX[r*columns +c], end= "")
    print('\n')
print("\n")

#Runs the simulation
inst= test(MATRIX, rows, columns, stride)
inst.config_sim(trace= True)
inst.run_sim()

