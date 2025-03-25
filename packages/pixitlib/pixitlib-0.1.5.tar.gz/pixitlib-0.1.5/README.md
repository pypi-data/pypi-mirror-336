# PixitLib

PixitLib est une librairie Python permettant de gérer la connexion et la communication avec une matrice LED et une console de jeu.

## Installation

Vous pouvez installer PixitLib directement depuis PyPI :
```bash
pip install pixitlib
```

Ou depuis GitHub :
```bash
pip install git+https://github.com/TonGithub/pixitlib.git
```

## Utilisation

### Importation de la librairie

```python
from pixitlib import GameConnexion
```

### Création d'une connexion

```python
game = GameConnexion()
game.connect()
```

### Envoi d'une trame à la matrice LED

Vous pouvez envoyer une trame personnalisée à la matrice LED :

```python
frame = ";".join(["(255,0,0)"] * 128 + ["(0,0,255)"] * 128)  # Rouge et bleu
game.send_frame(frame)
```

### Réception des commandes de la console

```python
game.listen_commands()
```

### Fermeture de la connexion

```python
game.close()
```

## Configuration

Par défaut, `pixitlib` utilise les valeurs suivantes :
- **Adresse IP** : `127.0.0.1`
- **Port Console** : `58591`
- **Port Matrice LED** : `58600`

Vous pouvez modifier ces paramètres lors de l'initialisation :

```python
game = GameConnexion(host="192.168.1.10", console_port=12345, matrix_port=54321)
```

## Développement

Si vous souhaitez contribuer au projet, clonez le dépôt et installez la version locale :
```bash
git clone https://github.com/TonGithub/pixitlib.git
cd pixitlib
pip install -e .
```

## 📝 Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser et de le modifier selon vos besoins.

