import os
import sys

import numpy as np
import pygame

from SceneRepresent import Scene
from SceneRepresent import SceneElement

class Visualize:
    def __init__(self,*, scene:Scene) -> None:
        self.scene = scene

        self.width = 320
        self.height = 240

        self.scale = max(self.width / scene.sceneWidth, self.height / scene.sceneHeight)
        self.resolution = 1 / self.scale
        self.width = int(scene.sceneWidth * self.scale)
        self.height = int(scene.sceneHeight * self.scale)

        self.originCanvasToScene = np.array([
            -scene.sceneWidth / 2.0,
            scene.sceneHeight / 2.0
        ])
        self.originSceneToCanvas = np.array([
            self.width / 2.0,
            self.height / 2.0
        ])
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

    def drawScene(self) -> None:
        cavas = pygame.Surface((self.width, self.height))
        cavas.fill((255, 255, 255))

        for element in self.scene.sceneElements:
            if element.type == 'Circle':
                pygame.draw.circle(
                    cavas,
                    (0, 0, 0) if element.action == 'None' else (255, 0, 0),
                    self.cvtCoordSceneToCavas(element.center[0], element.center[1]),
                    int(np.sqrt((element.vertices[0][0]) ** 2 + (element.vertices[0][1]) ** 2) / self.resolution),
                    0
                )
            elif element.type == 'Polygon':
                pygame.draw.polygon(
                    cavas,
                    (0, 0, 0) if element.action == 'None' else (255, 0, 0),
                    [self.cvtCoordSceneToCavas(vertex[0], vertex[1]) for vertex in element.verticesTransformed],
                    0
                )

        for startPoint in self.scene.puzzle.start:
            pygame.draw.circle(
                cavas,
                (0, 255, 0),
                self.cvtCoordSceneToCavas(startPoint[0], startPoint[1]),
                3,
                0
            )

        for goalPoint in self.scene.puzzle.goal:
            pygame.draw.circle(
                cavas,
                (0, 0, 255),
                self.cvtCoordSceneToCavas(goalPoint[0], goalPoint[1]),
                3,
                0
            )
        
        self.screen.blit(cavas, (0, 0))
        pygame.event.pump()
        pygame.display.flip()

        self.clock.tick(60)

    def cvtCoordCavasToScene(self, x:int, y:int):
        '''
        Convert map coordinates to scene coordinates
        '''
        return (
           x * self.resolution + self.originCanvasToScene[0],
           -y * self.resolution - self.originCanvasToScene[1]
        )
    
    def cvtCoordSceneToCavas(self, x:float, y:float):
        '''
        Convert scene coordinates to map coordinates
        '''
        return (
            int(x / self.resolution + self.originSceneToCanvas[0]),
            int(-y / self.resolution + self.originSceneToCanvas[1])
        )
    

if __name__ == '__main__':
    scene = Scene(
        sceneFile = 'D:/RlWs/gymtest/Dataset/test1/scene.scn',
        puzzleFile = 'D:/RlWs/gymtest/Dataset/test1/puzzle.puz'
    )
    visualize = Visualize(scene=scene)

    while visualize.running:
        visualize.drawScene()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                visualize.running = False
                break
    pygame.quit()