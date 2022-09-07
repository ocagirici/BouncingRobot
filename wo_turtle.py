from sympy import Circle, Segment, Point, Polygon, Ray, N, oo,pi
from mpmath import radians, degrees
import random
from math import asin, sqrt
from SimplePolygon import SimplePolygon
import PolygonTypes
# import turtle

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
    for i in range(len(hit_points[e])-1):
        if hit_points[e][i].distance(e.p1) < hit.distance(e.p1) and\
            hit_points[e][i+1].distance(e.p1) > hit.distance(e.p1):
                hit_points[e].insert(i+1, hit)
                break



def run(x, y, alpha, bounce='smart'):
    nb_bounces = 0
    pos = Point(x,y)
    vec = Ray(pos, angle=radians(alpha))
    # t.pu()
    # t.goto(x,y)
    # t.setheading(alpha)
    # t.stamp()
    for e in E:
        hit_points[e] = [e.p1, e.p2] 
    k = 0
    # t.pd()
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
        # t.goto(hit_point)
        # t.write('')
        # t.dot(3)
        if hit_edge == None:
            print(N(pos,1), N(vec,1))
        edge_ray = Ray(N(hit_edge.p1), N(hit_edge.p2))
        curr_vec = Ray(N(pos), N(hit_point))
        diff = hit_point - pos
        hit_angle = curr_vec.angle_between(edge_ray)        
        paint(hit_edge, N(hit_point))
        if all_painted() or nb_bounces >= bounce_limit:
            return nb_bounces
        nb_bounces += 1
        if bounce == 'smart':
            alpha = (1 - k) * N(- hit_angle - pi/2) + k * N(hit_angle + pi/2 + smart_angle)
        elif bounce == 'randsmart':
            ru= random.uniform(.1, degrees(smart_angle)*2)
            alpha = (1-k) * N(- hit_angle - pi/2) + k * (N(hit_angle + pi/2) + radians(ru))
        elif bounce == 'random':
            alpha = random.uniform(N(-pi-hit_angle+.1), N(-hit_angle-.1))
        elif bounce == 'reflect':
            alpha =  N(-2*hit_angle) 
        elif bounce == 'probsmart':
            rand = random.uniform(0,1)
            for p in prob:
                if rand >= p[0] and rand <= p[1]:
                    #print(rand, prob[p])
                    sangle = asin((paint_len) / (sqrt(paint_len ** 2 + prob[p] ** 2)))
                    alpha =  (1 - k) * N(- hit_angle - pi/2) + k * N(hit_angle + pi/2 - sangle*.5)
                    break

        curr_vec = curr_vec.rotate(alpha, pos).translate(N(diff.x), N(diff.y))
        if k == 0:
            k = 1
        elif k == 1:
            k = 0
        pos = hit_point
        if pos in V:
            pos = Circle(pos, .02).intersection(hit_edge)[0]
        vec = curr_vec
        
        
# turtle.setworldcoordinates(-.6, -.6, .6, .6)
# turtle.tracer(False)
# t = turtle.Turtle()
# a = turtle.Turtle()
# m = turtle.Turtle()
# counter = turtle.Turtle()
# a.hideturtle()
# m.hideturtle()
# m.color('blue')
# m.width(2)
# a.width(2)
 
for j in range(2,8):       
    side_ratio = j/10
    if side_ratio > 1:
        side_ratio = 1/side_ratio
    V = [(-.5,-side_ratio/2), (-.5,side_ratio/2), (.5,side_ratio/2), (.5,-side_ratio/2)]
    # m.penup()
    # m.goto(V[0])
    # m.pendown()
    # for v in V[1:]:
    #     m.goto(v)
    # m.goto(V[0])
    # m.penup()
# for j in range(1):
#     V = PolygonTypes.poly_list[j]
    maxX, maxY = map(max, zip(*V))
    minX, minY = map(min, zip(*V))
    max_overall = max(maxX, maxY)
    min_overall = min(minX, minY)
    P = Polygon(*tuple(V))
    prob, side_len = SimplePolygon(P).compute_smart_angles()
    
    
    E = []
    for u,v in zip(V, V[1:]):
        E.append(Segment(u,v))
    E.append(Segment(V[-1], V[0]))
    
    
    test_reflect= []
    test_random = []
    test_smart = []
    test_randsmart = []
    test_probsmart = []
    starting_state = []
    paint_len = .15
    smart_angle = asin((paint_len) / (sqrt(paint_len ** 2 + side_len ** 2)))
    bounce_limit = 1500
    hit_points = {}
    for e in E:
        hit_points[e] = [e.p1, e.p2]
    
    for i in range(20):
        x, y, alpha = random.uniform(minX+.01, maxX-.01), random.uniform(minY+.01, maxY-.01), random.uniform(.1,359.9)
        starting_state.append([x, y, alpha])
        try:
            probsmart = run(x, y, alpha, 'probsmart')
            test_probsmart.append(probsmart)
        except:
            print('Test', (i+1), 'probsmart failed', x, y, alpha, side_ratio)
        try:
            smart = run(x, y, alpha, 'smart')
            test_smart.append(smart)
        except:
            print('Test', (i+1), 'smart failed', x, y, alpha, side_ratio)
       
        try:
            randsmart = run(x, y, alpha, 'randsmart')
            test_randsmart.append(randsmart)
        except:
            print('Test', (i+1), 'randsmart failed', x, y, alpha, side_ratio)
            
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
    
    
    
    
    
    
    
    # for i in range(20):
    #     x, y, alpha = random.uniform(minX+.01, maxX-.01), random.uniform(minY+.01, maxY-.01), random.uniform(.1,359.9)
    #     while not P.encloses_point(Point(x,y)):
    #         x, y = random.uniform(minX+.01, maxX-.01), random.uniform(minY+.01, maxY-.01)
    #     starting_state.append([x, y, alpha])
    #     pos = Point(x,y)
    #     vec = Ray(pos, angle=radians(alpha))
        
    #     try:
    #         smart = run(x, y, alpha, 'smart')
    #         test_smart.append(smart)
    #     except:
    #         print('Test', (i+1), 'smart failed', x, y, alpha)
        
    #     try:
    #         randsmart = run(x, y, alpha, 'randsmart')
    #         test_randsmart.append(randsmart)
    #     except:
    #         print('Test', (i+1), 'randsmart failed', x, y, alpha)
        
    #     try:
    #         reflect = run(x, y, alpha, 'reflect')
    #         test_reflect.append(reflect)
    #     except:
    #         print('Test', (i+1), 'reflect failed', x, y, alpha)

    #     try:
    #         ran = run(x, y, alpha, 'random')
    #         test_random.append(ran)
    #     except:
    #         print('Test', (i+1), 'random failed', x, y, alpha)

    #     try:
    #         print('%s %.2f & %.2f & %.2f & %d & %d & %d & %d \\\\' %(PolygonTypes.poly_list_str[j], x, y, alpha, reflect, ran, smart, randsmart))
    #     except:
    #         print('Test', (i+1), 'skipped', x, y, alpha)
        
        
    
    # print('reflect', min(test_reflect), max(test_reflect), sum(test_reflect)/len(test_reflect))
    # print('random', min(test_random), max(test_random), sum(test_random)/len(test_random))
    # print('smart', min(test_smart), max(test_smart), sum(test_smart)/len(test_smart))
    # print('randsmart', min(test_randsmart), max(test_randsmart), sum(test_randsmart)/len(test_randsmart))
    # print('probsmart', min(test_probsmart), max(test_probsmart), sum(test_probsmart)/len(test_probsmart))