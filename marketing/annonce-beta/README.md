# Kit d'annonce de la bêta

Teaser vidéo (24 s) + carrousel Instagram (5 images) + image Story, dans la DA « golden hour » du Village Tech : ciel bleu roi, violet et rose, accents manuscrits.

| Fichier | Rôle |
|---|---|
| `comp.html` | Le teaser : 7 scènes animées, pilotées image par image par `seek(t)` |
| `posters.html` | Les slides 1, 2, 5 du carrousel et l'image Story (`?a=a1`, `a2`, `a5`, `a6`) |
| `music.py` | La bande-son, synthétisée (aucun fichier audio externe, donc aucun souci de droits) |
| `render.cjs` | Rend le teaser en MP4 4:5 avec la bande-son |
| `stills.cjs` | Rend les images du carrousel (les slides 3 et 4 sont des images du teaser) |

## Refaire le rendu

Depuis ce dossier, avec Node, Python 3 (numpy), ffmpeg et Playwright :

```sh
mkdir -p a out/carrousel
cp ../../public/images/{sunset,hero,poste,reunion,academie,amphi,marche,collegues,rencontre,vpro,enzo}.webp \
   ../../public/images/logo-v.svg ../../public/images/logo-512.png a/
npm i @fontsource/plus-jakarta-sans@5.0.20 @fontsource/space-grotesk@5.0.18 @fontsource/jetbrains-mono@5.0.20 @fontsource/kaushan-script@5.0.12
cp node_modules/@fontsource/plus-jakarta-sans/files/plus-jakarta-sans-latin-{700,800}-normal.woff2 \
   node_modules/@fontsource/space-grotesk/files/space-grotesk-latin-{500,600}-normal.woff2 \
   node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-600-normal.woff2 \
   node_modules/@fontsource/kaushan-script/files/kaushan-script-latin-400-normal.woff2 a/
python3 music.py out/music.wav
node render.cjs "$PWD" "$PWD/out/teaser-4x5.mp4"
node stills.cjs "$PWD"
```

Version 9:16 (Reels / Stories) à partir du 4:5 :

```sh
ffmpeg -i out/teaser-4x5.mp4 -filter_complex "[0:v]split[a][b];[a]scale=1536:1920,boxblur=40:2,eq=brightness=-0.05:saturation=1.3,crop=1080:1920[bg];[bg][b]overlay=0:285[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy out/teaser-9x16.mp4
```

Pour changer un texte : modifier `comp.html` (titres des scènes, liste `LIEUX`) ou `posters.html`, puis relancer le rendu.

## Teaser « Viens chercher ton billet » (v2, 19,5 s)

L'intro (hyperespace, logo, « La bêta est lancée ! ») puis une carte d'embarquement qui se remplit
comme la carte de l'entrepreneur, le tampon « Place confirmée », le tableau des départs
« Dernier appel pour le Village ! » et la fin « Viens chercher ton billet ! ».

```sh
python3 music2.py out/music2.wav
node render2.cjs "$PWD" "$PWD/out/billet-4x5.mp4"
```

Pour changer les infos du billet : attributs `data-f` (texte) et `data-t` (moment d'apparition) dans `billet.html`.
