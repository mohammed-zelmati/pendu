import random
import os
import pygame
import unidecode

# Initialiser Pygame
pygame.init()
pygame.mixer.init()  # Initialiser le module de mixage audio

# Paramètres de la fenêtre
win = pygame.display.set_mode((1280, 720))
# Titre de la fenêtre :
pygame.display.set_caption("Jeu du Pendu")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
PINK = (255, 192, 203)

# Police
FONT = pygame.font.SysFont('Arial', 40)
SMALL_FONT = pygame.font.SysFont('Arial', 25)

# Charger les sons
win_sound_file = "win_sound.mp3"
lose_sound_file = "lose_sound.mp3"

# Charger les mots depuis le fichier
def load_words():
    with open("mots.txt", "r", encoding='utf-8') as file:
        words = [unidecode.unidecode(line.strip().upper()) for line in file.readlines()]
    return words

# Sauvegarder un score
def save_score(name, score):
    with open("scores.txt", "a", encoding='utf-8') as file:
        file.write(f"{name} {score}\n")

# Afficher les scores
def show_scores():
    win.fill(WHITE)
    y_offset = 50

    # Lire les scores à partir du fichier
    with open("scores.txt", "r", encoding='UTF-8') as file:
        scores = file.readlines()

    valid_scores = []
    for score in scores:
        parts = score.split()
        if len(parts) == 2:
            valid_scores.append((parts[0], int(parts[1])))

    # Trier les scores par ordre décroissant
    valid_scores = sorted(valid_scores, key=lambda x: x[1], reverse=True)

    # Afficher les en-têtes des colonnes
    header_name = SMALL_FONT.render("NOM", True, BLACK)
    header_score = SMALL_FONT.render("SCORE", True, BLACK)
    win.blit(header_name, (250, y_offset))
    win.blit(header_score, (600, y_offset))
    y_offset += 40

    # Afficher les scores dans le tableau
    for name, score_value in valid_scores[:5]:
        text_name = SMALL_FONT.render(name, True, BLACK)
        text_score = SMALL_FONT.render(str(score_value), True, BLACK)
        win.blit(text_name, (250, y_offset))
        win.blit(text_score, (600, y_offset))
        y_offset += 30
    
    pygame.display.update()
    pygame.time.wait(4000)  # Ajout d'un délai pour afficher les scores pendant 2 secondes

# Afficher le texte au centre
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, text_rect)

# Afficher le pendu en fonction des erreurs
def draw_hangman(errors, word):
    # Base
    if errors >= 1:
        pygame.draw.line(win, BLACK, (150, 550), (250, 550), 9)
        pygame.draw.line(win, BLACK, (200, 550), (200, 150), 9)
        pygame.draw.line(win, BLACK, (200, 150), (350, 150), 9)
        pygame.draw.line(win, BLACK, (350, 150), (350, 250), 9)

    # Corps :
    # Load the fresh face image
    image = pygame.image.load('image.jpg')
    # Redimensionnement de l'image
    small_image = pygame.transform.scale(image, (80, 72)) 
    # Replace head drawing with fresh face image
    if errors >= 2: win.blit(small_image, (308, 190))  # Adjust the coordinates as needed
    # if errors >= 2: pygame.draw.circle(win, RED, (350, 230), 30, 3)  # tête
    if errors >= 3: pygame.draw.line(win, BLACK, (350, 260), (350, 340), 3)  # tronc
    if errors >= 4: pygame.draw.line(win, BLACK, (350, 280), (310, 320), 3)  # bras gauche
    if errors >= 5: pygame.draw.line(win, BLACK, (350, 280), (390, 320), 3)  # bras droit
    if errors >= 6: pygame.draw.line(win, BLACK, (350, 340), (380, 400), 3)  # jambe droite
    if errors >= 7: 
        pygame.draw.line(win, BLACK, (350, 340), (320, 400), 3)  # jambe gauche
        # Afficher le mot complet en cas de perte
        text = FONT.render(f'Le mot était : {word}', True, BROWN)
        win.blit(text, (450, 600))

# Afficher les lettres ratées
def draw_missed_letters(missed_letters):
    text = SMALL_FONT.render("Lettres ratées: " + " ".join(missed_letters), True, RED)
    win.blit(text, (20, 600))

# Commencer une nouvelle partie
def start_game():
    words = load_words()
    word = random.choice(words)
    guessed = ['_'] * len(word)
    errors = 0
    guessed_letters = []
    missed_letters = []  # Ajouter cette ligne

    return word, guessed, errors, guessed_letters, missed_letters  # Ajouter missed_letters

# Fonction pour saisir le nom du joueur
def get_player_name():
    name = ""
    entering_name = True
    while entering_name:
        win.fill(WHITE)
        draw_text("Entrez votre nom:", FONT, BLACK, 1280 // 2, 150)
        draw_text(name, FONT, BLACK, 1280 // 2, 250)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return name

# Fonction pour saisir un nouveau mot
def add_new_word():
    new_word = ""
    adding_word = True
    while adding_word:
        win.fill(YELLOW)
        draw_text("Entrez un nouveau mot:", FONT, BLACK, 1280 // 2, 150)
        draw_text(new_word, FONT, BLACK, 1280 // 2, 250)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    adding_word = False
                elif event.key == pygame.K_BACKSPACE:
                    new_word = new_word[:-1]
                else:
                    new_word += event.unicode
    # Enregistrer le mot dans mots.txt
    with open("mots.txt", "a", encoding='utf-8') as file:
        file.write(unidecode.unidecode(new_word).upper() + "\n")

# Fonction principale du jeu
def game_loop(player_name):
    clock = pygame.time.Clock()
    word, guessed, errors, guessed_letters, missed_letters = start_game()  # Ajouter missed_letters

    # Boucle principale du jeu
    while True:
        win.fill(WHITE)
        draw_text('Pendu', FONT, BLACK, 1280 // 2, 50)
        draw_text(' '.join(guessed), FONT, BLACK, 1280 // 2, 350)  # décalé vers le bas
        draw_text(f'Joueur: {player_name}', SMALL_FONT, BLACK, 1280 // 2, 100)
        draw_hangman(errors, word)
        draw_missed_letters(missed_letters)  # Ajouter cet appel

        if errors >= 7:
            draw_text("Vous avez perdu !", FONT, RED, 1280 // 2, 450)
            pygame.display.update()
            pygame.mixer.music.load(lose_sound_file)
            pygame.mixer.music.play()
            save_score(player_name, 0)
            pygame.time.wait(4000)
            break

        if '_' not in guessed:
            draw_text("Vous avez gagné !", FONT, GREEN, 1280 // 2, 450)
            pygame.display.update()
            pygame.mixer.music.load(win_sound_file)
            pygame.mixer.music.play()
            score = len([char for char in guessed if char != '_'])
            save_score(player_name, score)
            pygame.time.wait(4000)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                letter = pygame.key.name(event.key)
                letter = unidecode.unidecode(letter).upper()
                # Fonction principale du jeu (suite)
                if letter.isalpha() and letter not in guessed_letters:
                    guessed_letters.append(letter)
                    if letter in word:
                        for i in range(len(word)):
                            if word[i] == letter:
                                guessed[i] = letter
                    else:
                        errors += 1
                        missed_letters.append(letter)  # Ajouter cette ligne

        pygame.display.update()
        clock.tick(10)

# Menu principal
def main():
    while True:
        win.fill(WHITE)
        draw_text("Menu du jeu", FONT, GREEN, 1280 // 2, 50)
        draw_text("Faites votre choix : entre 1 et 4 :", SMALL_FONT, RED, 1280 // 2, 100)
        draw_text("1. Jouer", SMALL_FONT, BLACK, 1280 // 2, 200)  # décalé vers le bas
        draw_text("2. Ajouter un mot", SMALL_FONT, BLACK, 1280 // 2, 250)
        draw_text("3. Scores", SMALL_FONT, BLACK, 1280 // 2, 300)
        draw_text("4. Quitter", SMALL_FONT, BLACK, 1280 // 2, 350)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_name = get_player_name()
                    game_loop(player_name)
                elif event.key == pygame.K_2:
                    add_new_word()
                elif event.key == pygame.K_3:
                    show_scores()
                    pygame.time.wait(4000)  # Afficher les scores pendant 2 secondes
                elif event.key == pygame.K_4:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    main()
