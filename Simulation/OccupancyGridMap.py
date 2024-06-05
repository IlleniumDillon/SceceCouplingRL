import os
import sys
import numpy as np

from SceneRepresent import Scene
from SceneRepresent import SceneElement


class OccupancyGridMap:
    def __init__(self,*, scene:Scene) -> None:
        self.scene = scene
        self.width = int(scene.sceneWidth / scene.resolution)
        self.height = int(scene.sceneHeight / scene.resolution)
        self.resolution = scene.resolution
        self.mapBlank = np.zeros((self.height, self.width), dtype=np.uint8)
        self.map = np.zeros((self.height, self.width), dtype=np.uint8)
        self.originMapToScene = np.array([
            -scene.sceneWidth / 2.0,
            scene.sceneHeight / 2.0
        ])
        self.originSceneToMap = np.array([
            self.width / 2.0,
            self.height / 2.0
        ])

        self.generateMapBlank()
        self.updateMap()

    def cvtCoordMapToScene(self, x:int, y:int) -> np.array:
        '''
        Convert map coordinates to scene coordinates
        '''
        return np.array([
           x * self.resolution + self.originMapToScene[0],
           -y * self.resolution - self.originMapToScene[1]
        ]).astype(float)
    
    def cvtCoordSceneToMap(self, x:float, y:float) -> np.array:
        '''
        Convert scene coordinates to map coordinates
        '''
        return np.array([
            x / self.resolution + self.originSceneToMap[0],
            -y / self.resolution + self.originSceneToMap[1]
        ]).astype(int)
    
    def generateMapBlank(self) -> None:
        '''
        Generate blank map
        '''
        self.map = np.copy(self.mapBlank)
        for element in self.scene.sceneElements:
            if element.type == 'Circle':
                temp = element.vertices[0]
                self.drawCircle(
                    self.map,
                    self.cvtCoordSceneToMap(element.center[0], element.center[1]),
                    int(
                        np.sqrt(
                            (temp[0] - element.center[0]) ** 2 + (temp[1] - element.center[1]) ** 2
                        ) / self.resolution
                    )
                )
            elif element.type == 'Polygon':
                self.drawPolygon(
                    self.map,
                    [self.cvtCoordSceneToMap(vertex[0], vertex[1]) for vertex in element.verticesTransformed]
                )

    def updateMap(self) -> None:
        '''
        Update map
        '''
        for element in self.scene.sceneElements:
            if element.action == 'None':
                continue
            if element.type == 'Circle':
                temp = element.vertices[0]
                self.drawCircle(
                    self.mapBlank,
                    self.cvtCoordSceneToMap(element.center),
                    int(
                        np.sqrt(
                            (temp[0] - element.center[0]) ** 2 + (temp[1] - element.center[1]) ** 2
                        ) / self.resolution
                    )
                )
            elif element.type == 'Polygon':
                self.drawPolygon(
                    self.mapBlank,
                    [self.cvtCoordSceneToMap(vertex) for vertex in element.vertices]
                )

    def drawCircle(self,map:np.array, center:np.array, radius:int) -> None:
        '''
        Draw circle on map
        '''
        minx = max(0, int(center[0] - radius))
        maxx = min(self.width, int(center[0] + radius))
        miny = max(0, int(center[1] - radius))
        maxy = min(self.height, int(center[1] + radius))
        for x in range(minx, maxx):
            for y in range(miny, maxy):
                if (x - center[0])**2 + (y - center[1])**2 <= radius**2:
                    map[y, x] = 1

    def drawPolygon(self,map:np.array, vertices:list[np.array]) -> None:
        '''
        Draw polygon on map
        '''
        minx = int(min([vertex[0] for vertex in vertices]))
        maxx = int(max([vertex[0] for vertex in vertices]))
        miny = int(min([vertex[1] for vertex in vertices]))
        maxy = int(max([vertex[1] for vertex in vertices]))
        for x in range(minx, maxx):
            for y in range(miny, maxy):
                if self.isInsidePolygon(vertices, np.array([x, y])):
                    map[y, x] = 1

    def isInsidePolygon(self, vertices:list[np.array], point:np.array) -> bool:
        '''
        Check if point is inside polygon
        '''
        n = len(vertices)
        inside = False
        cross = 0
        for i in range(n):
            j = (i + 1) % n
            if self.checkIntersect(vertices[i], vertices[j], point, np.array([self.width, point[1]])):
                cross += 1
        if cross % 2 == 1:
            inside = True
        return inside

    def checkIntersect(self, 
                        a:np.array, 
                        b:np.array,
                        c:np.array,
                        d:np.array) -> bool:
        '''
        Check if two polygons intersect
        '''
        if max(a[0], b[0]) < min(c[0], d[0]) or \
            max(c[0], d[0]) < min(a[0], b[0]) or \
            max(a[1], b[1]) < min(c[1], d[1]) or \
            max(c[1], d[1]) < min(a[1], b[1]):
            return False
        cross = lambda p1,p2: p1[0] * p2[1] - p1[1] * p2[0]
        if cross(a - d, c - d) * cross(b - d, c - d) > 0 or \
            cross(d - b, a - b) * cross(c - b, a - b) > 0:
            return False
        return True
    

if __name__ == '__main__':

    import cv2

    test = Scene(
        sceneFile = 'D:/RlWs/gymtest/Dataset/test1/scene.scn',
        puzzleFile = 'D:/RlWs/gymtest/Dataset/test1/puzzle.puz'
    )
    testMap = OccupancyGridMap(scene = test)

    map = np.copy(testMap.map)
    # show map
    map = 255 - map * 255
    img = cv2.Mat(map)
    cv2.imshow('map', img)
    cv2.waitKey(0)
    
