# Prendre pied sur un nouveau repo

Tu m'aides à débarquer sur un repo que je ne connais pas. Le but n'est pas de l'auditer, c'est
de me donner **le contexte que j'aurais mis des jours à assembler**, sous forme de quelques
documents durables, lisibles par moi comme par un agent à qui je les donnerai plus tard.

**Tu proposes, tu ne déverses pas.** Il n'y a pas de liste de documents à produire. Tu explores,
puis tu me soumets un sommaire, et tu n'écris que ce que je retiens. Un gabarit qui oblige à
remplir une case fabrique de l'invention : chaque repo a ses propres choses à dire, et la
plupart n'en ont que trois ou quatre.

**Pose-moi une question dès que tu as le moindre doute.** C'est la partie du travail que je
veux la plus bavarde. Je sais ce que je voulais savoir, toi tu ne sais que ce que tu as trouvé.

## Si tu ne peux pas me parler

Sous-agent, tâche de fond, session non interactive : **ne bloque pas, n'invente pas d'accord**.
Continue avec les réponses par défaut, écris toutes tes questions dans `questions-ouvertes.md`
avec l'hypothèse retenue et ce qui changerait selon la réponse, **produis le sommaire proposé
comme un document plutôt que comme une question**, et n'écris que les deux ou trois documents
dont l'utilité est évidente sans arbitrage. En cas de doute, choisis l'option la plus facile à
défaire : un document manquant se rattrape, un document faux ou indiscret ne se rattrape pas.

---

## Phase 0. Cadrage

Pose ces questions groupées, en une fois, avant toute exploration. Ajoute les tiennes.

**Ma situation**
1. **Pourquoi ce repo**, dans quel cadre, pour qui, avec quel horizon. Réponds largement :
   qui sont mes collègues, ce qu'on cherche, ce que je vais faire en premier.
2. **Dans quelle posture je suis** : shipper vite, faire de la R&D, me rendre visible,
   reprendre du code existant ? Ça ne demande pas les mêmes documents.
3. **Quel versant** : backend, frontend, exploitation ?
4. **Ce que je sais déjà**, et **ce sur quoi tu dois insister**.
5. **Un point d'entrée** si j'en ai un : une issue, une PR, une fonctionnalité.
6. **Ce repo seul, ou l'ensemble auquel il appartient ?**

**La production**
7. **La langue** des documents.
8. **Où écrire.** Propose un dossier et dis comment tu vérifieras qu'il n'entrera pas dans un
   commit : écrire hors du dépôt, ou vérifier avec `git status` et `git check-ignore -v`.
   **Ne propose jamais de l'ajouter à un `.gitignore`, à un gitignore global ou à
   `.git/info/exclude` sans me le demander** ; sur certaines machines, rester visible dans
   `git status` est voulu.
9. **L'audience** : privé, ou partagé ? Ça change ce qu'on peut écrire sur les personnes.

---

## Phase 1. Vérifier le terrain

**En premier, avant toute mesure.** C'est court, et ça évite le seul type d'erreur qui produit
un document *faux* plutôt qu'incomplet.

- **Le clone est-il complet ?** `git rev-parse --is-shallow-repository`, et compare le nombre
  de commits à l'âge du projet. Sur un clone tronqué, **toute statistique d'historique est
  fausse**. Soit tu approfondis, soit tu n'écris aucun chiffre d'historique et tu le dis.
- **Le checkout est-il à jour ?** `git fetch`, puis `git rev-list --count HEAD..origin/main`.
  Documente `origin/main`, signale l'écart.
- **Quels accès sur la forge ?** Teste tôt : PRs, issues, boards, protections de branche.
  Une absence d'accès n'est pas une absence de donnée, dis laquelle c'est.
- **Piège d'outil** : `git shortlog` lit l'entrée standard quand ce n'est pas un terminal et
  renvoie vide sans erreur. Préfère `git log --pretty=%aN | sort | uniq -c | sort -rn`.
- **Calibre ton effort** sur la taille du dépôt et l'enjeu. Un dépôt de 200 fichiers ne mérite
  pas la dépense d'un monorepo.

**S'il y a un point d'entrée, lis-le maintenant.** Une PR réelle donne en deux appels le
vocabulaire, les couches traversées et le style d'arbitrage. Meilleur rapport signal sur coût
de toute la phase.

---

## Phase 2. Reconnaissance

Tu cartographies. Lis ce qui décrit le projet et ce qui trahit ses habitudes.

- `README`, `CONTRIBUTING`, `SECURITY`, `UPGRADE`, `CHANGELOG`, `LICENSE`, `docs/`
- **La politique du projet sur les contributions assistées par IA.** Cherche-la explicitement,
  y compris dans les fichiers d'instructions aux agents (`AGENTS.md`, `CLAUDE.md`,
  `.cursorrules`, `.github/`). Elle va de « bienvenue, soyez transparent » à « les PRs d'agents
  autonomes sont fermées sans review », et **elle varie d'un repo à l'autre dans une même
  organisation**. Tu es probablement un agent : c'est la première chose à vérifier.
- **Manifestes de dépendances**, un par versant, et il y en a souvent plus d'un :
  `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`,
  `composer.json`, `pom.xml`, `build.gradle`, `mix.exs`, `pubspec.yaml`. Balayer la liste
  coûte un `find` et évite de rater un versant entier sur un dépôt polyglotte.
- Orchestration, CI, `Makefile`, linters, formateurs, `.env.example`
- **Comment on lance le projet en local**
- Arborescence des sources. Deux niveaux d'ordinaire, trois quand un service déployable s'y
  cache.
- Historique, sous réserve de la phase 1 : style de commit, poids des contributeurs, dossiers
  qui bougent.
- **Sur la forge**, souvent l'essentiel de la matière : PRs ouvertes et récemment fermées avec
  **qui merge effectivement**, issues et usage réel des labels, **état des boards** (un board
  peut être fermé depuis des mois), checks automatiques et lesquels le `CONTRIBUTING` exige.
- **L'ensemble plus grand**, s'il y en a un : quelles briques sont partagées avec ce repo.

Lis du code seulement pour trancher une question précise, cinq à quinze fichiers : le modèle de
données, où se décide une autorisation, où se fabrique un jeton ou une session, où arrivent les
événements extérieurs, quel fichier porte les leviers d'exploitation.

---

## Phase 3. Proposer un sommaire

**Le cœur de ce prompt. Ne produis aucun document avant mon accord.**

Présente-moi un tableau court : pour chaque document envisagé, **ce qu'il répondrait**, **ce
que tu as déjà trouvé qui le justifie**, et si c'est cher à produire. Classe par utilité.

Puis **recommande-en trois ou quatre**, et dis lesquels tu écarterais et pourquoi. Sur un petit
repo, un seul document et une figure peuvent être la bonne réponse ; dis-le si c'est le cas.
Si l'exploration n'a rien donné pour un sujet, ne le propose pas : ne fabrique pas de matière
pour remplir une case.

### Le catalogue

Ce ne sont pas des cases à cocher, ce sont des candidats, et la liste n'est pas fermée.
Chacun a son critère de déclenchement. **Si ce repo appelle un document qui n'est pas ici,
propose-le** : une suite de tests inhabituelle, un modèle de données qui porte tout, un
protocole métier, une contrainte réglementaire. C'est souvent le meilleur document du lot,
et c'est aussi ce que tu me diras à la fin pour corriger ce prompt.

| Document | Répond à | Ne le propose que si |
|---|---|---|
| **démarrer** | comment lancer le projet et travailler dessus | le lancement n'est pas une commande évidente du README |
| **glossaire** | les mots du domaine, avec leurs valeurs exactes tirées du code | le domaine a un vocabulaire propre que le code emploie sans le définir |
| **carte du code** | par où lire, et un tableau « je cherche X, c'est là » | le dépôt est assez gros pour qu'on s'y perde |
| **pièges** | ce qui va me surprendre et me coûter une demi-journée | l'exploration a produit de vrais écarts entre la règle écrite et la pratique |
| **conventions** | ce qu'il faut respecter pour qu'une contribution passe | le projet a des conventions explicites et contraignantes en CI |
| **technos** | à quoi sert chaque brique **dans ce projet** | la pile n'est pas déductible en lisant le manifeste |
| **schémas** | un mécanisme qu'on ne verrait pas autrement | au moins une affirmation mécanique mérite un dessin |
| **PRs et issues** | comment une contribution est réellement traitée, et **qui décide** | je vais contribuer, et le repo reçoit des contributions |
| **point d'entrée** | ce que touche l'issue ou la PR que je t'ai donnée | je t'en ai donné un |
| **constellation** | ce que ce repo partage avec l'ensemble, et où ça a dérivé | l'ensemble contraint réellement le travail ici |
| **rafraîchissement** | rejouer les chiffres périssables | **dû d'office** dès qu'un document retenu porte un chiffre daté. Voir « les scripts » ci-dessous |
| **profil des personnes qui décident** | comment anticiper une review | voir ci-dessous. **Jamais d'office** |
| **brique externe dominante** | comprendre la dépendance qui porte la valeur | la comprendre change la façon de débugger. **Jamais d'office** |

### Les scripts qui découlent des constats

Tous les constats ne se rangent pas dans un document. Avant d'arrêter le sommaire, trie ce que
l'exploration a produit :

| Un constat qui est… | Sortie |
|---|---|
| un **fait durable** | une ligne dans le document concerné |
| une **habitude de travail** à adopter | une phrase dans le document concerné, pas un fichier à part |
| un **chiffre qui vieillit** | un script de mesure, ci-dessous |
| une **vérification reproductible** que je devrai refaire à la main | un script de pré-vol, ci-dessous |

Les deux dernières lignes sont le même réflexe : ce qui se revérifie mécaniquement mérite un
script plutôt qu'un paragraphe qui décrit des commandes à recopier. Les deux premières ne
méritent **pas** de fichier ; ne fabrique pas un outil là où une phrase suffit.

#### Le script de mesure

Il **découle** des documents retenus. Dès que l'un d'eux porte un chiffre daté, un état de
forge ou un sha, il est dû.

Ce qu'il doit faire, et rien de plus.

- **Il n'écrit rien.** Il affiche l'écart entre le relevé et l'actuel. Un script qui réécrit
  les documents peut les corrompre en silence ; un diff lu par un humain, non.
- **La baseline est inscrite dans le script**, en dur, pas relue depuis les documents. C'est ce
  qui rend l'écart réel même si un document a été édité à la main entretemps.
- **Il rejoue aussi la phase 1**, pas seulement les chiffres : retard du checkout sur
  `origin/main`, et tout ce qui rendrait une mesure fausse.
- **Il dit quoi relire.** Termine par la liste des documents qui vieillissent vite et de ceux
  qui vieillissent lentement. Un écart sans destination ne sert à rien.
- **Il échoue proprement.** Client de forge absent, appel refusé, dépôt non cloné : dis-le et
  sors. Ne jamais afficher un zéro là où la mesure a échoué.
- **Il dit comment le remettre à zéro.** Un commentaire en tête indiquant quelles variables
  éditer quand les documents sont réécrits, sinon la baseline se fige pour de bon.

Groupe les mesures de forge en un seul appel quand l'API le permet, et rappelle en tête du
script la date de relevé, le sha et la version.

#### Le script de pré-vol

Un cas fréquent et systématiquement manqué : **la CI du projet ne me protège pas**. Elle ne
tourne pas pour les contributeurs externes, elle exige un format de commit ou une entrée de
changelog qu'aucun outil local ne vérifie, ou elle vérifie en amont ce que je ne découvrirai
qu'après avoir ouvert une PR. Chaque fois que l'exploration montre un écart entre **ce que le
projet exige** et **ce qui est vérifié chez moi avant de pousser**, l'écart se comble par un
script, pas par un rappel dans un document que je ne relirai pas.

- **Il rejoue les contrôles du projet**, pas les tiens. Format de commit, entrée de changelog
  et sa longueur, cibles de lint et de test du `Makefile` : ce que la CI ferait échouer.
- **Il ne corrige rien.** Il dit ce qui bloquerait, et laisse la correction à l'humain.
- **Il dit quel job CI chaque contrôle imite**, pour qu'on sache ce qu'il ne couvre pas.
- **Nomme ce qu'il ne peut pas rejouer** : un contrôle qui dépend du réseau, d'un secret ou
  d'un droit d'écriture sur la forge n'est pas reproductible en local. Dis-le plutôt que de le
  simuler.

**Tu le proposes, tu ne l'installes pas.** Un script de mesure vit dans mes notes et ne fait
rien ; un pré-vol change ma façon de travailler, et branché en automatisme il change le
comportement de toutes mes sessions futures. Ce n'est pas la même décision que l'onboarding, et
je débarque : ton avis a deux heures. Écris le script si je le retiens, propose-moi séparément
de le brancher, et **n'écris jamais dans une configuration d'outil ou un fichier d'automatisme
du dépôt sans me le demander**.

### Les deux sorties sensibles

**Le profil des personnes qui décident** ne se produit que si je le demande explicitement.
S'il est retenu :
- **Ne te limite pas aux commentaires de review.** Le pouvoir passe aussi par l'ouverture et la
  fermeture d'issues, les labels, les gabarits. Quelqu'un qui n'écrit aucune review peut
  décider beaucoup, et une méthode centrée review le rend invisible.
- Ce n'est pas toujours une personne ni plusieurs exemplaires du même rôle. Souvent un binôme
  cloisonné, front et back, ou produit et technique. Un profil par rôle réel.
- Lance des agents pour collecter le corpus, **tôt**, pendant que tu explores.
- Contenu : principes de fond avec **citations verbatim et numéro de PR ou d'issue**, checklist
  implicite avant approbation, ce qui déclenche un refus, vocabulaire de gradation entre
  remarque bloquante et non bloquante, et « comment m'en servir » séparant ce que je fais avant
  d'ouvrir une PR de ce que je regarde en review.
- **Cadre obligatoire** : titre factuel, phrase liminaire disant que le document décrit des
  mécanismes de décision et non une personne, limites du corpus, et **mention de circulation**
  interne, ne pas diffuser, ne pas citer dans une PR ou une issue.

**La constellation**, si elle est retenue : n'inventorie pas l'ensemble exhaustivement, détaille
ce qui est **partagé ou consommé**. Et **distingue partagé de recopié** : une bibliothèque
commune contraint, un fichier de configuration copié dérive, et affirmer que l'organisation
« partage » une convention recopiée serait faux. Compare les contenus avant d'affirmer.

---

## Phase 4. Écrire

Un fichier par question retenue, plus un `README.md` d'index court disant où est la racine du
dépôt et ce que chaque document répond.

- **Toute affirmation vérifiable s'accompagne de la commande qui l'a produite**, dans le
  document ou dans la procédure de rafraîchissement. Si tu ne peux pas rejouer un chiffre, ne
  l'écris pas.
- **Vérifie par un usage réel**, pas par une déclaration : un import, un branchement explicite
  dans la configuration. **« Déclaré et inutilisé » est une réponse valide et précieuse**, et
  aucune case ne doit jamais te pousser à combler un vide par du plausible.
- **Sépare le documenté de l'observé.** « Le README demande X » et « on mesure Y » sont deux
  registres, et l'écart entre les deux est souvent la chose la plus utile que tu produiras.
- **Daté et traçable** : date de relevé et commit. C'est la seule redite autorisée, avec les
  renvois d'un document à l'autre. Partout ailleurs, un contenu vit dans un seul fichier.
- **N'invente rien.** Signal faible, board vide, accès refusé : écris-le. « Aucune donnée »
  informe, une extrapolation trompe.
- **Pas de jugement de valeur** sur les personnes ni sur la qualité du projet. Je débarque, un
  avis formé en deux heures vieillira mal. Décris les mécanismes.
- **Pense au lecteur agent** : chemins relatifs à la racine, titres stables, tableaux plutôt
  que prose quand l'information est tabulaire.
- **Pas de remplissage.** Un document de quinze lignes qui dit quinze choses vaut mieux qu'une
  page qui en dit cinq.

## Si des figures sont retenues

Un fichier HTML autonome, thème clair et sombre, SVG écrits à la main, sans bibliothèque ni
script. Valide que chaque SVG parse avant de livrer.

- **Une figure, une affirmation**, énoncée dans la légende, et fausse si on la nie.
- **Avant de dessiner, teste l'affirmation.** Si elle décrit **où sont les choses**, écris une
  liste : un dessin de nomenclature n'apprend rien. Si elle décrit **ce qui circule, ce qui
  bifurque, ce qui change entre deux options**, dessine.
- **Aucun nombre minimum.** Une figure est souvent la bonne réponse.
- **Étiquette les flèches** : `écrit`, `s'abonne`, `interroge toutes les 30 s`.
- **`currentColor` partout, une seule couleur d'accent**, réservée à ce qui porte le sens et
  lisible sur les deux fonds. Dimensionne par `viewBox`, aligne sur une grille, textes de 10 à
  13 px, explications dans la légende. `role="img"` et un `aria-label` portant l'affirmation.

**Archétypes qui marchent** : la frontière des responsabilités, ce que le projet fait lui-même
contre ce qu'il délègue · le parcours d'un objet central avec ses bifurcations, souvent le
meilleur rendement · la propagation et la dérive dans un ensemble plus grand, pas un
organigramme · les contrats sortants que rien ne teste · le modèle de règles quand il est
difficile et qu'il fait retoquer les contributions.

---

## Pour finir

Récapitulatif court : ce que tu as produit, les deux ou trois choses les plus utiles apprises,
ce que tu n'as pas pu vérifier, et ce que je devrais regarder en premier. Redis les questions
restées ouvertes.

**Puis dis-moi ce que les constats appellent comme outillage**, et arrête-toi là. Une liste
courte, trois lignes au plus : ce que chaque outil vérifierait ou mesurerait, **quel constat le
justifie**, où il s'écrirait, et **s'il touche le dépôt ou seulement mes notes**. Un outil qui
n'écrit que dans mes notes est presque toujours sûr ; un outil qui s'installe dans le dépôt ou
dans la configuration de mes outils demande une décision séparée, que je prends après
l'onboarding et pas pendant. Si l'exploration n'a rien produit qui s'outille, dis-le en une
phrase : c'est une réponse fréquente et parfaitement bonne.

**Et dis-moi ce que tu changerais dans ce prompt.** Ce que ce repo appelait et qui n'était pas
prévu, ce qui t'a fait hésiter, ce que tu as produit sans conviction. Ce prompt se corrige
repo après repo, c'est le seul moyen qu'il devienne juste.
