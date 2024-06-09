from ._image import Image


class CreateImage(Image):
    def __init__(self, config, image,x=0, y=0, w=None, h=None) -> None:
        super().__init__(
            config,
            image,
            x=x,
            y=y,
            w=w,
            h=h,
        )
