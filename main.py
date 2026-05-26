import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def run_3d_universe():
    rng = np.random.default_rng(42)
    n = 3000
    r = rng.power(2.5, n) * 12
    theta = rng.uniform(0, 2*np.pi, n)
    phi = np.arccos(rng.uniform(-1, 1, n))
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi) * 0.4
    spiral = theta + r*0.6
    x += np.cos(spiral); y += np.sin(spiral)

    fig = plt.figure(figsize=(10,8), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    sc = ax.scatter(x, y, z, c=r, cmap='plasma', s=15, alpha=0.9)
    ax.set_title('3D Quantum Universe - 3000 Galaxies', color='white')
    ax.grid(False)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.fill = False

    def rotate(i):
        ax.view_init(elev=25, azim=i*0.5)
    ani = FuncAnimation(fig, rotate, frames=720, interval=30)
    plt.show()

def run_wave_packet():
    x = np.linspace(-10,10,500)
    sigma = 0.8
    psi = np.exp(-x**2/(2*sigma**2))
    plt.figure(facecolor='black')
    ax = plt.gca(); ax.set_facecolor('black')
    plt.plot(x, np.abs(psi)**2, color='#00e5ff', lw=3)
    plt.title('Schrödinger Wave Packet - Quantum Uncertainty', color='white')
    plt.xlabel('Position', color='white'); plt.ylabel('|ψ|²', color='white')
    plt.tick_params(colors='white')
    plt.show()

def run_inflation():
    t = np.linspace(0,10,500)
    a = np.exp(t); a[t>6] = a[300]* (t[t>6]/6)**0.5
    plt.figure(facecolor='black')
    ax = plt.gca(); ax.set_facecolor('black')
    plt.semilogy(t, a, color='#ff3d8a', lw=3)
    plt.title('Cosmic Inflation - Universe ka Expansion', color='white')
    plt.xlabel('Time', color='white'); plt.ylabel('Scale Factor', color='white')
    plt.tick_params(colors='white')
    plt.grid(alpha=0.2)
    plt.show()

def run_fluctuations():
    size=256
    rng = np.random.default_rng(0)
    k = np.fft.fftfreq(size)[:,None]**2 + np.fft.fftfreq(size)[None,:]**2
    k[0,0]=1e-6
    Pk = k**(-0.02)
    phase = rng.uniform(0,2*np.pi,(size,size))
    field = np.fft.ifft2(np.sqrt(Pk)*(np.cos(phase)+1j*np.sin(phase))).real
    plt.figure(facecolor='black')
    plt.imshow(field, cmap='inferno'); plt.axis('off')
    plt.title('Quantum Fluctuations → CMB Seed', color='white')
    plt.show()

print("=== Quantum Universe Simulator ===")
print("1. Schrödinger Wave Packet")
print("2. Cosmic Inflation")
print("3. Quantum Fluctuations")
print("4. 3D Quantum Universe")
choice = input("Choice [1-4]: ").strip()

if choice=='1': run_wave_packet()
elif choice=='2': run_inflation()
elif choice=='3': run_fluctuations()
else: run_3d_universe()