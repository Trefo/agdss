from webclient.models import *
import numpy
import re
import matplotlib.pyplot as plt

#Note that this geometry uses the top left as (0,0) and going down and to the right is positive

def distance(point1, point2):
    return numpy.linalg.norm(numpy.subtract(point1, point2))


class Circle:
    def __init__(self, center, radius):
        self.x, self.y = center
        self.center = center
        self.radius = radius
    def __str__(self):
        return "(x,y): (%f, %f), radius: %f" %(self.x, self.y, self.radius)

    def point_in_circle(self, point):
        return distance(point, self.center) <= self.radius

class Window:
    def __init__(self, top_left, width, height):
        self.x, self.y = top_left
        self.center = top_left
        self.width = width
        self.height = height

        #Note that vertices are: 0---------1
        #                        |         |
        #                        3---------2
        self.vertices = (top_left, (top_left[0] + width, top_left[1]), (top_left[0] + width, top_left[1] + height), (top_left[0], top_left[1] + height))

    def point_in_window(self, point):
        return point.x >= self.x and point.x <= self.x + self.width and point.y >= self.y and point.y <= self.y + self.height

# class line_segment:
#     def __init__(self, x1, y1, x2, y2, m):
#         self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
#         self.m = m
#         self.b = self.y - (self.m * self.x)
#
#         def point_on_line_segment(self, point):
#             x, y = point
#             crossproduct = (y - self.y1) * (self.x2 - self.x1) - (x - self.x1) * (self.x2 - self.x1)
#             if abs(crossproduct) != 0:
#                 return False
#             dotproduct = (x - self.x1) * (self.x2 - self.x1) + (y - self.y1)  * (self.y2 - self.y1)
#             squaredlengthba = (self.y2 - self.x1) * (self.y2 - self.x1) + (self.y2 - self.y1) * (self.y2 - self.x1)
#             if dotproduct > squaredlengthba: return False
#
#             return True

#Returns whether circle and window share at least 1 common point
#True iff circle's center is in rectangle or an edge of rectange intersects circle (or is inside circle)
def circle_window_overlap(circle, window):
    if window.point_in_window(circle.center):
        return True
    if circle.point_in_circle(window.top_left):
        return True
    ##Check if one of the edges of the window is in the circle
    if(abs(circle.x - window.x) < circle.radius or abs(circle.x - window.x + window.height) < circle.radius or
       abs(circle.y - window.y) < circle.radius or abs(circle.y - window.y + window.height) < circle.radius):
        return True
    return False


re_circle_path = re.compile(r'(<circle[^/>]*cx="(?P<cx>\d*\.?\d*)"[^/>]*cy="(?P<cy>\d*\.?\d*)"[^/>]*r="(?P<radius>\d*\.?\d*)"[^/>]*/>)')

def circles_from_label(label):
    circle_strs = re.finditer(re_circle_path, label.labelShapes)
    circles = []
    for circle_str in circle_strs:
        circles.append(Circle(center=(float(circle_str.group('cx')), float(circle_str.group('cy'))), radius=float(circle_str.group('radius'))))
    return circles


def show_circles(circles):
    fig, ax = plt.subplots()
    ax.set_xlim((0, 1920))
    ax.set_ylim((0, 1080))
    for circle in circles:
        print circle
        pltCircle = plt.Circle(circle.center, circle.radius, color='red')
        ax.add_artist(pltCircle)
    fig.savefig('C:/Users/Sandeep/Dropbox/kumar-prec-ag/temp/t.png')
    plt.show()


# def temp_test():
#     circles = circles_from_label(ImageLabel.objects.all()[0])
#     show_circles(circles)
