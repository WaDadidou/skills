---
name: onboard-repo
description: Se constituer le contexte d'un repo inconnu. Pose des questions de cadrage, explore, propose un sommaire de documents adapté à CE repo, puis n'écrit que ce qui est retenu. À utiliser quand l'utilisateur débarque sur un projet qu'il ne connaît pas, ou dit "onboard", "état des lieux", "je débarque sur ce repo", "prends connaissance du repo".
---

# Prendre pied sur un nouveau repo

Suis intégralement `PROMPT.md`, dans ce même dossier. Lis-le maintenant, avant toute action.

```
Read ~/.claude/skills/onboard-repo/PROMPT.md
```

Cinq points que la fatigue fait sauter en premier.

1. **Tu proposes, tu ne déverses pas.** Il n'y a pas de liste de documents à produire. La
   phase 3 est le cœur : tu explores, tu soumets un sommaire adapté à ce repo, et **tu
   n'écris rien avant l'accord**. Trois ou quatre documents suffisent presque toujours. Sur un
   petit repo, un seul document et une figure sont la bonne réponse.

2. **Vérifie le terrain avant de mesurer.** Clone superficiel, checkout périmé, accès refusé
   sur la forge : ce sont les seules erreurs qui produisent un document *faux* et non
   simplement incomplet. Un `git shortlog` sur un clone tronqué invente un contributeur
   dominant.

3. **La phase 0 est bavarde et bloquante quand tu peux parler.** Quand tu ne peux pas, applique
   le repli du prompt : continue, consigne les questions, écris le sommaire au lieu de le
   demander, et ne produis aucune des deux sorties sensibles (profil des personnes qui
   décident, brique externe dominante).

4. **Cherche la politique du projet sur les contributions IA.** Elle varie d'un repo à l'autre
   dans une même organisation, de « bienvenue » à « fermée sans review ». Tu es probablement un
   agent.

5. **Un constat qui se revérifie mérite un script ; un script qui agit ne s'installe pas tout
   seul.** Chiffres périssables et contrôles que la CI du projet ne rejoue pas chez moi appellent
   un exécutable plutôt qu'un paragraphe. Mais tu le **proposes** : n'écris jamais dans une
   configuration d'outil, un fichier d'automatisme ou un hook du dépôt sans accord explicite.

Ce prompt est aussi conçu pour être copié tel quel dans un autre agent. Si l'utilisateur le
demande, donne-lui le contenu de `PROMPT.md` sans le paraphraser.
