import pygame

from src.entities import CreateImage
from src.utils import GameConfig


class SelectView:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.stop_times = self.config.fps*0.5
        self.panel_background = CreateImage(self.config, self.config.images.plants_panel_background,y=601)
        self.chooser_background = CreateImage(self.config, self.config.images.plants_chooser_background,y=-87)
        # 465 513
        self.panel_background.add_animation_move(15,y_formula='-34.2',)
        self.chooser_background.add_animation_move(15,y_formula='5.8')
        pass

    def tick(self):
        if self.stop_times != 0:
            if self.stop_times > 0:
                self.stop_times -= 1
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.panel_background.tick()
        self.chooser_background.tick()
