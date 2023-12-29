#this code is from someone helping me out with trying to get the book cover image url
from customtkinter import (
    CTk,
    CTkLabel,
    CTkFont,
    CTkImage
)
from requests import get as get_from
from PIL.Image import open as open_img
from io import BytesIO
class CTkUrlLabel(CTkLabel):
    """
    A class designed to ease and facilitate the image fetching from web URL in `customtkinter`.

    Specific methods:
    - cget()        : Updated to get the url image.
    - configure()   : Updated to update the url image.

    Specific attributes:
    - url           : Complete url of the image
    - params        : Some webservers requires params while some do not.
    - url_image_size: If None, it will use actual size of the image

    """

    def __init__(self,
                 master: any,
                 width: int = 0,
                 height: int = 28,
                 corner_radius: int | None = None,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = None,
                 text_color: str | tuple[str, str] | None = None,
                 text_color_disabled: str | tuple[str, str] | None = None, text: str = "CTkLabel",
                 font: tuple | CTkFont | None = None,
                 image: CTkImage | None = None,
                 compound: str = "center",
                 anchor: str = "center",
                 wraplength: int = 0,
                 url: str | None = None,
                 params: dict | None = None,
                 url_image_size: tuple[int, int] = None,
                 **kwargs):

        # Saving URL Image specific options
        self._url = url
        self._url_image = None
        self.__image = None
        self._params = params
        self._url_image_size = url_image_size

        if url:
            self.__image, image = image, None

        super().__init__(master, width, height, corner_radius, bg_color, fg_color, text_color, text_color_disabled,
                         text, font, image, compound, anchor, wraplength, **kwargs)

        # Calling the URL function at start
        if url: self._fetch_from_url()

    def _fetch_from_url(self):
        try:
            # Fetching the image from resource locator
            url_response = get_from(url=self._url, params=self._params)
            url_image = open_img(BytesIO(url_response.content))

            # Setting up the new fetched image.
            self._url_image = CTkImage(url_image, None,
                                       size=url_image.size if not self._url_image_size else self._url_image_size)
            self.configure(image=self._url_image)

        except:
            # If there is an error, set default image.
            self.configure(image=self.__image)

    def cget(self, attribute_name: str) -> any:
        """On 'url_image' returns object of `CTkImage` if any."""
        if "url_image" == attribute_name:
            return self._url_image

        return super().cget(attribute_name)

    def configure(self, require_redraw=False, **kwargs):
        """URL image options: 'url', 'params', and 'url_image_size'."""
        if "url" in kwargs:
            self._url = kwargs.pop("url")
            self._fetch_from_url()
        if "params" in kwargs:
            self._params = kwargs.pop("params")
            self._fetch_from_url()
        if "url_image_size" in kwargs:
            self._url_image_size = kwargs.pop("url_image_size")
            self._fetch_from_url()

        return super().configure(require_redraw, **kwargs)