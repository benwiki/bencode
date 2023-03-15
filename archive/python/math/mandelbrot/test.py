from os import path
import re
raw = lambda string: repr(string)[1:-1]
p = "G:\My Drive\PROGRAMMING\CUccom\Python\Mandelbrot\noutput2.jpeg"

print(raw(p), path.exists(raw(p)))
print(re.search("([\w\s\:\\\/]+)[\\\/]+\w+\.\w+", raw(p))[1].strip())
print(re.search("\w+\.(jpe?g|png|gif)", raw(p))[0].strip())

print(str(hex(10//16)))
print((10+10j)*(0.1+0.1j))