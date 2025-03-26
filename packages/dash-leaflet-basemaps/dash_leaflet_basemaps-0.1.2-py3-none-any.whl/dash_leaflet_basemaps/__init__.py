"""The init file of the package."""
import dash_leaflet as dl

from .basemaps import basemap_tiles

__version__ = "0.1.2"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"


class BasemapLayer(dl.TileLayer):
    """A class to represent a basemap layer."""

    def __init__(self, name: str, show_attribution: bool = True, **kwargs):
        """Initialize the class.

        Args:
            name: The name of the basemap.
            show_attribution: decide if the attribution of the newly added layer should be displayed in leaflet attributions. Must be done in agreement with the licence of each individual layer. Default is ``True``.
            kwargs: any keyword arguments from dash-leaflet TileLayer class knowing that ``url``, ``id`` and ``attribution`` will be ignored.
        """
        # check if the name exists
        if name not in basemap_tiles:
            raise ValueError(
                f"Basemap {name} not found. Available basemaps are: [{', '.join(basemap_tiles.keys())}"
            )

        # get the basemap
        kwargs["url"] = basemap_tiles[name].url
        kwargs["id"] = basemap_tiles[name].id
        kwargs["maxZoom"] = kwargs.get("maxZoom", basemap_tiles[name].max_zoom)

        # add the atribution if requested
        if show_attribution is True:
            kwargs["attribution"] = basemap_tiles[name].attribution

        super().__init__(**kwargs)
