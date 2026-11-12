# VillageTech — landing page & portail d'accès bêta

Site statique (Astro) : landing page + formulaire de demande d'accès à la bêta gratuite.
Les demandes sont stockées dans Supabase (offre gratuite). Vous les validez à la main, puis activez le compte sur Higgsfield.

## Pages
- `/` — landing page
- `/acces` — portail d'accès (formulaire + bouton « Entrer dans le village » pour les comptes validés)
- `/confidentialite` — mentions RGPD (remplacer l'adresse de contact)

## Mise en route (≈10 min)
1. Créer un projet gratuit sur supabase.com.
2. SQL Editor → coller `supabase/beta_requests.sql` → Run.
3. Copier `.env.example` en `.env` et remplir l'URL et la clé `anon` (Project Settings → API), plus le lien de votre monde Higgsfield.
4. `npm install && npm run dev` → http://localhost:4321
5. Déployer gratuitement (Vercel, Netlify ou Cloudflare Pages) : build `npm run build`, dossier `dist`, et ajouter les 3 variables `PUBLIC_*` dans les réglages du site.

## Valider un bêta-testeur
Supabase → Table Editor → `beta_requests` (ou la vue `beta_a_traiter` pour celles en attente) :
1. Activer son compte sur Higgsfield avec `higgsfield_username`.
2. Passer `status` de `en_attente` à `valide` (`validated_at` se remplit tout seul).
3. Lui écrire à `email` pour lui dire que la porte est ouverte.

Le site public peut seulement *ajouter* une demande : personne ne peut lire la liste depuis le site.
Une même adresse email ne peut faire qu'une seule demande.
