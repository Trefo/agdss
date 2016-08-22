from webclient.models import *
import numpy


def distance(point1, point2):
    return numpy.linalg.norm(numpy.subtract(point1, point2))


class circle():
    def __init__(self, center, radius):
        self.x, self.y = center
        self.center = center
        self.radius = radius

    def point_in_circle(self, point):
        return distance(point, self.center) <= self.radius

def window():
    def __init__(self, top_left, width, height):
        self.x, self.y = top_left
        self.center = top_left
        self.width = width
        self.height = height

    def point_in_window(self, point):
        return point.x >= self.x and point.x <= self.x + self.width and point.y >= self.y and point.y <= self.y + self.height

def line_segment():
    def __init__(self, x1, y1, x2, y2, m):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.m = m
        self.b = self.y - (self.m * self.x)

        def point_on_line_segment(self, point):
            x, y = point
            crossproduct = (y - self.y1) * (self.x2 - self.x1) - (x - self.x1) * (self.x2 - self.x1)
            if abs(crossproduct) != 0:
                return False
            dotproduct = (x - self.x1) * (self.x2 - self.x1) + (y - self.y1)  * (self.y2 - self.y1)
            squaredlengthba = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)
            if dotproduct > squaredlengthba: return False

            return True

#Returns whether circle and window share at least 1 common point
#True iff circle's center is in rectangle or an edge of rectange intersects circle (or is inside circle)
def circle_window_overlap(circle, window):
    if window.point_in_window(circle.center):
        return True
