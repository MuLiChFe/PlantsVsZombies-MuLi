import time

from ..utils import GameConfig
from ..entities import CreateImage
from .select_view import SelectView
import pygame


class GamePage:
    @staticmethod
    def _read_info(game_level):
        print(game_level)
        return {
            "level": '1-1',
            "map_index": 0,
            "zombie_list": [],
        }

    def __init__(self, config: GameConfig):
        self.level_elements:dict= {}

        self.next_state = None
        self.config = config
        self.level = '1-1'
        # 读取 info
        self.info = self._read_info(self.level)
        self.level_map = CreateImage(self.config, self.config.images.level_map_group[self.info['map_index']])
        self.select_view()

    def select_view(self):
        # 500px
        self.level_map.tick()
        pygame.display.update()
        time.sleep(1.8)
        #self.level_map.add_animation_move(times=32, x_formula='-15.625')
        self.level_map.add_animation_move(times=32, x_formula='-18.75')
        self.level_elements['select_view'] = SelectView(self.config)
        pass

    def game_view(self):
        # 500px
        self.level_map.add_animation_move(times=32, x_formula='15.625')

        pass

    def elements_tick(self, elements: dict) -> None:
        for element in elements.values():
            if isinstance(element, dict):
                self.elements_tick(element)
            else:
                element.tick()

    async def update(self):
        self.level_map.tick()
        self.elements_tick(self.level_elements)
        self.config.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
