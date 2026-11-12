# Prompts vidéo IA : le décollage du Village

Pour Higgsfield (ou Kling, Veo, Runway, Sora). Les prompts sont en anglais : les modèles vidéo les suivent mieux.
Format : 4:5 (1080×1350) pour le fil, 9:16 (1080×1920) pour Reels / Stories. Durée : 5 s par plan.

Astuce : joindre le logo V HD (`public/images/logo-512.png`) en image de référence pour la dérive de l'avion.

## Plan 1 : le décollage (5 s)

```
Cinematic aerial shot, photorealistic. A modern twin-turboprop regional airliner takes off from a small runway on a lush tropical island at golden hour. Glossy white fuselage with a smooth violet-to-pink gradient on the tail fin and engine nacelles, a large stylized blue "V" logo on the tail, the words "VILLAGE TECH" painted in violet along the fuselage, a row of passenger windows, propellers spinning with motion blur. The nose lifts, the wheels leave the ground, the aircraft climbs over palm trees toward a turquoise lagoon. Camera: low tracking shot alongside the runway, then rising with the plane. Warm sunlight, soft lens flare, light heat haze, sea spray in the air. Ultra detailed, realistic materials and reflections, smooth 24 fps motion, shot on a cinema camera, shallow depth of field.
```

## Plan 2 : le survol du lagon (5 s) — le plan de ta référence

```
Cinematic air-to-air shot, photorealistic. A modern twin-turboprop regional airliner in flight, banking gently above a breathtaking tropical lagoon. Glossy white fuselage, violet-to-pink gradient tail fin with a large blue "V" logo, "VILLAGE TECH" written in violet on the fuselage, propellers spinning with motion blur. Below: a volcanic island with dramatic green mountain peaks and rocky cliffs, a turquoise lagoon ringed by a coral reef with white surf, deep navy-blue ocean outside the reef, small sandy islets and a row of overwater bungalows. Camera: smooth air-to-air tracking from slightly above and in front of the left wing, slowly orbiting toward a side view. Bright midday sun, clear blue sky with a few soft white clouds, crisp atmosphere, realistic water caustics. Ultra detailed, realistic aircraft materials, stable cinematic motion, 24 fps.
```

## Plan 3 : l'avion s'éloigne vers le ciel (5 s) — pour enchaîner sur la fin

```
Cinematic aerial shot, photorealistic. The same white airliner with a violet-to-pink gradient tail and a blue "V" logo climbs away from a tropical island toward a sky that shifts from bright blue to a soft violet and pink sunset. The plane gets smaller as it flies into the light, leaving a faint vapor trail. Camera: static, slightly low angle, the island and lagoon at the bottom of the frame, a lot of open sky at the top for a title. Dreamy, joyful, cinematic, ultra detailed, smooth 24 fps.
```

## À ajouter à chaque prompt (prompt négatif / « à éviter »)

```
cartoon, low poly, toy plane, video game graphics, CGI look, distorted aircraft, extra wings, extra engines, melting shapes, warped text, misspelled text, real airline logos, watermark, logo of other brands, jittery camera, flicker, low resolution
```

## Conseils

- Si le texte « VILLAGE TECH » sort déformé (fréquent avec les modèles vidéo), enlève-le du prompt : le logo et les couleurs suffisent pour reconnaître l'avion, et on peut ajouter le texte au montage.
- Génère 3 ou 4 essais par plan et garde le plus stable.
- Pour un enchaînement propre, utilise la dernière image du plan 1 comme image de départ du plan 2 (image-to-video).
