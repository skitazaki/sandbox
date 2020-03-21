#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
from collections import namedtuple
import webapp2
from jpgridmap import jpgrid
import geojson


Coordinates = namedtuple('Coordinates', 'lat lng')


class JsonHandler(webapp2.RequestHandler):

    def set_headers(self):
        origin = self.request.headers.get('origin')
        if origin:
            self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'


class ReverseGeocodingHandler(JsonHandler):

    def get(self, lat, lng):
        self.set_headers()
        coord = Coordinates._make((float(lat), float(lng)))
        grid = jpgrid.encodeEighth(*coord)
        results = {'grid': {
            'lv1': grid[:4],
            'lv2': grid[:6],
            'lv3': grid[:8],
            'base': grid[:8],
            'half': grid[:9],
            'quarter': grid[:10],
            'eighth': grid
        }}
        json.dump(results, self.response)


class ChildrenHandler(JsonHandler):

    def get(self, grid):
        self.set_headers()
        level = len(grid)
        meshes = []
        if level == 4:  # Lv1
            for i in range(8):
                for j in range(8):
                    meshes.append('{}{}{}'.format(grid, i, j))
        elif level == 6:  # Lv2
            for i in range(10):
                for j in range(10):
                    meshes.append('{}{}{}'.format(grid, i, j))
        elif level == 7:  # Unified 5
            pass
        elif level == 8:  # Lv3
            for i in range(4):
                meshes.append('{}{}'.format(grid, i))
        elif level == 9:  # Unified 2 or Half
            # TODO: Detect given grid is Unified 2 or Half ?
            for i in range(4):
                meshes.append('{}{}'.format(grid, i))
        elif level == 10:  # Quarter
            for i in range(4):
                meshes.append('{}{}'.format(grid, i))
        elif level == 11:  # Eighth
            self.response.set_status(404)
            json.dump({'message': 'Children is not found'}, self.response)
            return
        else:
            self.response.set_status(400)
            json.dump({'message': 'Invalid grid mesh code'}, self.response)
            return
        json.dump(meshes, self.response)


class GridHandler(JsonHandler):

    def get(self, grid):
        self.set_headers()
        bbox = jpgrid.bbox(grid)
        center = jpgrid.decode(grid)
        geometry = geojson.LineString(([bbox['s'], bbox['w']],
                                       [bbox['s'], bbox['e']],
                                       [bbox['n'], bbox['e']],
                                       [bbox['n'], bbox['w']],
                                       [bbox['s'], bbox['w']]))
        properties = {'center': center}
        feature = geojson.Feature(geometry=geometry, properties=properties)
        geojson.dump(feature, self.response)


class NeighborHandler(JsonHandler):

    def get(self, grid):
        self.set_headers()
        neighbors = jpgrid.neighbors(grid)
        json.dump(neighbors, self.response)


app = webapp2.WSGIApplication([
    ('/coordinates/(?P<lat>[\d\.]+),(?P<lng>[\d\.]+)', ReverseGeocodingHandler),
    ('/grid/(?P<grid>\d+)', GridHandler),
    ('/grid/(?P<grid>\d+)/children', ChildrenHandler),
    ('/grid/(?P<grid>\d+)/neighbor', NeighborHandler)
], debug=True)
