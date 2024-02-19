import randomNoise as rN
import random
import sys

#random.seed(1234)

in_text = "abcd def ghi lmno"
error_rate = 0.1 # in [0,1]

args = sys.argv[1:]

if len(args) > 0:
    
    print(args)
    in_text, error_rate = args[0], float(args[1])

    
tc = rN.TransposeChars(in_text, error_rate)
sor = rN.SimulateOcrErrors(in_text, error_rate)
ot = rN.OcrTransposition(in_text, error_rate)

print(f"Original text = {in_text}.\nError rate = {error_rate}")
print(f"TransposeChars output = {tc}")     
print(f"SimulateOcrErrors output = {sor}")  
print(f"OcrTransposition output = {ot}")          

