import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Paramètres du jeu
bird_width = 34
bird_height = 24
bird_velocity = 0
gravity = 0.5
jump = -10

pipe_width = 80
pipe_gap = 200
pipe_velocity = 5
pipe_frequency = 1500  # Milliseconds

# Chargement des ressources
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, bird_width, bird_height))

    def update(self):
        self.velocity += gravity
        self.y += self.velocity

    def flap(self):
        self.velocity = jump

class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, pipe_width, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + pipe_gap, pipe_width, screen_height - self.height - pipe_gap))

    def update(self):
        self.x -= pipe_velocity

def draw_button(screen, text, x, y, width, height):
    pygame.draw.rect(screen, WHITE, [x, y, width, height])
    pygame.draw.rect(screen, BLACK, [x, y, width, height], 2)
    label = small_font.render(text, True, BLACK)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

def main():
    bird = Bird(100, 300)
    pipes = []
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    score = 0
    running = True

    while running:
        screen.fill(LIGHT_BLUE)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Physique de l'oiseau
        bird.update()

        # Génération des tuyaux
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequency:
            pipe_height = random.randint(100, screen_height - pipe_gap - 100)
            pipes.append(Pipe(screen_width, pipe_height))
            last_pipe = current_time

        # Mouvement et dessin des tuyaux
        new_pipes = []
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            if pipe.x + pipe_width > 0:
                new_pipes.append(pipe)
            # Détection de collision
            if bird.x < pipe.x + pipe_width and bird.x + bird_width > pipe.x:
                if bird.y < pipe.height or bird.y + bird_height > pipe.height + pipe_gap:
                    running = False

        pipes = new_pipes

        # Vérification des limites de l'écran
        if bird.y < 0 or bird.y + bird_height > screen_height:
            running = False

        # Dessin de l'oiseau
        bird.draw(screen)

        # Augmentation du score
        score += 1

        # Affichage du score
        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 20))

        # Mise à jour de l'écran
        pygame.display.flip()

        # Cadence de rafraîchissement
        pygame.time.Clock().tick(30)

    # Fin du jeu
    end_game(score)

def end_game(score):
    while True:
        screen.fill(BLACK)
        text = font.render(f"Game Over! Score: {score}", True, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

        # Bouton Rejouer
        button_width = 200
        button_height = 50
        button_x = screen_width // 2 - button_width // 2
        button_y = screen_height // 2 + text.get_height()

        draw_button(screen, "Rejouer", button_x, button_y, button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                    main()

        pygame.display.flip()

if __name__ == "__main__":
    main()
