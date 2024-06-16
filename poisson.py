import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Groupe de poissons")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Paramètres du poisson
num_fish = 50  # Nombre total de poissons
max_speed = 1
neighborhood_radius = 100
avoid_radius = 20  # Distance à laquelle les poissons évitent les autres poissons
cohesion_weight = 0.02
alignment_weight = 0.05
separation_weight = 0.5
randomness_weight = 0.5

class Fish:
    def __init__(self):
        # Initialiser les poissons autour du centre de l'écran
        center_x, center_y = width // 2, height // 2
        self.position = pygame.Vector2(
            random.uniform(center_x - 50, center_x + 50),
            random.uniform(center_y - 50, center_y + 50)
        )
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * max_speed
        self.is_leader = False

    def update(self, fishes):
        if self.is_leader:
            self.copy_movement(fishes)
        else:
            self.flock(fishes)
        self.position += self.velocity
        self.edges()

    def edges(self):
        if self.position.x > width:
            self.position.x = width
            self.velocity.x *= -1  # Inverser la direction horizontale
        elif self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= -1  # Inverser la direction horizontale
        if self.position.y > height:
            self.position.y = height
            self.velocity.y *= -1  # Inverser la direction verticale
        elif self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -1  # Inverser la direction verticale

    def flock(self, fishes):
        alignment = pygame.Vector2(0, 0)
        cohesion = pygame.Vector2(0, 0)
        separation = pygame.Vector2(0, 0)
        random_movement = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        total = 0

        for fish in fishes:
            distance = self.position.distance_to(fish.position)
            if fish != self and distance < neighborhood_radius:
                alignment += fish.velocity
                cohesion += fish.position
                if distance < avoid_radius:
                    separation += self.position - fish.position
                total += 1

        if total > 0:
            alignment /= total
            alignment = alignment.normalize() * max_speed

            cohesion /= total
            if cohesion.length() > 0:
                cohesion = (cohesion - self.position).normalize() * max_speed * 0.5  # Réduire l'impact de la cohésion

            if separation.length() > 0:
                separation /= total
                separation = separation.normalize() * max_speed

            self.velocity += alignment * alignment_weight
            self.velocity += cohesion * cohesion_weight
            self.velocity += separation * separation_weight

        self.velocity += random_movement * randomness_weight
        self.velocity = self.velocity.normalize() * max_speed

    def copy_movement(self, fishes):
        for fish in fishes:
            if not fish.is_leader:
                fish.velocity += (self.velocity - fish.velocity) * 0.1

# Créer un groupe de poissons
fishes = [Fish() for _ in range(num_fish)]

# Choisir un leader aléatoire parmi les poissons
leader = random.choice(fishes)
leader.is_leader = True

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for fish in fishes:
        fish.update(fishes)
        if fish.is_leader:
            # Dessiner le leader en blanc
            pygame.draw.circle(screen, WHITE, (int(fish.position.x), int(fish.position.y)), 5)
        else:
            # Dessiner les autres poissons en blanc également
            pygame.draw.circle(screen, WHITE, (int(fish.position.x), int(fish.position.y)), 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
