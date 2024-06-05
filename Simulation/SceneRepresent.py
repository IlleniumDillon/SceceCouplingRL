import os
import sys
import numpy as np
import json

class SceneElement:
    '''
    SceneElement class
    '''
    def __init__(self,*,
                name:str,
                type:str,
                center:np.ndarray,
                rotation:float,
                vertices:list[np.ndarray],
                action:str = 'None',
                anchor:list[np.ndarray] = []):
        '''
        Constructor

        Args:
            name: str   - name of the element
            type: str   - type of the element: 'Polygon' or 'Circle'
            center: np.ndarray  - center of the element
            rotation: float    - rotation of the element
            vertices: list[np.ndarray]  - vertices of the element
            action: str - action of the element: 'None', 'Move', 'Rotate'
            anchor: list[np.ndarray]    - anchor of the element
        '''
        self.name = name
        # check if type is valid
        if type not in ['Polygon', 'Circle']:
            raise ValueError('Invalid type of element. Must be either Polygon or Circle')
        self.type = type
        self.center = center
        self.rotation = rotation
        self.vertices = vertices
        # check if action is valid
        if action not in ['None', 'Move', 'Rotate']:
            raise ValueError('Invalid action of element. Must be either None, Move or Rotate')
        self.action = action
        self.anchor = anchor

        self.verticesTransformed = []
        self.anchorTransformed = []

        self.updateGeometry()

    def updateGeometry(self):
        '''
        Update geometry of the vertices and anchor
        '''
        if self.type == 'Polygon':
            self.verticesTransformed.clear()
            for vertex in self.vertices:
                point = np.array([
                    vertex[0] * np.cos(self.rotation) - vertex[1] * np.sin(self.rotation) + self.center[0],
                    vertex[0] * np.sin(self.rotation) + vertex[1] * np.cos(self.rotation) + self.center[1]
                ])
                self.verticesTransformed.append(point)
            self.anchorTransformed.clear()
            for anchor in self.anchor:
                point = np.array([
                    anchor[0] * np.cos(self.rotation) - anchor[1] * np.sin(self.rotation) + self.center[0],
                    anchor[0] * np.sin(self.rotation) + anchor[1] * np.cos(self.rotation) + self.center[1]
                ])
                self.anchorTransformed.append(point)

    def move(self,*, delta:np.ndarray):
        '''
        Move the element

        Args:
            delta: np.ndarray    - delta to move
        '''
        self.center += delta
        self.updateGeometry()

    def rotate(self,*, angle:float):
        '''
        Rotate the element

        Args:
            angle: float    - angle to rotate
        '''
        self.rotation += angle
        self.updateGeometry()
            


class puzzle:
    '''
    Puzzle class
    '''
    def __init__(self):
        self.start = []
        self.goal = []

class Scene:
    '''
    Scene class 
    '''
    def __init__(self, *, sceneFile:str, puzzleFile:str) -> None:
        self.sceneFile = sceneFile
        self.puzzleFile = puzzleFile

        self.sceneWidth = 0.0
        self.sceneHeight = 0.0
        self.resolution = 0.0
        self.sceneElements = []

        self.puzzle = puzzle()

        self.parseSceneFile()
        self.parsePuzzleFile()

    def parseSceneFile(self) -> None:
        '''
        Parse scene file

        Returns: list of SceneElement
        '''
        with open(self.sceneFile, 'r') as f:
            fjson = json.load(f)
            self.sceneWidth = fjson['width']
            self.sceneHeight = fjson['height']
            self.resolution = fjson['resolution']
            for element in fjson['primitives']:
                name = element['name']
                type = element['type']
                center = np.array(element['center'])
                rotation = element['rotation']
                vertices = [np.array(vertex) for vertex in element['vertices']]
                action = element['action']
                anchor = []
                if 'anchor' in element:
                    anchor = [np.array(vertex) for vertex in element['anchor']]
                self.sceneElements.append(
                    SceneElement(
                        name = name,
                        type = type,
                        center = center,
                        rotation = rotation,
                        vertices = vertices,
                        action = action,
                        anchor = anchor
                    )
                )

            print('Scene file parsed')
            print('Scene width:', self.sceneWidth)
            print('Scene height:', self.sceneHeight)
            print('Resolution:', self.resolution)
            print(f'Number of elements: {len(self.sceneElements)}')
    
    def parsePuzzleFile(self) -> None:
        '''
        Parse puzzle file

        Returns: list of SceneElement
        '''
        with open(self.puzzleFile, 'r') as f:
            fjson = json.load(f)

            self.puzzle.start = [np.array(vertex) for vertex in fjson['start']]
            self.puzzle.goal = [np.array(vertex) for vertex in fjson['goal']]

            print('Puzzle file parsed')
            print('Start:', self.puzzle.start)
            print('Goal:', self.puzzle.goal)


if __name__ == '__main__':
    test = Scene(
        sceneFile = 'D:/RlWs/gymtest/Dataset/test1/scene.scn',
        puzzleFile = 'D:/RlWs/gymtest/Dataset/test1/puzzle.puz'
    )