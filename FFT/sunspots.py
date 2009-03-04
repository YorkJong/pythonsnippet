#!/usr/bin/python
"""
This demonstration uses the FFT function to analyze the variations in
sunspot activity over the last 300 years.

Sunspot activity is cyclical, reaching a maximum about every 11 years. Let's
confirm that. Here is a plot of a quantity called the Wolfer number, which
measures both number and size of sunspots. Astronomers have tabulated this
number for almost 300 years.

Note:

This demonstration is original from both Anders Andreasen's and Mathworks' page.
I translated it into Python with matplotlib.

See also:

- "Python for scientific use, Part II: Data analysis" by Anders Andreasen
    <http://linuxgazette.net/115/andreasen.html>
- Using FFT in Matlab
    <http://www.mathworks.com/products/demos/shipping/matlab/sunspots.html>
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "December 2006"
__revision__ = "1.3"


import scipy.io.array_import
from pylab import *


figure(figsize=(13,4.5))

subplot(121)
sunspot = scipy.io.array_import.read_array('sunspots.dat')
year = sunspot[:,0]
wolfer = sunspot[:,1]
plot(year, wolfer, "r+-")
xlabel('Year')
ylabel('Wolfer number')
title('Sunspot data')

subplot(122)
Y = fft(wolfer)
plot(Y.real, Y.imag, "ro")
xlabel('Real Axis')
ylabel('Imaginary Axis')
title('Fourier Coefficients in the Complex Plane')
xlim(-4000, 2000)


figure(figsize=(13,4.5))

subplot(121)
N = len(Y)
power = abs(Y[:(N/2)])**2
Fs = 1.
nyquist = Fs/2
freq = linspace(0,1,N/2)*nyquist
plot(freq[1:], power[1:])
xlabel('Frequency (Cycles/Year)')
ylabel('Power')
title("Spectrum")
xlim(0, 0.20)

subplot(122)
period = 1./freq
plot(period[1:], power[1:])
index = find(power==max(power[1:]))
plot(period[index], power[index], 'ro')
text(float(period[index])+1, float(power[index])*.95,
                             'Period=%3.4f'%period[index])
xlabel('Period (Years/Cycle)')
ylabel('Power')
title("Periodogram")
xlim(0, 40)

show()
