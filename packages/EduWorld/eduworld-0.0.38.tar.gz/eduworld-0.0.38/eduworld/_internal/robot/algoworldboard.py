r"""
This file is part of eduworld package.

This class defines Board that can read file based world-boards

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

import sys
import re
from pathlib import Path

from .tile import Tile
from .board import Board
from .robot import Robot


# pylint: disable=too-few-public-methods


class ParseAsFn:
    def __init__(self, key: str, fn, required: bool):
        self.key = key
        self.fn = fn
        self.req = required


class ParseAsInt(ParseAsFn):
    def __init__(self, key: str, required: bool = False):
        super().__init__(key, int, required)


class ParseAsFloat(ParseAsFn):
    def __init__(self, key: str, required: bool = False):
        super().__init__(key, float, required)


class ParseAsStr(ParseAsFn):
    def __init__(self, key: str, required: bool = False):
        super().__init__(key, str, required)


class ParseAsInfInt(ParseAsFn):
    def __init__(self, key: str, required: bool = False):
        super().__init__(key, self._inf_int, required)

    def _inf_int(self, v):
        """value of * or -1 means that something will have inifinite size or amount"""
        return -1 if v == "*" else int(v)


class MapDef:
    """Class encapsulating logic for parsing world file definitions
    World file format is defined as follows.
    - It should specify one definition per line in the format
      DEF_NAME: PARAMETERS
    - Empty lines or lines starts with # are ignored
    - PARAMETERS:
        - Format: name=value. There is no spaces around the equals sign!
        - parameters are separated by space
        - case insensitive
        - can appear in any order
        - unknown parameter names are ignored
    - The accepted DEF_NAME: PARAMETERS
        - map: rows=int cols=int
          Technically optional, but *Required* at the moment because Canvas
          does not support drawing of infinite board
          Board is infinite by default but you can make a bounded world by
          specifying a positive int value for both rows and cols, if you do
          both "rows" and "cols" parameters are *required*
        - robot: x=int y=int
          Optional: initial position of 'default' robot in this world
          defaults to 1, 1
        - tile: x=int y=int beepers=N,* temperature=float radiation=float color="" walls=""
            - Required: "x" and "y" parameters
            - Other parameters are optional
            - Parameter "beepers" accepts either special '*' char value
              which means 'inifinite' amount, or positive int value - amount of beepers
            - radiation and temperature accept any float value
              (use dot to separate the whole and fractional parts)
            - Parameter "color" accept any color value described in Tk docs
              but without whitespace between words:
              https://tcl.tk/man/tcl8.6/TkCmd/colors.htm
            - Parameter "walls" describe walls around the cell
              t - top, b - bottom, l - left, r - right, f - full
              It accepts only 't', 'b', 'r', 'l', or 'f' chars
              or any combination of them in any order (e.g. 'tbr' or "tlbr")
              Unknown characters are ignored. e.g. "tool" is the same as "tl"
              Duplicate characters are ignored.
    """

    Invalid = 0
    Size = 1
    Tile = 2
    Robot = 3

    def __init__(self, line: str, line_index: int):
        self.type = 0
        self.data = {}
        self._line = line.strip().lower()
        self._index = line_index
        self._parse()

    def _parse(
        self,
    ) -> None:
        line = self._line
        if not line or line.startswith("#"):
            return
        if line.startswith("map:"):
            self._parse_def("map", MapDef.Size)
            self._validate_size_def()
            return
        if line.startswith("tile:"):
            self._parse_def("tile", MapDef.Tile)
            self._validate_tile_def()
            return
        if line.startswith("robot:"):
            self._parse_def("robot", MapDef.Robot)
            self._validate_robot_def()

    def _validate_robot_def(self):
        pairs = [
            ParseAsInt("x", True),
            ParseAsInt("y", True),
            ParseAsInfInt("beepers"),
        ]
        self._validate_req_data(pairs)

    def _validate_tile_def(self):
        pairs = [
            ParseAsInt("x", True),
            ParseAsInt("y", True),
            ParseAsFloat("radiation"),
            ParseAsFloat("temperature"),
            ParseAsInfInt("beepers"),
            ParseAsStr("color"),
            ParseAsStr("walls"),
            ParseAsStr("mark"),
        ]
        self._validate_req_data(pairs)

    def _validate_size_def(self):
        pairs = [ParseAsInt("rows", True), ParseAsInt("cols", True)]
        self._validate_req_data(pairs)

    def _parse_def(self, def_key: str, def_type: int) -> None:
        self.type = def_type
        start = len(def_key) + 1  # to take into account :
        parts = set(re.split(" ", self._line[start:].lstrip()))
        self._parse_parts(parts)

    def _parse_parts(self, parts) -> None:
        for p in parts:
            p = p.strip()
            if len(p) == 0:
                continue
            k, v = re.split("=", p)
            self.data[k.strip()] = v.strip()

    def _validate_req_data(self, pairs):
        keys = [*self.data.keys()]
        for pfn in pairs:
            if pfn.key in keys:
                keys.remove(pfn.key)
            if pfn.req and pfn.key not in self.data:
                raise ValueError(
                    f'Definition "{self._line}" as {self._index} '
                    f"does not contains required '{pfn.key}' parameter"
                )
            if pfn.key in self.data:
                self.data[pfn.key] = pfn.fn(self.data[pfn.key])

        for k in keys:
            del self.data[k]


class AlgoWorldBoard(Board):
    """Board loaded from the world file in AlgoWorld World format .aww extension"""

    def __init__(self, world: str):
        super().__init__()
        self.world_path = self._find_world_path(world)
        self._load()

    def _find_world_path(self, world_name):
        if not world_name.endswith(".aww"):
            world_name += ".aww"

        package_path = Path(__file__).absolute().parent / "worlds"
        for worlds_dir in [Path("."), Path("worlds"), package_path]:
            if not worlds_dir.is_dir():
                continue
            world_path = worlds_dir / world_name
            if world_path.is_file():
                return world_path

        raise FileNotFoundError(
            "The specified file was not one of provided worlds.\n"
            "Please store custom worlds in a directory named 'worlds'"
        )

    def _parse_map(self):
        with self.world_path.open(encoding="utf-8") as f:
            for i, line in enumerate(f):
                ld = MapDef(line, i)
                if ld.type == MapDef.Size:
                    self.nrows = ld.data["rows"]
                    self.ncols = ld.data["cols"]
                    self.initialized = True
                if ld.type == MapDef.Tile:
                    x = ld.data["x"]
                    y = ld.data["y"]
                    tile = Tile(**ld.data)
                    self.tiles[x, y] = tile
                if ld.type == MapDef.Robot:
                    x = ld.data.get("x", 1)
                    y = ld.data.get("y", 1)
                    b = ld.data.get("beepers", -1)
                    r = Robot()
                    r.setup(name="default", x=x, y=y, beepers=b)
                    self.add_robot(robot=r)

    def save(self):
        lines = []
        lines.append(f"map: rows={self.nrows} cols={self.ncols}\n\n")
        r = self.get_default_robot()
        lines.append(f"robot: x={r.x} y={r.y}\n\n")
        coords = [x for x in self.tiles]
        coords.sort()
        for xy in coords:
            tile = self.tiles[*xy]
            lines.append(f"{tile}\n")
        with open("out.aww", "w") as f:
            f.writelines(lines)

    def _load(self):
        self._parse_map()
        self.place_outer_walls()

        if not self.initialized:
            print(
                "ERROR: Map definition does not contain required MAP tag "
                "with the size of the board (rows and cols)"
            )
            sys.exit(1)
