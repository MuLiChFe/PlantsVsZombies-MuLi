import time
import pygame
from ..entities import ButtonImage, CreateImage
from ..utils import GameConfig


class MainMenuPage:
    def __init__(self, config: GameConfig):
        self.config = config
        self.next_state = None
        print(self.config.window.width)
        self.main_menu = CreateImage(self.config,self.config.images.main_menu,w=self.config.window.width,h=self.config.window.height)
        self.adventure_but = ButtonImage(self.config,
                                         default_image=self.config.images.adventure_group[0],
                                         hover_image=self.config.images.adventure_group[1],
                                         x=410,
                                         y=75, )

    async def _adventure(self):
        self.adventure_but.hover_image = None
        self.adventure_but.add_animation_flash(times=-2,
                                               loop_list=self.config.images.adventure_group,
                                               current=1,
                                               break_gap=self.config.fps * 0.1)
        time_ = time.time() + 2.7
        while time.time() < time_:
            await self.refresh()
        self.next_state = 'game_page'

    async def refresh(self):
        self.main_menu.tick()
        self.adventure_but.tick()
        pygame.display.update()
        self.config.tick()

    async def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                await self.adventure_but.handle_event(self._adventure, False)

        await self.refresh()
