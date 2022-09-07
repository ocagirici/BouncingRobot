from tkinter import Tk, Canvas
import turtle
from sympy import Circle, Segment, Point, Polygon, Ray, N,oo
from mpmath import radians, degrees
import random
from math import asin, sqrt
from SimplePolygon import SimplePolygon
import PolygonTypes
def all_painted():
    for e in E:
        if hit_points[e][0].distance(hit_points[e][1]) > paint_len/2 or\
            hit_points[e][-1].distance(hit_points[e][-2]) > paint_len/2:
                return False
        for i,j in zip(hit_points[e][1:], hit_points[e][2:]):
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
    turtle.tracer(True)
    for i in range(len(hit_points[e])-1):
        if hit_points[e][i].distance(e.p1) < hit.distance(e.p1) and\
            hit_points[e][i+1].distance(e.p1) > hit.distance(e.p1):
                hit_points[e].insert(i+1, hit)
                break

def compute_next_bounce(seg, pos, vec):
    #plot_vec(vec, 'cyan')
    distance_to_segments = {}
    hit_edge = None
    hit_point = None
           
    for e in E:
        if e.equals(seg):
            continue
        i = vec.intersection(e)
        if len(i) > 0 and isinstance(i[0], Point):
            distance_to_segments[e] = pos.distance(i[0])
    
    distance_to_segments = sorted(distance_to_segments.items(), key=lambda item: item[1])
    # for dist in distance_to_segments:
    #     print(N(dist[0]), N(dist[1]))
    for segment, dist in distance_to_segments:
        hit_point = vec.intersection(segment)[0]
        #print(N(hit_point))
        if hit_point in V:
            #print('hit point in V')
            hit_point = Circle(hit_point, .02).intersection(segment)[0]
        else:
            hit_edge = segment
            #print(N(hit_edge))
            break

    return hit_point, hit_edge

def run(x, y, angle, bounce='smart', test_nb = 1):
    nb_bounces = 0
    t.clear()
    a.clear()
    parameters.clear()
    parameters_st = '#%s \t %.2f \t %.2f \t %.2f \t %s %s' %(test_nb, x, y, angle, bounce, poly_type)
    parameters.write(parameters_st)
    turtle.tracer(False)
    t.pu()
    t.goto(x,y)
    t.setheading(angle)
    t.stamp()
    pos = Point(t.pos())
    vec = Ray(pos, angle=radians(t.heading()))
    for e in E:
        hit_points[e] = [e.p1, e.p2]
    
    
    
    k = 0
    turtle.tracer(True)
    t.pd()
    hit_edge = None
    while True:
        min_dist = oo
        hit_point = None
        hit_edge = None
        for e in E:
            intersections = vec.intersection(e)
            if len(intersections) > 0:
                for i in intersections:
                    if isinstance(i, Point):
                        if pos.distance(i) < min_dist and pos.distance(i) > .0001:
                            min_dist = pos.distance(i)
                            hit_point = i
                            hit_edge = e
        #print(N(hit_point))
        ln = hit_edge.perpendicular_line(hit_point)
        pt = ln.projection(pos)
        t.goto(hit_point)
       
        paint(hit_edge, N(hit_point))
        if all_painted() or nb_bounces >= bounce_limit:
            return nb_bounces
        nb_bounces += 1
        counter.clear()
        counter.write(nb_bounces, font=("Arial", 12, "bold"))
        
        if bounce == 'smart':
            angle = k * t.towards(pt.x, pt.y) + (1-k) * (t.towards(pt.x, pt.y) + smart_angle*.5)
        elif bounce == 'randsmart':
            angle = k * t.towards(pt.x, pt.y) + (1-k) * (t.towards(pt.x, pt.y) + random.uniform(.1, smart_angle*2))
            #print('ANGLE', angle)
        elif bounce == 'random':
            angle = random.uniform(t.towards(pt.x, pt.y) + 89.9, t.towards(pt.x, pt.y) - 89.9)
        elif bounce == 'reflect':
            angle = 2 * t.towards(pt.x, pt.y) - 180 - angle
        elif bounce == 'probsmart':
            rand = random.uniform(0,1)
            for p in prob:
                if rand >= p[0] and rand <= p[1]:
                    #print(rand, prob[p])
                    sangle = degrees(asin((paint_len) / (sqrt(paint_len ** 2 + prob[p] ** 2))))
                    angle =  k * t.towards(pt.x, pt.y) + (1-k) * (t.towards(pt.x, pt.y) + sangle)
                    break

            
        t.setheading(angle)
        if k == 0:
            k = 1
        elif k == 1:
            k = 0
        pos = Point(t.pos())
        vec = Ray(pos, angle=radians(t.heading()))

#V = PolygonTypes.tetris_L

for j in range(4):       
    # side_ratio = j/10
    # if side_ratio > 1:
    #     side_ratio = 1/side_ratio
    # V = [(-.5,-side_ratio/2), (-.5,side_ratio/2), (.5,side_ratio/2), (.5,-side_ratio/2)]
    V = PolygonTypes.poly_list[j]
    poly_type = PolygonTypes.poly_list_str[j]
    E = []
    for u,v in zip(V, V[1:]):
        E.append(Segment(u,v))
    E.append(Segment(V[-1], V[0]))
    maxX, maxY = map(max, zip(*V))
    minX, minY = map(min, zip(*V))
    max_overall = max(maxX, maxY)
    min_overall = min(minX, minY)
    P = Polygon(*tuple(V))
    prob, side_len = SimplePolygon(P).compute_smart_angles()
    #print(prob)
    turtle.setworldcoordinates(min_overall-.1, min_overall-.1, max_overall+.1, max_overall+.1)
    turtle.tracer(False)
    
    t = turtle.Turtle()
    a = turtle.Turtle()
    m = turtle.Turtle()
    counter = turtle.Turtle()
    a.hideturtle()
    m.hideturtle()
    t.hideturtle()
    counter.hideturtle()
    m.color('blue')
    m.width(2)
    a.width(2)
    t.speed(0)
    a.speed(0)
    a.color('red')
    m.penup()
    m.goto(V[0])
    m.pendown()
    for v in V[1:]:
        m.goto(v)
    m.goto(V[0])
    m.penup()
    counter.goto(maxX, maxY+.05)
    counter.pd()
    t.pd()
    parameters = turtle.Turtle()
    parameters.goto(minX, maxY+.05)
    parameters.pd()
    
    test_reflect= []
    test_random = []
    test_smart = []
    test_randsmart = []
    test_probsmart = []
    starting_state = []
    paint_len = .1
    smart_angle = degrees(asin((paint_len) / (sqrt(paint_len ** 2 + side_len ** 2))))
    #smart_angle = 40
    bounce_limit = 1500
    hit_points = {}
    for e in E:
        hit_points[e] = [e.p1, e.p2]
    
    #x, y, angle = random.uniform(minX+.01, maxX-.01), random.uniform(minY+.01, maxY-.01), random.uniform(.1,359.9)
    #x, y, angle = -.2, -.2, random.uniform(0,360)
    #x, y, angle = .33, .2, random.uniform(0,360)
    
    #run(1, -0.1749028141102265, 0.031421690439504886, 20.132143471740296, 'probsmart')
    # print(run(x, y, angle, 'reflect'), run(x, y, angle, 'random'))
    
    
    for i in range(20):
        x, y, alpha = random.uniform(minX+.01, maxX-.01), random.uniform(minY+.01, maxY-.01), random.uniform(.1,359.9)
        starting_state.append([x, y, alpha])
        try:
            probsmart = run(x, y, alpha, 'probsmart', i+1)
            test_probsmart.append(probsmart)
        except Exception as e:
            print(e, 'Test', (i+1), 'probsmart failed', x, y, alpha)
            
        try:
            smart = run(x, y, alpha, 'smart', i+1)
            test_smart.append(smart)
        except Exception as e :
            print(e, 'Test', (i+1), 'smart failed', x, y, alpha)
       
        try:
            randsmart = run(x, y, alpha, 'randsmart', i+1)
            test_randsmart.append(randsmart)
        except Exception as e:
            print(e, 'Test', (i+1), 'randsmart failed', x, y, alpha)
        
        try:
            reflect = run(x, y, alpha, 'reflect', i+1)
            test_reflect.append(randsmart)
        except Exception as e:
            print(e, 'Test', (i+1), 'reflect failed', x, y, alpha)
            
        try:
            random = run(x, y, alpha, 'random', i+1)
            test_random.append(randsmart)
        except Exception as e:
            print(e, 'Test', (i+1), 'random failed', x, y, alpha)
            
    avg = sum(test_smart)/len(test_smart)
    minimum = min(test_smart)
    maximum = max(test_smart)
    print('{Smart}\t%.2f\t%.2f\t%.2f\\\\' %(avg, maximum-avg, minimum-avg))
    
    avg = sum(test_randsmart)/len(test_randsmart)
    minimum = min(test_randsmart)
    maximum = max(test_randsmart)
    print('{RandSmart}\t%.2f\t%.2f\t%.2f\\\\' %(avg, maximum-avg, minimum-avg))
    
    avg = sum(test_probsmart)/len(test_probsmart)
    minimum = min(test_probsmart)
    maximum = max(test_probsmart)
    print('{ProbSmart}\t%.2f\t%.2f\t%.2f\\\\' %(avg, maximum-avg, minimum-avg))
    
    
# print(starting_state)
# print('reflect:', test_reflect)
# print('random:', test_random)
# print('smart:', test_smart)
# print('randsmart:', test_randsmart)




# turtle.exitonclick()
# turtle.done()
