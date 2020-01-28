import numpy as np
import matplotlib.pyplot as plt

N = 128   # the sequence length
# Generate some random sequence we use for the convolution
x = abs(N*np.fft.ifft(np.random.randn(5)+1j*np.random.randn(5), N))
# use some exponential sequence for the second function
h = np.exp(-0.1*np.arange(N))
n = np.arange(N)
hx = np.fft.ifft(np.fft.fft(x[n]) * np.fft.fft(h[n]))
plt.plot(x, label='$x[n]$');
plt.plot(h, label='$h[n]$');
plt.plot(hx, label='$h[n]$');

plt.show()
