"""
Class repesenting a map tile

This file is part of eduworld package.

=== LICENSE INFO ===

Copyright (c) 2024 - Stanislav Grinkov

The eduworld package is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

The package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the algoworld package.
If not, see `<https://www.gnu.org/licenses/>`_.
"""

from typing import Tuple, Dict
from .tile import Tile


Coords = Tuple[int, int]
MapType = Dict[Coords, Tile]


class TileMap:
    """Sparse container for a tiles on a grid"""

    def __init__(self):
        self.tiles: MapType = {}

    def __getitem__(self, xy: Coords) -> Tile:
        return self.tiles.get(xy, Tile(*xy))

    def __setitem__(self, xy: Coords, tile: Tile) -> None:
        self.tiles[xy] = tile

    def __contains__(self, xy: Coords) -> bool:
        return xy in self.tiles

    def __iter__(self):
        return self.tiles.__iter__()
