import pygame
from .utils import Window, GameConfig, Images
from .state import MainMenuPage,GamePage

PAGE_DICT = {
    'main_menu_page': MainMenuPage,
    'game_page': GamePage,
}


class PVZ:
    def __init__(self):
        self.Image = None
        pygame.init()
        pygame.display.set_caption("DVA")
        window = Window(800, 600)
        screen = pygame.display.set_mode((window.width, window.height), vsync=True)

        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=60,
            window=window,
            images=images
        )
        self.window = None
        self.change_sate()

    def change_sate(self,manual :str = None):
        self.window = PAGE_DICT[manual if manual else self.config.state](self.config)

    async def start(self):
        while True:
            await self.window.update()
            await self.update()
            self.config.tick()

    async def update(self):
        if self.window.next_state:
            self.config = self.window.config
            self.config.state = self.window.next_state
            self.change_sate()
            # self.change_sate(self.Window.next_state)
