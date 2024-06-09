import asyncio
from typing import Optional
from ._image import Image

import pygame


class ButtonImage(Image):
    def __init__(self,
                 config,
                 default_image: Optional[pygame.surface] = None,
                 hover_image: Optional[pygame.surface] = None,
                 x=0,
                 y=0,
                 w: int = None,
                 h: int = None,
                 **kwargs,
                 ) -> None:
        super().__init__(
            config=config,
            default_image=default_image,
            hover_image=hover_image,
            x=x,
            y=y,
            w=w,
            h=h,
            **kwargs,
        )
        self.config = config

    async def handle_event(self, command, if_not) -> bool:
        self.hovered = self._rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            return await command()
        return if_not
