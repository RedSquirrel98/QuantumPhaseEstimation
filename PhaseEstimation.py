# This code implements the phase estimation algorithm using Pennylane in python. The goal of this circuit is to find the
#  eigenvalue of a certain operator of the form:
#[ [1, 0],[0, exp(i*phi)], where the eigenvalue that the circuit approximates is given by phi/2pi. This is a primitive demo
# that approximates the eigenvalue of 5/8 for the matrix [ [1, 0],[0, exp(i*5pi/4)]
# We implement this using a phase estimation circuit and the inverse quantum fourier transform.
#
#
import pennylane as qml
import numpy as np
import cmath
import math

pi=math.pi
binary=[]

def fractional_binary_to_float(s):
    t = s.split('.')
    return int(t[0], 2) + int(t[1], 2) / 2.**len(t[1])

def float_to_fractional_binary(x,max_bits=10):
    for i in range(max_bits+1):
        x= x*2
        if x>=1.0:
            binary.append(1)
            x=x-1.0
        elif x<1.0:
            binary.append(0)
        else:
            pass  

    s = [str(j) for j in binary]
    res = "".join(s)  
    binary_string= "0."+res   
    return binary_string

def result_to_eigenV(prob_dict,max_prob):
    for key, value in prob_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if value == max_prob:
            result=key.replace('b','.')
            print("Most probable result for eigenvalues is", fractional_binary_to_float(result))
    return



dev = qml.device("default.qubit", wires=4, shots=2000)
@qml.qnode(dev)


#######################################
#  circuit for 2c
######################################
def circuit2():
    # create input state of 1
    qml.PauliX(wires=3)
    # apply phase estimation circuit
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    qml.Hadamard(wires=2)

    qml.CRZ(5*pi/2, wires=[2,3])
    for i in range (2):    
        qml.CRZ(5*pi/2, wires=[1,3])   

    for i in range(4):
        qml.CRZ(5*pi/2, wires=[0,3])
# QFT-1
    qml.SWAP(wires=[0,2])
    qml.Hadamard(wires=2)
    qml.CRZ(pi/2,wires=[2,1]).inv()
    qml.CRZ(pi/4,wires=[2,0]).inv()
    qml.Hadamard(wires=1)
    qml.CRZ(pi/2,wires=[1,0]).inv()
    qml.Hadamard(wires=0)
    return qml.probs(wires=[0,1,2])
    
prob_list=circuit2()
print(circuit2.draw())
max_prob=max(prob_list)

# use a dict to store probabilities and corresponding binary state outputs
prob_dict={}
for i in range(len(prob_list)):
    bin_val = bin(i)
    prob_dict[bin(i)] = prob_list[i]

# call the function result_to_eigenV to get the eigenvalue corresponding to the state with highest probability
result_to_eigenV(prob_dict, max_prob)