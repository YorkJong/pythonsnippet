#!/usr/bin/python
"""
A common use of Fourier transforms is to find the frequency components of a
signal buried in a noisy time domain signal. Consider data sampled at 1000 Hz.
Form a signal containing a 50 Hz sinusoid of amplitude 0.7 and 120 Hz sinusoid
of amplitude 1 and corrupt it with some zero-mean random noise:

Note:

This example is original from Matlab Funcion Reference.
I translated it into Python with matplotlib.

See Also:

- Matlab function reference of FFT
    <http://www.mathworks.com/access/helpdesk/help/techdoc/ref/fft.html>
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "December 2006"
__revision__ = "1.1"

from pylab import *

def nextpow2(A):
    return int(ceil(log2(A)))


Fs = 1000.          # Sampling frequency
Ts = 1/Fs           # Sample period
N = 1000            # Length of signal
t = arange(N)*Ts    # Time vector

# Sum of a 50 Hz sinusoid and a 120 Hz sinusoid
x = 0.7*sin(2*pi*50*t) + sin(2*pi*120*t)
y = x + 2*randn(size(t))     # Sinusoids plus noise

figure(figsize=(7,8), frameon=False)
subplots_adjust(hspace=.4)

subplot(211)
plot(1000*t[:50], y[:50])
title('Signal Corrupted with Zero-Mean Random Noise')
xlabel('Time, t (ms)')
ylabel('Amplitude, y(t)')

NFFT = 2**nextpow2(N)  # Next power of 2 from length of y
Y = fft(y, NFFT)/N
f = Fs/2 * linspace(0, 1, NFFT/2)

subplot(212)
plot(f, 2*abs(Y[:NFFT/2]))  # Plot single-sided amplitude spectrum.
title('Single-Sided Amplitude Spectrum of y(t)')
xlabel('Frequency, f (Hz)')
ylabel('Magnitude, |Y(f)|')

show()
