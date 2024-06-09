from typing import Optional

import pygame


class Image:
    def __init__(
            self,
            config,
            default_image: Optional[pygame.surface] = None,
            hover_image: Optional[pygame.surface] = None,
            x=0,
            y=0,
            w: int = None,
            h: int = None,
            **kwargs,
    ) -> None:
        self.config = config
        self.hovered = None
        self.hover_image = None
        self.image = default_image
        self.showed_image = default_image
        self.x = x
        self.y = y
        if w or h:
            self.w = w or config.window.ratio * h
            self.h = h or w / config.window.ratio
            self.default_image = pygame.transform.scale(default_image, (self.w, self.h))
            if hover_image:
                self.hover_image = pygame.transform.scale(hover_image, (self.w, self.h))

        else:
            self.default_image = default_image
            self.hover_image = hover_image
            self.w = default_image.get_width() if default_image else 0
            self.h = default_image.get_height() if default_image else 0
        self._rect = self.default_image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.default_image)
        self.animation_dict = {
            'move': [],
            'flash': [],
        }
        self.stop_times = 0
        self.__dict__.update(kwargs)

    def update_image(
            self, image: pygame.Surface, w: int = None, h: int = None
    ) -> None:
        self.default_image = image
        self.w = w or (image.get_width() if image else 0)
        self.h = h or (image.get_height() if image else 0)

    def add_animation_stop(self,num):
        self.stop_times = num
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def tick(self) -> None:
        if self.stop_times != 0:
            if self.stop_times > 0:
                self.stop_times -= 1
            return
        self.hover_update()
        self._animation_flash()
        self._animation_move()
        # process animation
        # move animation
        self.draw()

    def draw(self) -> None:
        if self.image:
            self.config.screen.blit(self.image, self.rect)

    # move the image
    def add_animation_move(self, times: int, x_formula: str = '0', y_formula: str = '0', break_gap: int = 0) -> None:
        if times == -1:
            self.animation_dict['move'] = []
            return
        self.animation_dict['move'].append({'times': times,
                                            'direction': [x_formula, y_formula],
                                            'break_info': [0, break_gap]})

    def _animation_move(self):
        if not self.animation_dict['move']:
            return
        times, direction, break_info = self.animation_dict['move'][0].values()
        if times == 0:
            del self.animation_dict['move'][0]
            return self._animation_move()
        current_break_time, aim_break_gap = break_info
        if current_break_time < aim_break_gap:
            self.animation_dict['move'][0]['break_info'] = [current_break_time + 1, aim_break_gap]
            return
        self.animation_dict['move'][0]['break_info'] = [0, aim_break_gap]
        times -= 1
        x_func, y_func = direction
        self.x += float(eval(x_func.replace('t', str(times))))
        self.y += float(eval(y_func.replace('t', str(times))))
        self.animation_dict['move'][0]['times'] -= 1

    # switch the image in the image list
    def add_animation_flash(self, times: int, loop_list, current, break_gap) -> None:
        if times == -1:
            self.animation_dict['flash'] = []
            return
        self.animation_dict['flash'].append({'times': times,
                                             'loop_info': [loop_list, current],
                                             'break_info': [0, break_gap]})

    def _animation_flash(self):
        if not self.animation_dict['flash']:
            return
        times, loop_info, break_info = self.animation_dict['flash'][0].values()
        if times == 0:
            del self.animation_dict['flash'][0]
            return self._animation_move()
        current_break_time, aim_break_gap = break_info
        if current_break_time < aim_break_gap:
            self.animation_dict['flash'][0]['break_info'] = [current_break_time + 1, aim_break_gap]
            return
        self.animation_dict['flash'][0]['break_info'] = [0, aim_break_gap]
        times -= 1
        loop_list, current = loop_info
        image_index = (current + 1) % len(loop_list)
        self.image = loop_list[image_index]
        self.showed_image = self.image
        self.animation_dict['flash'][0]['times'] -= 1
        self.animation_dict['flash'][0]['loop_info'] = [loop_list, image_index]

    def hover_update(self):
        """根据悬停状态更新图片。"""
        if not self.hover_image:
            return
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (mouse_pos[0] - self._rect.x, mouse_pos[1] - self._rect.y)
        self.hovered = self._rect.collidepoint(mouse_pos) and self.mask.get_at(relative_mouse_pos)
        self.image = self.hovered and self.hover_image or self.showed_image
        pygame.mouse.set_cursor(self.hovered and pygame.SYSTEM_CURSOR_HAND or pygame.SYSTEM_CURSOR_ARROW)
