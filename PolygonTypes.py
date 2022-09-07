from sympy import Polygon, Point

rectangle = [
  Point(0, 0),
  Point(0, 8),
  Point(8, 8),
  Point(8, 0),
]

challenging = [
    Point(0,0),
 	Point(0,3),
 	Point(1,3),
 	Point(1,1.4),
 	Point(2,1.4),
 	Point(2,3),
 	Point(3,3),
 	Point(3,2.6),
 	Point(4,2.6),
 	Point(4,3),
 	Point(5,3),
 	Point(5,0),
 	Point(4,0),
 	Point(4,2.3),
 	Point(3,2.3),
 	Point(3,0),
 	Point(2,0),
 	Point(2,1.3),
 	Point(1,1.3),
 	Point(1,0)
    ]

default = [
Point(0, 0),
Point(0, 2),
Point(1, 2),
Point(1, 6),
Point(0, 6),
Point(0, 8),
Point(1, 8),
Point(1, 7),
Point(3, 7),
Point(3, 6),
Point(2, 6),
Point(2, 4),
Point(4, 4),
Point(4, 7),
Point(7, 7),
Point(7, 6),
Point(6, 6),
Point(6, 4),
Point(7, 4),
Point(7, 2),
Point(6, 2),
Point(6, 0),
Point(5, 0),
Point(5, 3),
Point(2, 3),
Point(2, 2),
Point(4, 2),
Point(4, 1),
Point(3, 1),
Point(3, 0)
]

tetris_O =[(-.5,-.5), (-.5, .5), (.5,.5), (.5,-.5)]
tetris_I = [(-.5,-.5), (-.5, 1.5), (0,1.5), (0,-.5)]
tetris_L = [(-.5, -.5), (-.5, 1), (0,1), (0,0), (.5,0), (.5,-.5)]
tetris_J = [(-.5, -.5), (-.5, 0), (0,0), (0,1), (.5,1), (.5,-.5)]
tetris_S = [(-.5, -.5), (-.5, 0), (0,0), (0,.5), (1,.5), (1,0), (.5,0), (.5,-.5)]
tetris_Z = [(-.5, -.5), (-.5, 0), (-1,0), (-1,.5), (0,.5), (0,0), (.5,0), (.5,-.5)]

poly_list = [tetris_O, tetris_I, tetris_L, tetris_S]
poly_list_str = ['TetrisO', 'TetrisI', 'TetrisL', 'TetrisS']