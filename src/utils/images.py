import random
from typing import List, Tuple

import pygame


class Images:

    adventure_group:list[pygame.Surface]
    background: pygame.Surface

    def __init__(self) -> None:
        # convert_alpha()
        self.main_menu = pygame.image.load(f'assets/sprites/Screen/main_menu.png').convert()
        self.adventure_group = [
            pygame.image.load(f'assets/sprites/Screen/Adventure_0.png').convert_alpha(),
            pygame.image.load(f'assets/sprites/Screen/Adventure_1.png').convert_alpha(),
        ]
        self.level_map_group = [
            pygame.image.load(f'assets/sprites/Background/Background_{index}.jpg').convert() for index in range(5)
        ]

        self.plants_panel_background = pygame.image.load(f'assets/sprites/Screen/PanelBackground.png').convert_alpha()
        self.plants_chooser_background = pygame.image.load(f'assets/sprites/Screen/ChooserBackground.png')