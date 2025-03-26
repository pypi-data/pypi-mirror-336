"""Build basemaps from different providers as a list of TileLayers."""


from box import Box
from xyzservices import TileProvider
from xyzservices import providers as xyz

xyz_tiles: dict = {
    "OpenStreetMap": {
        "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "attribution": "OpenStreetMap",
        "name": "OpenStreetMap",
    },
    "ROADMAP": {
        "url": "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Maps",
    },
    "SATELLITE": {
        "url": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Satellite",
    },
    "TERRAIN": {
        "url": "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Terrain",
    },
    "HYBRID": {
        "url": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Satellite",
    },
}
"Custom XYZ tile services."


def get_xyz_dict(
    free_only: bool = True,
    _collection: dict | None = None,
    _output: dict | None = None,
) -> dict:
    """Returns a dictionary of xyz services.

    Args:
        free_only: Whether to return only free xyz tile services that do not require an access token.
        _collection: the collection to anylize (subset of :code:`xyz`)
        _output: the dict to use as an output (mutable object)

    Returns:
        A dictionary of xyz services.
    """
    # the 2 following lies avoid to display xyz descriptor in the method documentation
    # do not replace in the prototype default values
    _collection = xyz if _collection is None else _collection
    _output = {} if _output is None else _output

    for v in _collection.values():
        if isinstance(v, TileProvider):
            if not (v.requires_token() and free_only):
                _output[v.name] = v
        else:  # it's a Bunch
            get_xyz_dict(free_only, v, _output)

    return _output


def basemap_names() -> list:
    """Returns a list of available basemaps names.

    Returns:
        A list of available basemaps.
    """
    return list(xyz_tiles.keys()) + list(get_xyz_dict().keys())


def xyz_to_dict() -> dict:
    """Convert all available xyz tile services to dictionary of properties.

    Returns:
        A dictionary of dash-leaflet tile layers.
    """
    leaflet_dict = {}

    for key in xyz_tiles:
        leaflet_dict[key] = {
            "url": xyz_tiles[key]["url"],
            "id": xyz_tiles[key]["name"],
            "attribution": xyz_tiles[key]["attribution"],
            "max_zoom": 22,
        }

    for item in get_xyz_dict().values():
        leaflet_dict[item.name] = {
            "url": item.build_url(),
            "id": item.name,
            "max_zoom": item.get("max_zoom", 22),
            "attribution": item.attribution,
        }

    return leaflet_dict


basemap_tiles: Box = Box(xyz_to_dict(), frozen_box=True)
"the basemaps list as a box"
