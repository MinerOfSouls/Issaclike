from abc import abstractmethod

import arcade

class Item:
    def __init__(self, sprite):
        self.sprite = sprite

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def activated(self, **kwargs):
        pass