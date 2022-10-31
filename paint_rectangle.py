import turtle
from sympy import Segment, Point, Polygon, Ray, N, oo
from mpmath import radians, degrees
import random
from math import asin, sqrt, pi
import collections
import re


bounce_limit = 400
paint_len = 1
def all_painted():
    for e in E:
        if edge_hits[e][0].distance(edge_hits[e][1]) > paint_len/2 or\
            edge_hits[e][-1].distance(edge_hits[e][-2]) > paint_len/2:
                return False
        for i,j in zip(edge_hits[e][1:], edge_hits[e][2:]):
            if i.distance(j) > paint_len:
                return False
    return True
def paint(e, hit):
   
    turtle.tracer(False)
    a.penup()
    a.goto(hit)
    a.setheading(a.towards(N(e.p1.x), N(e.p1.y)))
    dist = min(N(Point(a.pos()).distance(e.p1)), paint_len/2)
    a.forward(dist)
    dist = min(N(Point(a.pos()).distance(e.p2)), paint_len)
    a.setheading(a.towards(N(e.p2.x), N(e.p2.y)))
    a.pendown()
    a.forward(dist)
    a.penup()
    #turtle.tracer(True)
    for i in range(len(edge_hits[e])-1):
        if edge_hits[e][i].distance(e.p1) < hit.distance(e.p1) and\
            edge_hits[e][i+1].distance(e.p1) > hit.distance(e.p1):
                edge_hits[e].insert(i+1, hit)
                break
    turtle.tracer(True)

            
            
            
def superscript(n):
    return "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[ord(c)-ord('0')] for c in str(n)])



def find_signature(hits):
    s = ''.join(chr(97+i) for i in hits)
    print(s)
    max_length = int(len(hits)/2)

    result = re.sub(
        rf'(\w{{2,{max_length}}}?)(\1+)', # Omit the second number in the repetition to match any number of repeating chars (\w{2,}?)(\1+)
        lambda m: f'({m.group(1)}){superscript(len(m.group(0))//len(m.group(1)))}',
        s
    )
 
    sig_len = 0
    for c in result[0:len(result):1]:
        if c.isalpha():
            sig_len += 1
    print(result, 'length:', sig_len)
    



def run(x, y, angle):
    hits = []
    nb_bounces = 1
    #t.clear()
    #turtle.tracer(False)
    t.pu()
    t.goto(x,y)
    t.setheading(angle)
    t.stamp()
    pos = Point(t.pos())
    vec = Ray(pos, angle=radians(t.heading()))
    for e in E:
        edge_hits[e] = [e.p1, e.p2]
    
    turtle.tracer(True)
    t.pd()
    while True:
        min_dist = oo
        hit = None
        hit_edge = None
        for e in E:
            intersections = vec.intersection(e)
            if len(intersections) > 0:
                for i in intersections:
                    if isinstance(i, Point):
                        if pos.distance(i) < min_dist and pos.distance(i) > .00001:
                            min_dist = pos.distance(i)
                            hit = i
                            hit_edge = e
        if hit != None:
            pt = hit_edge.perpendicular_line(hit).projection(pos)
            t.goto(hit)
            paint(hit_edge, N(hit))
            nb_bounces = nb_bounces + 1
            print(N(hit))
            hits.append(hit)
            if all_painted():
                return nb_bounces, hits
            
            angle = 2 * t.towards(pt.x, pt.y) - 180 - t.heading()
            t.setheading(angle)
            pos = Point(t.pos())
            vec = Ray(pos, angle=radians(t.heading()))
            
            
    


side_len_a = 6
side_len_b = 14
x,y = 0,2.5 # starting pos
V = [(0,0), (side_len_b,0), (side_len_b,side_len_a), (0,side_len_a)]
maxX, maxY = map(max, zip(*V))
minX, minY = map(min, zip(*V))
max_overall = max(maxX, maxY)
min_overall = min(minX, minY)
turtle.setworldcoordinates(min_overall-.1, min_overall-.1, max_overall+.1, max_overall+.1)



turtle.tracer(False)
t = turtle.Turtle()
a = turtle.Turtle()
m = turtle.Turtle()
m.hideturtle()
a.hideturtle()
a.color('blue')
m.width(2)
a.width(2)

m.penup()
m.goto(V[0])
m.pendown()
for v in V[1:]:
    m.goto(v)
m.goto(V[0])
m.penup()

E = []
for u,v in zip(V, V[1:]):
    E.append(Segment(u,v))
E.append(Segment(V[-1], V[0]))
edge_hits = {}
for e in E:
    edge_hits[e] = [e.p1, e.p2]


# print(E[:4])
# m.penup()
# m.goto(V[0])
# print('\\coordinate({:d}) at ({:.1f},{:.1f}) {{}};'.format(i, m.xcor(), m.ycor()))
# m.pendown()
# for v in V[1:]:
#     m.goto(v)
#     print('\\coordinate({:d}) at ({:.1f},{:.1f}) {{}};'.format(i, m.xcor(), m.ycor()))
# m.goto(V[0])
# m.penup()



angle = 45#random.uniform(minX+.01, maxX-.01), random.uniform(minY+.01, maxY-.01), random.uniform(.1,359.9)
t.color('red')

t.speed(0)
turtle.tracer(False)
nb_bounces, hit_points = run(x, y, angle)
#t.hideturtle()


#turtle.tracer(False)

i = 1 # len(edge_hits) - 4
for pt in hit_points:
    posx, posy = pt.x, pt.y
    
    if posx != 0:
        posx = N(pt.x,2)
    else:
        posx = 0.0
    if posy != 0:
        posy = N(pt.y,2)
    else:
        posy = 0.0
    print("\\coordinate (%d) at (%.1f,%.1f);" % (i, posx, posy))
    #m.goto(N(pt.x) ,N(pt.y))
    #m.dot(5)
    # m.goto(N(pt.x) ,N(pt.y) + .01)
    # m.write(i)
    i += 1






turtle.exitonclick()
turtle.done()
