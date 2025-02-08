import random, os, pygame, unidecode

# Initialiser Pygame
pygame.init()
pygame.mixer.init()  # Initialiser le module de mixage audio

# Paramètres de la fenêtre
win = pygame.display.set_mode((1280, 720))

background = pygame.image.load('background.jpg')
# Titre de la fenêtre :
pygame.display.set_caption("Jeu du Pendu")

# Couleurs
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0) ,(255, 0, 0),(0, 255, 0),(0, 0, 255)
YELLOW, ORANGE, PURPLE, BROWN,PINK = (255, 255, 0),(255, 165, 0),(128, 0, 128),(165, 42, 42),(255, 192, 203)

# Police
FONT = pygame.font.SysFont('Roboto', 50)
SMALL_FONT = pygame.font.SysFont('Roboto', 25)

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
    win.fill(YELLOW)
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
    header_name = SMALL_FONT.render("NOM", True, BLUE)
    header_score = SMALL_FONT.render("SCORE", True, BLUE)
    win.blit(header_name, (250, y_offset))
    win.blit(header_score, (600, y_offset))
    y_offset += 40

    # Afficher les scores dans le tableau
    for name, score_value in valid_scores[:10]:# on peut afficher que les 5 premiers [:5]
        text_name = SMALL_FONT.render(name, True, PURPLE)
        text_score = SMALL_FONT.render(str(score_value), True, PURPLE)
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
        pygame.draw.line(win, BLACK, (150, 550), (250, 550), 6)
        pygame.draw.line(win, BLACK, (200, 550), (200, 150), 6)
        pygame.draw.line(win, BLACK, (200, 150), (350, 150), 6)
        pygame.draw.line(win, BLACK, (350, 150), (350, 250), 6)

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
    word, guessed, errors, guessed_letters, missed_letters = start_game()
    while True:
        win.fill(WHITE)
        draw_text('Pendu', FONT, BLACK, 1280 // 2, 50)
        draw_text(' '.join(guessed), FONT, BLACK, 1280 // 2, 350)
        draw_text(f'Joueur: {player_name}', SMALL_FONT, BROWN, 1280 // 2, 100)
        draw_hangman(errors, word)
        draw_missed_letters(missed_letters)

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
                letter = event.unicode.upper()
                if letter.isalpha() and letter not in guessed_letters:
                    guessed_letters.append(letter)
                    if letter in word:
                        for i in range(len(word)):
                            if word[i] == letter:
                                guessed[i] = letter
                    else:
                        errors += 1
                        missed_letters.append(letter)

        pygame.display.update()
        clock.tick(10)

# Menu principal
def main():
    while True:
        
        win.blit(background, (0, 0))
         
        draw_text("Menu du jeu", FONT, GREEN, 1280 // 2, 50)
       
        # Définition des rectangles pour les zones cliquables
        do_your_choice = pygame.Rect(1280 // 2 - 200, 250, 350, 40)
        play_rect = pygame.Rect(1280 // 2 - 100, 300, 200, 35)
        add_word_rect = pygame.Rect(1280 // 2 - 100, 350, 200, 35)
        scores_rect = pygame.Rect(1280 // 2 - 100, 400, 200, 35)
        quit_rect = pygame.Rect(1280 // 2 - 100, 450, 200, 35)

        # Dessiner les rectangles pour les zones cliquables
        pygame.draw.rect(win, BLACK, do_your_choice)
        pygame.draw.rect(win, BLACK, play_rect)
        pygame.draw.rect(win, BLACK, add_word_rect)
        pygame.draw.rect(win, BLACK, scores_rect)
        pygame.draw.rect(win, BLACK, quit_rect)
        
        # Textes dans les zones cliquables
        draw_text("Faites votre choix : entre 1 et 4 :", SMALL_FONT, WHITE,do_your_choice.centerx, do_your_choice.centery)
        draw_text("1. Jouer", SMALL_FONT, GREEN, play_rect.centerx, play_rect.centery)
        draw_text("2. Ajouter un mot", SMALL_FONT, GREEN, add_word_rect.centerx, add_word_rect.centery)
        draw_text("3. Scores", SMALL_FONT, GREEN, scores_rect.centerx, scores_rect.centery)
        draw_text("4. Quitter", SMALL_FONT, GREEN, quit_rect.centerx, quit_rect.centery)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    player_name = get_player_name()
                    game_loop(player_name)
                elif add_word_rect.collidepoint(event.pos):
                    add_new_word()
                elif scores_rect.collidepoint(event.pos):
                    show_scores()
                    pygame.time.wait(4000)  # Afficher les scores pendant 2 secondes
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    main()