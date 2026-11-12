import numpy as np, wave, sys
SR = 48000; DUR = 19.5
N = int(SR * DUR); t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR); j = min(N, i + len(sig)); s = sig[: j - i] * gain
    L[i:j] += s * (1 - max(0, pan)); R[i:j] += s * (1 + min(0, pan))

def env(n, a, d):  # attaque / décroissance exponentielle
    x = np.arange(n) / SR
    return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / d)

def lp(x, k):  # passe-bas simple (moyenne glissante)
    if k <= 1: return x
    c = np.cumsum(np.insert(x, 0, 0)); y = (c[k:] - c[:-k]) / k
    return np.concatenate([y, np.zeros(k - 1)])

# --- nappe : ré mineur, saws filtrés + sous-basse ---
def pad(freqs, start, end, gain):
    n = int((end - start) * SR); x = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-0.25, 0.25):
            ph = (f + det) * x
            s += 2 * (ph - np.floor(ph + 0.5))
    s = lp(s, 90) / len(freqs)
    fade = np.minimum(1, x / 1.2) * np.minimum(1, (end - start - x) / 0.6)
    add(s * fade, start, gain)

# --- montée (riser) ---
def riser(start, dur, gain, f0=180, f1=2400):
    n = int(dur * SR); x = np.arange(n) / SR; k = x / dur
    noise = rng.standard_normal(n); noise = noise - lp(noise, int(40 - 36 * k.mean()))
    f = f0 * (f1 / f0) ** k; ph = 2 * np.pi * np.cumsum(f) / SR
    s = (0.6 * noise * k ** 2 + 0.5 * np.sin(ph) * k) * k
    add(s, start, gain)

# --- impacts ---
def boom(start, gain=1.0, f0=70, f1=32, d=1.4):
    n = int(2.5 * SR); x = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-x * 6); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env(n, 0.002, d)
    nz = rng.standard_normal(n) * env(n, 0.001, 0.08); nz = lp(nz, 6)
    add(np.tanh((s + 0.5 * nz) * 1.6), start, gain)
def kick(start, gain=0.7):
    n = int(0.5 * SR); x = np.arange(n) / SR
    f = 45 + 120 * np.exp(-x * 30); ph = 2 * np.pi * np.cumsum(f) / SR
    click = rng.standard_normal(n) * env(n, 0.0005, 0.006)
    add(np.sin(ph) * env(n, 0.001, 0.18) + 0.3 * click, start, gain)
def hat(start, gain=0.12):
    n = int(0.12 * SR); s = rng.standard_normal(n); s = s - lp(s, 3)
    add(s * env(n, 0.0005, 0.03), start, gain, pan=0.3)
def whoosh(start, dur=0.45, gain=0.25):
    n = int(dur * SR); x = np.arange(n) / SR
    s = rng.standard_normal(n); s = lp(s, 12) * np.sin(np.pi * x / dur) ** 2
    add(s, start, gain, pan=-0.2)
def tick(start, gain=0.08):
    n = int(0.03 * SR); x = np.arange(n) / SR
    add(np.sign(np.sin(2 * np.pi * 2200 * x)) * env(n, 0.0005, 0.008), start, gain, pan=0.4)
def bell(start, f, gain=0.18, d=1.2):
    n = int(2.5 * SR); x = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * f * 2.01 * x) + 0.15 * np.sin(2 * np.pi * f * 3.98 * x)) * env(n, 0.003, d)
    add(s, start, gain, pan=0.15)


pad([73.42, 110.0, 146.83, 174.61], 0.0, 12.65, 0.16)
pad([58.27, 87.31, 116.54, 174.61], 12.6, 15.45, 0.16)
pad([73.42, 110.0, 146.83, 220.0, 293.66], 15.4, 19.5, 0.18)
add(np.sin(2 * np.pi * 36.7 * t[: int(19.0 * SR)]) * np.minimum(1, t[: int(19.0 * SR)] / 2) * 0.18, 0.0)
riser(0.15, 1.8, 0.35)
riser(8.9, 0.7, 0.28, 300, 3200)
riser(14.8, 0.6, 0.25, 300, 2600)
boom(1.95, 1.0)
kick(2.3, 0.7); kick(2.75, 0.8)
whoosh(4.45, 0.5, 0.3); boom(4.6, 0.6, 60, 32, 0.9); kick(4.85, 0.6)
for k in range(10):
    tt = 5.0 + k * 0.45
    kick(tt, 0.35); hat(tt + 0.225, 0.07)
fills = [(5.5, 3), (5.8, 3), (6.6, 13), (7.1, 11), (7.5, 11), (7.9, 9), (8.25, 4), (8.55, 7), (8.8, 2), (8.95, 7), (9.1, 10)]
for t0, n in fills:
    for i in range(n):
        tick(t0 + 0.45 * (0.35 + 0.65 * i / max(1, n - 1)), 0.06)
    bell(t0 + 0.45, 1318.5, 0.05, 0.4)
whoosh(5.85, 1.2, 0.18)
boom(9.6, 1.0, 80, 35, 1.2); kick(9.6, 0.9)
for i, f in enumerate([523.25, 659.25, 783.99, 1046.5, 1318.5]): bell(9.75 + i * 0.07, f, 0.12, 1.5)
for k in range(10): tick(10.35 + k * 0.05, 0.05)
boom(12.58, 0.8, 60, 30, 1.0)
for k in range(30): tick(12.85 + k * 0.03, 0.07)
bell(14.0, 659.25, 0.16, 1.2); bell(14.25, 523.25, 0.16, 1.4)
boom(15.38, 1.0, 65, 28, 2.4)
for i, f in enumerate([293.66, 440, 587.33, 880]): bell(15.45 + i * 0.12, f, 0.11, 2.2)

mix = np.stack([L, R], 1)
mix = mix - lp(mix[:, 0], 1)[:, None] * 0  # pas de DC
peak = np.max(np.abs(mix)); mix = np.tanh(mix / peak * 1.4) * 0.89
fade = np.minimum(1, (DUR - t) / 1.2)[:, None]; mix *= fade
pcm = (mix * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', mix.shape)
