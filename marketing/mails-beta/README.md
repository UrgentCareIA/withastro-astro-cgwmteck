# Mails de la bêta

Quatre mails aux couleurs du Village, en HTML compatible avec les clients mail (tableaux, styles en ligne).

| Fichier | Quand l'envoyer | Objet |
|---|---|---|
| `1-place-reservee.html` | Juste après l'inscription (J0) | Ta place pour le Village est réservée ✈ |
| `2-dans-les-coulisses.html` | J+2, si le compte n'est pas encore validé | Pendant que tu attends : un tour en coulisses |
| `3-la-porte-est-ouverte.html` | Dès que tu passes le statut à `valide` | {{PRENOM}}, la porte du Village est ouverte 🎉 |
| `4-demande-non-retenue.html` | Si tu passes le statut à `refuse` | Ta demande d'accès au Village Tech |

## Variables à remplacer

- `{{PRENOM}}`, `{{NOM}}`, `{{PSEUDO_HIGGSFIELD}}` : colonnes `first_name`, `last_name`, `higgsfield_username` de Supabase
- `{{SITE_URL}}` : l'adresse du site en ligne (ex. `https://levillagetech.fr`), sans `/` à la fin
- `{{HIGGSFIELD_URL}}` : le lien vers votre monde sur Higgsfield

## Comment les envoyer

- **À la main au début** : ouvre le fichier dans un navigateur, copie le rendu dans ton mail (Gmail accepte le copier-coller), remplace les variables.
- **Automatiquement ensuite** : avec un service comme Brevo ou Resend (gratuits pour quelques centaines de mails par mois), en collant le HTML comme modèle. L'envoi peut être déclenché par Supabase quand le statut change.

Les images (`logo.png`, `hydravion.jpg`) sont chargées depuis le site : elles ne s'affichent qu'une fois le site en ligne.
