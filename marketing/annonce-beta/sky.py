import sys, numpy as np
from PIL import Image, ImageFilter
out = sys.argv[1]
W, H = 5400, 1350
rng = np.random.default_rng(26)
y = np.linspace(0, 1, H)[:, None]; x = np.linspace(0, 1, W)[None, :]
X = x * W; Y = y * H

def lerp(a, b, t): return a + (b - a) * t
def ss(a, b, v): t = np.clip((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
def col(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float) / 255

# --- ciel : bleu roi → violet → rose → pêche à l'horizon ---
HOR = 1080
stops = [(0, '#2f3fd8'), (0.30, '#5a46e0'), (0.55, '#a35be0'), (0.74, '#ff7fbf'), (0.90, '#ffb49a'), (1.0, '#ffd9b0')]
v = np.clip(Y / HOR, 0, 1)
sky = np.zeros((H, W, 3))
for (a, ca), (b, cb) in zip(stops, stops[1:]):
    t = np.clip((v - a) / (b - a), 0, 1)
    m = (v >= a) & (v <= b)
    sky = np.where(m[..., None], lerp(col(ca), col(cb), t[..., None]), sky)
# variation horizontale : plus chaud vers le soleil (slide 5)
SX, SY = 4720, 1010
dist = np.sqrt(((X - SX) / 1.0) ** 2 + ((Y - SY) * 1.6) ** 2)
warm = np.exp(-dist / 1500)
sky = sky + warm[..., None] * (col('#ffc8a0') - sky) * 0.45
# halo du soleil
sky += (np.exp(-dist / 160) * 0.8 + np.exp(-dist / 520) * 0.3)[..., None] * col('#fff1d6')

# --- bruit fractal pour les nuages ---
def noise(scale_x, scale_y, oct=6, seed=0):
    r = np.random.default_rng(seed); acc = np.zeros((H, W)); amp = 1; tot = 0
    for o in range(oct):
        gw = max(2, int(W / scale_x * 2 ** o)); gh = max(2, int(H / scale_y * 2 ** o))
        g = Image.fromarray((r.random((gh, gw)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
        acc += np.asarray(g, float) / 255 * amp; tot += amp; amp *= 0.52
    return acc / tot

# couche de cumulus bas (devant l'horizon)
n1 = noise(700, 260, 6, 1)
band1 = ss(700, 960, Y) * (1 - ss(1075, 1100, Y))
c1 = ss(0.42, 0.62, n1 * 0.8 + band1 * 0.35 - (Y - 900) / 2600) * band1
# couche haute de cirrus étirés
n2 = noise(1400, 120, 5, 2)
band2 = ss(80, 260, Y) * (1 - ss(560, 760, Y))
c2 = ss(0.50, 0.75, n2) * band2 * 0.8
# nuages moyens épars
n3 = noise(500, 220, 6, 3)
band3 = ss(380, 560, Y) * (1 - ss(820, 920, Y))
c3 = ss(0.52, 0.72, n3) * band3 * 0.9

def shade(c, top, bot, ydir=0.7):
    # éclairage : haut des nuages clair, bas plus rosé
    g = np.gradient(np.asarray(Image.fromarray((c * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(float), axis=0)
    lit = np.clip(0.5 - g / 18, 0, 1)
    return lerp(col(bot), col(top), lit[..., None])
for c, top, bot in [(c2, '#ffe6f3', '#c99bf0'), (c3, '#fff2f6', '#e7a0d8'), (c1, '#fff6ec', '#f59ac4')]:
    cs = Image.fromarray((c * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)); c = np.asarray(cs, float) / 255
    sky = lerp(sky, shade(c, top, bot), c[..., None] * 0.92)
# les nuages près du soleil prennent sa lumière
sky += (c1 * np.exp(-dist / 700))[..., None] * col('#ffd8a0') * 0.5

# --- rayons de soleil ---
ang = np.arctan2(Y - SY, X - SX)
rays = (0.5 + 0.5 * np.sin(ang * 18 + np.sin(ang * 5) * 2)) ** 3
sky += (rays * np.exp(-dist / 1100) * ss(0, 400, SY - Y))[..., None] * col('#fff0dc') * 0.10

# --- la mer sous l'horizon ---
sea_t = np.clip((Y - HOR) / (H - HOR), 0, 1)
sea = lerp(col('#9a72e0'), col('#4a3fd4'), sea_t[..., None])
sea = lerp(sea, col('#ff9cc6'), (np.exp(-np.abs(X - SX) / 900) * (1 - sea_t) * 0.6)[..., None])
# reflets du soleil : vagues
wav = noise(60, 6, 4, 9)
glit = ss(0.62, 0.9, wav) * np.exp(-np.abs(X - SX) / (260 + sea_t * 500)) * (Y > HOR)
sea += glit[..., None] * col('#fff3dc') * 1.2
waves = (ss(0.55, 0.75, noise(300, 10, 4, 7)) * 0.12)[..., None]
sea = sea + waves * col('#ffffff')
img = np.where((Y > HOR)[..., None], sea, sky)
# ligne d'horizon douce + brume
img = lerp(img, col('#ffd2c0'), (np.exp(-np.abs(Y - HOR) / 14) * 0.6)[..., None])
# îles lointaines (silhouettes)
isl = np.zeros((H, W))
for cx, w, h in [(900, 380, 26), (1300, 160, 14), (2600, 520, 34), (3300, 200, 16), (4150, 260, 20)]:
    prof = h * np.clip(1 - ((X - cx) / w) ** 2, 0, 1) ** 0.6 * (0.8 + 0.4 * noise(80, 400, 3, cx)[0:1, :])
    isl = np.maximum(isl, ((Y < HOR) & (Y > HOR - prof)).astype(float))
img = lerp(img, col('#8a5fc8'), isl[..., None] * 0.85)
# vignette légère + grain
vig = 1 - 0.18 * (((X - W / 2) / (W / 2)) ** 2 * 0.2 + ((Y - H / 2) / (H / 2)) ** 2)
img = img * vig[..., None]
img += (rng.random((H, W)) - 0.5)[..., None] * 0.035
Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).save(out, quality=95)
print('ok')
