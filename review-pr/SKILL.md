---
name: review-pr
description: Reviewer une pull request GitHub de bout en bout. Reconstitue la chaîne de la PR, vérifie que la CI a réellement tourné, lit le diff et cartographie les appelants, puis poste une review courte avec commentaires inline et suggestions. À utiliser quand l'utilisateur dit "review cette PR", "aide-moi à reviewer", ou donne une URL de pull request.
---

# Reviewer une pull request

Objectif : **faire gagner du temps au destinataire**, pas prouver qu'on a lu.
Une review utile affirme ce qu'elle a vérifié, pose deux ou trois questions que
le mainteneur seul peut trancher, et s'arrête.

Un repo peut avoir un skill qui étend celui-ci avec sa carte et ses
conventions. Lis-le d'abord s'il existe.

## Trois principes

Repris des skills publics de davd-gzl (<https://github.com/davd-gzl/skills>, MIT).

1. **Measure, never assume.** Une convention, une capacité, un compte viennent
   d'une commande lancée dans la session. Jamais de la mémoire, jamais d'un
   fichier qui l'a noté une fois. Si tu écris "le repo n'a pas de tests front",
   c'est que tu viens de lancer le `find`.
2. **Discipline de merge base.** Un problème qui se reproduit aussi sur la base
   n'est pas un finding de cette PR. Vérifie avant d'accuser le diff.
3. **Une affirmation porte la commande qui la prouve.** Numéros de ligne
   compris, relus sur la tête de la PR, pas sur la branche par défaut.

## Procédure

### 1. Reconstituer la chaîne

Une PR a souvent des ancêtres : une issue, une PR abandonnée, une PR recadrée.
**Le scope se juge contre ce que le mainteneur a demandé, pas dans l'absolu.**

```bash
gh pr view <PR> --json number,title,author,state,body,additions,deletions,changedFiles,baseRefName,headRefName
```

Suis les `#nnnn` cités dans le corps, et lis l'issue d'origine : elle dit ce que
l'utilisateur voulait, qui n'est pas toujours ce que la PR livre.

### 2. Isoler les commentaires humains

Les bots de review postent des pavés qui noient tout. Filtre-les.

```bash
for PR in <numéros>; do
  for EP in issues/$PR/comments pulls/$PR/comments pulls/$PR/reviews; do
    gh api repos/<owner>/<repo>/$EP --paginate \
      --jq '.[] | select(.user.login|test("bot|qodo|sonar|codecov";"i")|not)
            | "=== \(.user.login) \(.created_at // .submitted_at)\n\(.body)\n"'
  done
done
```

Le commentaire du mainteneur sur la PR précédente est souvent la clé du scope.

### 3. Vérifier que la CI a tourné

**Réflexe systématique, et souvent le point le plus rentable de la review.**

```bash
gh run list --branch <headRefName> --limit 10
```

`action_required` signifie que **rien n'a été testé** : sur une PR de fork,
GitHub attend qu'un mainteneur clique "Approve and run workflows". `gh pr checks
<PR>` peut afficher des checks verts et donner l'illusion inverse, parce que les
**apps GitHub** (Sonar, Snyk, GitGuardian, Codecov) tournent sans approbation.
Seuls les workflows du repo comptent.

Quand ils n'ont pas tourné, fais tourner la suite en local. C'est l'information
manquante la plus utile, et ça transforme un reproche en contribution. Prends
les commandes du repo, `Makefile`, `package.json` ou le workflow lui-même.

**Trois passes avant d'imputer un échec à la PR :**

1. La suite complète donne la liste des échecs.
2. **Rejoue-les en série**, sans parallélisme. Ce qui passe alors est un flake
   d'ordonnancement, pas un finding. Un worker qui tombe en produit plusieurs
   d'un coup.
3. **Rejoue le reste sur la merge base** (`git merge-base <base> <head>`). Ce
   qui échoue là aussi n'appartient pas à la branche. Recoupe avec
   `gh run list --branch <base> --limit 3` : si la base est verte en CI mais
   rouge chez toi, c'est ton environnement local.

Puis fais tourner spécifiquement les fichiers de tests que la PR touche.

Ce run local ne remplace pas la CI, qui fait aussi les lints et les images.
**N'affirme que ce que tu as lancé.**

### 4. Lire le diff en entier, puis cartographier

```bash
git fetch origin pull/<PR>/head:pr-<PR> && git checkout pr-<PR>
git diff --stat <base>...pr-<PR>
git diff <base>...pr-<PR> -- <fichiers source, sans les tests>
```

Puis, pour chaque fonction ou propriété que la PR introduit ou dont elle change
la sémantique : `grep -rn` sur tous ses appelants, **front compris**. Une PR qui
change ce que renvoie un champ d'API touche des écrans qu'elle ne modifie pas.

### 5. Écrire le tableau des vérifications avant la review

Une ligne par chose vérifiée, avec le `fichier:ligne` et le verdict. C'est ce
que la review affichera en premier. **Une vérification qui tient vaut autant
qu'un finding.**

### 6. Rédiger

Forme d'un finding : **le problème, son enjeu, la ligne où il vit, stop.** Pas
de justification étalée, pas de suggestion de redesign. Le destinataire qui n'a
rien demandé doit le lire une fois.

Écris dans la langue du repo.

**Maximum 4 findings.** Au-delà, tu transfères ta charge au mainteneur au lieu
de la lui retirer. Coupe les nits.

Un réflexe qui paie sur un repo multilingue : **rends les chaînes i18n
interpolées, dans les locales autres que l'anglais.** Une phrase qui se lit en
anglais peut être cassée ailleurs, quand le libellé injecté est un verbe là où
l'anglais a un groupe nominal. C'est un apport typique d'un relecteur non
anglophone.

### 7. Round suivant

Quand l'auteur pousse des correctifs, compare les patch-ids pour distinguer du
vrai code nouveau d'une branche qui a juste bougé sur sa base. **On ne re-reviewe
pas du code inchangé.**

```bash
git log --format='%H' <base>..pr-<PR> | xargs -n1 git show | git patch-id --stable
```

## Poster la review

Une review GitHub, c'est **un corps plus un tableau de commentaires inline, en
un seul appel**. Quatre commentaires postés séparément font quatre
notifications et arrivent en désordre.

```bash
gh api repos/<owner>/<repo>/pulls/<PR>/reviews --method POST --input payload.json
```

```json
{
  "event": "COMMENT",
  "body": "le corps",
  "comments": [
    {"path": "chemin/fichier.py", "line": 27, "side": "RIGHT", "body": "..."},
    {"path": "chemin/autre.py", "start_line": 259, "line": 265,
     "start_side": "RIGHT", "side": "RIGHT", "body": "..."}
  ]
}
```

Une suggestion est un bloc ` ```suggestion ` dans le `body` d'un commentaire.
Elle remplace **exactement** les lignes ancrées, indentation comprise.

**Contrainte qui décide de tout : on ne peut ancrer que sur des lignes présentes
dans le diff.** Le finding le plus actionnable porte souvent sur ce qui manque,
donc sur un fichier hors diff : il reste au corps. Vérifie avant de poster, un
seul ancrage invalide fait échouer tout l'appel.

```bash
gh api repos/<owner>/<repo>/pulls/<PR>/files --paginate > files.json
~/.claude/skills/review-pr/check-anchors.py files.json payload.json
```

Autres pièges :

- `line` est le numéro **côté droit**, après diff, au commit de tête.
- Multi-lignes : `start_line` **et** `line`, `start_side` **et** `side`.
- `event` : `COMMENT` pour un avis, `REQUEST_CHANGES` pour bloquer, `APPROVE`
  pour valider. Une seconde paire d'yeux non mainteneur poste `COMMENT`.
- **Omettre `event` crée la review en `PENDING`** : relisible dans le
  navigateur, puis soumise ou jetée. C'est le filet avant l'envoi.

**Ne poste jamais sans que l'utilisateur l'ait demandé dans le tour courant.**
Montre le corps et le JSON, attends le mot.

### Divulguer l'assistance IA

**Cherche la politique du repo avant de poster**, elle existe souvent.

```bash
grep -rn -i 'AI contributions\|AI-assisted\|generated with AI' README.md CONTRIBUTING.md .github/
```

Quand le repo demande de la transparence, une ligne suffit, à la fin du corps.
Elle doit faire trois choses et pas une de plus : **dire que c'est assisté par
IA, garder la propriété du côté de l'utilisateur, et donner au lecteur de quoi
vérifier.** C'est ce que la politique cherche, pas un badge.

> AI-assisted, per the README. I directed it and checked every claim before
> posting; the permalinks are pinned to `<sha>` so you can verify any of them.

Ce qu'il ne faut **pas** écrire : le nom de l'outil ou du skill. Ça ne dit rien
au mainteneur sur la manière de lire la review, et ça déplace la responsabilité
vers un outil alors que c'est l'utilisateur qui signe. La confiance vient des
commandes, des shas et des liens déjà dans la review, pas d'une mention.

Sans politique dans le repo, c'est l'appel de l'utilisateur, et sa règle par
défaut prime.

## Contrôle final

Dernière passe avant de montrer le JSON, sur l'artefact et pas de mémoire. Elle
ne juge pas le fond, déjà tranché : elle attrape ce qui rend une review
**périmée, illisible ou coûteuse**.

1. **Fraîcheur.** Le `headRefOid` est-il toujours celui que tu as lu ? La PR
   est-elle toujours ouverte, non draft, sans nouveau commentaire ni review
   depuis ta lecture ? Une review d'un arbre que personne ne lira est perdue.
   Relance juste avant de poster, pas au début.

   ```bash
   gh pr view <PR> --json headRefOid,state,isDraft,mergeable,updatedAt
   gh api 'repos/<owner>/<repo>/issues/<PR>/comments?since=<ta date de lecture>'
   ```

2. **Les ancrages disent ce que le commentaire prétend.** `check-anchors.py`
   vérifie que la ligne est dans un hunk, pas qu'elle porte le bon code.
   Imprime les lignes ancrées en face de la première phrase de chaque
   commentaire, et lis.

3. **Aucun déictique ambigu.** À un ancrage, le lecteur voit six lignes, pas le
   fichier. "le commentaire ci-dessous", "cette ligne", "plus haut" n'ont pas
   de référent si le bloc ancré contient déjà un commentaire. Nomme la ligne ou
   le symbole.

4. **Rien qui double un bot ou un fil résolu.** Quand ton finding prolonge le
   correctif d'un fil déjà résolu, dis-le et nomme le commit, sinon ça se lit
   comme une relance.

5. **Chaque finding nomme la décision qu'il demande.** Une question, un choix
   entre deux options, ou une suggestion cliquable. Un finding sans demande est
   du commentaire, et il coûte une lecture pour rien.

6. **Aucune consigne que le destinataire ne peut exécuter.** Approuver les
   workflows est le geste du mainteneur, pas de l'auteur. Énonce le fait,
   n'ordonne pas.

7. **Le partage corps / inline est bon.** Ce qui n'est pas ancrable va au
   corps, le reste en inline, rien n'apparaît deux fois.

8. **Chaque nombre et chaque sortie citée vient d'une commande de la session.**
   Numéros de ligne relus sur la tête de la PR, compteurs de tests pris du run,
   pas d'un souvenir.

9. **Les références portent un permalien, épinglé sur un sha.**

   ```
   https://github.com/<owner>/<repo>/blob/<sha>/<chemin>#L<n>
   https://github.com/<owner>/<repo>/blob/<sha>/<chemin>#L<a>-L<b>
   ```

   - **Épingle sur un sha, jamais sur une branche.** Un lien de branche suit la
     tête : le numéro de ligne dérive et finit par désigner autre chose. Un
     permalien sur sha est immuable, il ne peut pas pourrir. S'il devient
     historique après un force-push, c'est correct : il montre l'arbre que tu
     as reviewé.
   - **Le sha de tête pour le code de la branche, le sha de merge base pour ce
     qui n'est pas dans la PR** (une doc que la PR ne touche pas se cite sur la
     base, pas sur la branche).
   - **Le corps a besoin de liens, pas les commentaires inline.** Dans le
     corps, le lecteur n'est pas dans le fichier, et certaines références n'y
     sont même pas dans le diff. En inline il a le fichier sous les yeux : ne
     lie qu'une référence à un **autre** fichier, ou à une ligne hors du hunk
     affiché.
   - GitHub déplie un permalien de plage en extrait de code dans le
     commentaire, donc un lien y vaut une citation.
   - Laisse nus les shas et les `#1234` : ils sont autoliés.

## Ce qu'on ne soulève pas

- **Les perfs**, sauf si la PR touche un chemin chaud ou une requête. Un
  commentaire perf réflexe se voit.
- **La sécurité en mode "et si".** Énumère les chemins d'entrée, dis lesquels
  tiennent. Une liste vérifiée vaut dix questions ouvertes.
- **Ce que le repo ne fait pas.** Mesure avant de réclamer des tests dans une
  couche qui n'en a aucun.
- **Les nits de style** que le linter attrape déjà.
