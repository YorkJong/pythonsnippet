#!/usr/bin/python
"""
This example demonstrates the FFT of a simple sine wave and displays its
bilateral spectrum.  Since the frequency of the sine wave is folded by
whole number freqStep, the bilateral spectrum will display two non-zero point.

Note:

This example is coded original in Matlab from Roger Jang's
Audio Signal Processing page.  I translated it into Python with matplotlib.

See Also:

- "Discrete Fourier Transform" by Roger Jang
    <http://140.114.76.148/jang/books/audioSignalProcessing/ftDiscrete.asp>
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "December 2006"
__revision__ = "1.1"

from pylab import *


def fftshift(X):
    """Shift zero-frequency component to center of spectrum.

    Y = fftshift(X) rearranges the outputs of fft
    by moving the zero-frequency component to the center of the array.
    """
    Y = X.copy()
    Y[:N/2], Y[N/2:] = X[N/2:], X[:N/2]
    return Y


N = 256             # the number of points
Fs = 8000.          # the sampling rate
Ts = 1./Fs          # the sampling period
freqStep = Fs/N     # resolution of the frequency in frequency domain
f = 10*freqStep     # frequency of the sine wave; folded by integer freqStep
t = arange(N)*Ts    # x ticks in time domain, t = n*Ts
y = cos(2*pi*f*t)   # Signal to analyze
Y = fft(y)          # Spectrum
Y = fftshift(Y)     # middles the zero-point's axis

figure(figsize=(8,8))
subplots_adjust(hspace=.4)

# Plot time data
subplot(3,1,1)
plot(t, y, '.-')
grid("on")
xlabel('Time (seconds)')
ylabel('Amplitude')
title('Sinusoidal signals')
axis('tight')

freq = freqStep * arange(-N/2, N/2)  # x ticks in frequency domain

# Plot spectral magnitude
subplot(3,1,2)
plot(freq, abs(Y), '.-b')
grid("on")
xlabel('Frequency')
ylabel('Magnitude (Linear)')

# Plot phase
subplot(3,1,3)
plot(freq, angle(Y), '.-b')
grid("on")
xlabel('Frequency')
ylabel('Phase (Radian)')

show()
