import random
import os
import pygame

# Initialiser Pygame
pygame.init()
pygame.mixer.init()  # Initialiser le module de mixage audio

# Paramètres de la fenêtre
SCREEN_WIDTH = 1280  # Augmenté pour plus d'espace
SCREEN_HEIGHT = 720
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu du Pendu")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Police
FONT = pygame.font.SysFont('Arial', 40)
SMALL_FONT = pygame.font.SysFont('Arial', 25)

# Charger les sons
win_sound_file = "win_sound.mp3"
lose_sound_file = "lose_sound.mp3"

# Charger les mots depuis le fichier
def load_words():
    with open("mots.txt", "r") as file:
        words = [line.strip() for line in file.readlines()]
    return words

# Sauvegarder un score
def save_score(name, score):
    with open("scores.txt", "a") as file:
        file.write(f"{name} {score}\n")

# Afficher les scores
def show_scores():
    win.fill(WHITE)
    y_offset = 50
    with open("scores.txt", "r") as file:
        scores = file.readlines()

    valid_scores = []
    for score in scores:
        parts = score.split()
        if len(parts) == 2:
            valid_scores.append((parts[0], int(parts[1])))

    valid_scores = sorted(valid_scores, key=lambda x: x[1], reverse=True)

    for name, score_value in valid_scores[:5]:
        text = SMALL_FONT.render(f"{name}: {score_value}", True, BLACK)
        win.blit(text, (250, y_offset))
        y_offset += 30
    
    pygame.display.update()
    pygame.time.wait(2000)  # Ajout d'un délai pour afficher les scores pendant 2 secondes

# Afficher le texte au centre
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, text_rect)

# Afficher le pendu en fonction des erreurs
def draw_hangman(errors):
    # Base
    if errors >= 1:
        pygame.draw.line(win, BLACK, (150, 550), (250, 550), 5)
        pygame.draw.line(win, BLACK, (200, 550), (200, 150), 5)
        pygame.draw.line(win, BLACK, (200, 150), (350, 150), 5)
        pygame.draw.line(win, BLACK, (350, 150), (350, 200), 5)
    # Corps
    if errors >= 2: pygame.draw.circle(win, BLACK, (350, 230), 30, 3)  # tête
    if errors >= 3: pygame.draw.line(win, BLACK, (350, 260), (350, 340), 3)  # tronc
    if errors >= 4: pygame.draw.line(win, BLACK, (350, 280), (310, 320), 3)  # bras gauche
    if errors >= 5: pygame.draw.line(win, BLACK, (350, 280), (390, 320), 3)  # bras droit
    if errors >= 6: pygame.draw.line(win, BLACK, (350, 340), (380, 400), 3)  # jambe droite
    if errors >= 7: pygame.draw.line(win, BLACK, (350, 340), (320, 400), 3)  # jambe gauche

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
        draw_text("Entrez votre nom:", FONT, BLACK, SCREEN_WIDTH // 2, 150)
        draw_text(name, FONT, BLACK, SCREEN_WIDTH // 2, 250)
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
        win.fill(WHITE)
        draw_text("Entrez un nouveau mot:", FONT, BLACK, SCREEN_WIDTH // 2, 150)
        draw_text(new_word, FONT, BLACK, SCREEN_WIDTH // 2, 250)
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
    
    with open("mots.txt", "a") as file:
        file.write(new_word + "\n")

# Fonction principale du jeu
def game_loop(player_name):
    clock = pygame.time.Clock()
    word, guessed, errors, guessed_letters, missed_letters = start_game()  # Ajouter missed_letters

    # Boucle principale du jeu
    while True:
        win.fill(WHITE)
        draw_text('Pendu', FONT, BLACK, SCREEN_WIDTH // 2, 50)
        draw_text(' '.join(guessed), FONT, BLACK, SCREEN_WIDTH // 2, 350)  # décalé vers le bas
        draw_text(f'Joueur: {player_name}', SMALL_FONT, BLACK, SCREEN_WIDTH // 2, 100)
        draw_hangman(errors)
        draw_missed_letters(missed_letters)  # Ajouter cet appel
        
        if errors >= 7:
            draw_text("Vous avez perdu !", FONT, RED, SCREEN_WIDTH // 2, 450)
            pygame.display.update()
            pygame.mixer.music.load(lose_sound_file)
            pygame.mixer.music.play()
            save_score(player_name, 0)
            pygame.time.wait(2000)
            break
        
        if '_' not in guessed:
            draw_text("Vous avez gagné !", FONT, GREEN, SCREEN_WIDTH // 2, 450)
            pygame.display.update()
            pygame.mixer.music.load(win_sound_file)
            pygame.mixer.music.play()
            score = len([char for char in guessed if char != '_'])
            save_score(player_name, score)
            pygame.time.wait(2000)
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
                letter = pygame.key.name(event.key)
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
def main_menu():
    while True:
        win.fill(WHITE)
        draw_text("Menu du jeu", FONT, GREEN, SCREEN_WIDTH // 2, 50)
        draw_text("Faites votre choix : entre 1 et 4 :", SMALL_FONT, RED, SCREEN_WIDTH // 2, 100)
        draw_text("1. Jouer", SMALL_FONT, BLACK, SCREEN_WIDTH // 2, 200)  # décalé vers le bas
        draw_text("2. Ajouter un mot", SMALL_FONT, BLACK, SCREEN_WIDTH // 2, 250)
        draw_text("3. Scores", SMALL_FONT, BLACK, SCREEN_WIDTH // 2, 300)
        draw_text("4. Quitter", SMALL_FONT, BLACK, SCREEN_WIDTH // 2, 350)
        
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
                    pygame.time.wait(2000)  # Afficher les scores pendant 2 secondes
                elif event.key == pygame.K_4:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    main_menu()