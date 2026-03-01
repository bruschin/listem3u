# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
en essayant de se conformer à [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [README]

## [Unreleased]

### Ajouté

- Intégrer sur gitlab interne.
- Changelog.md
- Todo :
  - Revoir production wheel selon exemple Outil
  - Livrer fichier wheel sur nexus depuis gitlab
  - Soumettre à sonarqube Interne.
  - Gérer multi version python tests Unitaires avec Tox.
  - Revoir étapes de construction du docker. newenv trop long !

### Fixé

- Vérifier paramètre lancement -m sur clé USB. Codé à tester.
  
### Changé

- README.md

### Supprimé

- A remplir

## [2.0.1] - 2026-02-23

- Merge de la branche 23-préparation-v200 dans releases et de releases dans main
- création d'un Tag V2.0.1 et d'une release.
- Continuité développement sur la branche releases pour la version V2.0.2

## [2.0.0] - 2026-02-15

- Revue de code
- Création d'une nouvelle issue et d'une nouvelle branche = 23-préparation-v200
- Revue des réglages des Merge requests sur branche releases et main
- Revue du code pour développer la V2.0.0 et la merger dans releases et main
- Gestion du wiki et de la configuration de VSC.
- Todo. Régler le pipeline pour tests unitaires avec -eurs versions de python
- Prise en compte remarques SonarQube sur code if test => if [[]]
- Réglage Settings → Environments → github-pages → Selected branches and tags → Add deployment branch or tag rule
- Réglage pipeline github pour accepter push branche 23-préparation-v200 et merge-request

## 1.9.4 - 2025-12-12

- Mise au point
- Gestion pyenv et venv pour tests tox pytest pytest-cov python 3.10, 3.11, 3.12
- curl -fsSL <https://pyenv.run> | bash
- gestion .bashrc et .profile
- pyenv install -l
- pyenv install 3.10.19, puis pyenv install 3.11.14, puis pyenv install 3.12.12
- pyenv global 3.10 3.11 3.12
- pour la gestion de l'environnement virtuel
- apt install python3.12-venv
- python3 -m venv envdev
- gestion .bashrc et .profile
- lanceur_tox :
  - clean: OK (1.20=setup[1.13]-cmd[0.07] seconds)
  - lint: OK (2.53=setup[2.20]-cmd[0.33] seconds)
  - type: OK (2.57=setup[2.24]-cmd[0.32] seconds)
  - 3.10: OK (2.52=setup[2.21]-cmd[0.30] seconds)
  - 3.11: OK (2.69=setup[2.36]-cmd[0.33] seconds)
  - 3.12: OK (2.42=setup[2.10]-cmd[0.32] seconds)
- Test caractères accentués dans nom de fichier (Pb pour liste de lecture)
- remise à jour du pipeline ci/cd - github pages.
- Séparateur répertoire | fichier = \ et non plus /
- Generation possible d'une signature sha512 pour comparaison fichiers m3u
- Révision du pipeline github, des tests unitaires - couverture (pytest/tox)

## [1.9] - 2025-11-18

- Reprise du projet en novembre 2025 après 2 ans sans changement.
- Réactivation sonarcloud.io (le projet est en mode auto scan sonarqube)
- Python v 3.12
- Gestion version multiples
- Branche releases à merger dans main et création V1.9 à publier

## [1.8] - 2023-04-23

- Mise au point et tests du workflow en 5 fichiers yaml.
- Création d'une issue = plusieurs_yaml et d'une branche 19-plusieurs_yaml.
- Merge de la branche de développement dans releases avec suppression auto de
la branche 19. Merge à suivre dans Main selon règles.

## [1.7] - 2023-04-15

- Création branche releases - réglages configuration
- Création 3 issues mergées dans releases
- Activation workflow en 3 jobs avec un cache.

## 1.6.1 : 2023-04-13

- modification nom fichier .m3u

## [1.6] - 2023-04-12

- Modification contenus fichiers .m3u

## [1.5] - 2023-04-09

- modification contenus fichiers .m3u

## [1.4] - 2023-04-07

- introduction 1 parametre OBLIGATOIRE

## [1.3] - 2023-04-02

- issue 1-listemp3upy-sans-fichier-mp3

## 1.2 - 2023-03-28

- Debug repertoire travail PureWindowsPath

## 1.1 - 2023-03-26

- Filtre les fichiers mp3 listés.
- Pylint.
- Tests unitaires

## 1.0 - 2023-03-25

- Initialisation

[README]: README.md
[unreleased]: https://github.com/bruschin/listem3u
[2.0.1]: https://github.com/bruschin/listem3u/compare/V2.0.0...V2.0.1
[2.0.0]: https://github.com/bruschin/listem3u/compare/V1.9...V2.0.0
[1.9]: https://github.com/bruschin/listem3u/compare/V1.8...V1.9
[1.8]: https://github.com/bruschin/listem3u/compare/V1.7...V1.8
[1.7]: https://github.com/bruschin/listem3u/compare/V1.6...V1.7
[1.6]: https://github.com/bruschin/listem3u/compare/V1.5...V1.6
[1.5]: https://github.com/bruschin/listem3u/compare/V1.4...V1.5
[1.4]: https://github.com/bruschin/listem3u/compare/V1.3...V1.4
[1.3]: https://github.com/bruschin/listem3u/releases/tag/V1.3
