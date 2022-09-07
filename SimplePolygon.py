import numpy as np
from sympy import Circle, Point, N, Segment, Line, Polygon, oo
from itertools import combinations
#import turtle
from PolygonTypes import tetris_S, tetris_L
colorarray = ["red", "green", "blue", "olive", "darkorange", "fuchsia", "maroon", "navy", "yellow"]


#t = turtle.Turtle()
#turtle.setworldcoordinates(-1, -1, 9, 9)
#turtle.tracer(False)
def dist(a,b):
    return N(Point(a).distance(Point(b)))

def slope(seg): 
    s = Segment(seg[0], seg[1])
    return s.slope

def same_segments(e,f):
    return Segment(e[0], e[1]).equals(Segment(f[0], f[1]))

def seg_len(seg):
    return N(Segment(seg[0], seg[1]).length)

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

def closest_point_and_distance(p, e):
    a = e[0]
    b = e[1]
    s = np.subtract(b,a)
    w = np.subtract(p,a)
    ps = np.dot(w, s)
    if ps <= 0:
        return (p,a), a 
    l2 = np.dot(s, s)
    if ps >= l2:
        closest = b
    else:
        closest = np.add(a, ps / l2 * s)
    return (p, [closest[0], closest[1]]), closest

def compute_safe_angles_wp(polygon):
    a = polygon.sides[0].length
    b = polygon.sides[1].length
    prob_a = b/(a+b)
    prob_b = a/(a+b)
    
    return {a: prob_a, b: prob_b}
    
class SimplePolygon:
    def __init__(self, poly):
        #t.speed(0)
        self.polygon = poly
        self.V = []
        self.E = []
        self.reflex = []
        self.rooms = []
        self.doors = []
        self.room_graph = []
        self.door_graph = []
        self.edge_normals = []
        self.minX = oo
        self.minY = oo
        self.maxX = 0
        self.maxY = 0
        
        n = len(poly.vertices)
        for v in poly.vertices:
            self.V.append([v.x, v.y])
            if v.x < self.minX:
                self.minX = v.x
            if v.x > self.maxX:
                self.maxX = v.x
            if v.y < self.minY:
                self.minY = v.y
            if v.y > self.maxY:
                self.maxY = v.y
            
            # t.goto(v.x, v.y)            
            if poly.angles[v] > 3.14:
                self.reflex.append([v.x, v.y])
        # t.home()
        for u,v in zip(range(n-1), range(1,n)):
            self.E.append([self.V[u],self.V[v]])
        self.E.append([self.V[n-1],self.V[0]])   
        
        self.n = len(self.V)
        self.m = len(self.E)
        
    
                    
    def print_edges(self):
        for e in self.E:
            print(e)
    
    def is_edge(self, seg):
        for e in self.E:
            if Segment(e[0], e[1]).equals(Segment(seg[0], seg[1])):
                return True
        return False

    def is_door(self, seg):
        for d in self.doors:
            if set(d) == set(seg):
                return True
        return False

    def get_other_door_endpoint(self, i):
        for d in self.doors:
            if Point(d[0]).equals(Point(self.V[i])):
                return self.V.index(d[1])
            if Point(d[1]).equals(Point(self.V[i])):
                return self.V.index(d[0])
        return -1

    

    def get_edge_by_point(self, pt):
        for e in self.E:
            if Segment(e[0], e[1]).contains(Point(pt)):
                return e
        return None

    def get_other_edge(self, v, e):
        i = self.V.index(v)
        j = self.E.index(e)
        if i == j:
            return self.E[(j+1)%self.m]
        else:
            return self.E[j-1]
    
    def remove_non_orthogonal(self):
        to_be_removed = []
        for d in self.doors:
            if slope(d) not in [0, oo]:
                to_be_removed.append(d)
        
        for rem in to_be_removed:
                self.doors.remove(rem) 

    def remove_same(self):
        to_be_removed = []
        for i in range(len(self.doors)-1):
            for j in range(i+1, len(self.doors)):
                if i not in to_be_removed and j not in to_be_removed:
                    if same_segments(self.doors[i],self.doors[j]):
                        #print(i, '=', j)
                        to_be_removed.append(self.doors[j])
                
                
        for rem in to_be_removed:
            if rem in self.doors:
                self.doors.remove(rem)

            

    def compute_virtual_doors(self):
        for v in self.reflex:
            minDist = oo
            minSeg = None
            for e in self.E:
                seg, pt = closest_point_and_distance(v, e)
                if seg_len(seg) < minDist and seg_len(seg) > .01 and not self.is_edge(seg):
                    minSeg = seg
                    minDist = seg_len(seg)
            self.doors.append(minSeg)
        
        ##print('door len', len(self.doors))
        self.remove_non_orthogonal()
        ##print('door len after ort', len(self.doors))
        self.remove_same()
        ##print('door after same', len(self.doors))
        # for d in self.doors:
        #     #print(d)
        


    def get_ccw_points(self):
        ##print('old len', len(self.V))
        for d in self.doors:
            if d[0] not in self.V:
                e = self.get_edge_by_point(d[0])
                u = self.V.index(e[0])
                self.V.insert(u+1, d[0])
            elif d[1] not in self.V:
                e = self.get_edge_by_point(d[1])
                u = self.V.index(e[0])
                self.V.insert(u+1, d[1])
        ##print('new len', len(self.V))
        self.n = len(self.V)
        i = 0
        for v in self.V:
            # t.goto(v[0], v[1])
            # t.write(i)
            i += 1
            
    def decompose(self):
        #t.penup()
        #t.speed(6)
        self.compute_virtual_doors()
        self.get_ccw_points()
        ctr = 0
        queue = [0]
        visited = [False for i in range(self.n)]
        visited[0] = True
        ctr = 0
        while queue:
            room = []
            j = queue.pop()
            #print('pop', j)
            #t.goto(self.V[j][0], self.V[j][1])
            room.append(j)
            visited[j] = True
            i = j + 1
            #print(i)
            # t.begin_fill()
            # t.goto(self.V[i][0], self.V[i][1])
            # t.fillcolor(colorarray[ctr])
            while i != j:
                # t.goto(self.V[i][0], self.V[i][1])
                room.append(i)
                other_endpoint = self.get_other_door_endpoint(i)	
                if other_endpoint == j:
                    break
                if other_endpoint != -1 and other_endpoint not in room:
                    #print('other endpoint:', other_endpoint, 'not in room:', room)
                    if not visited[i]:
                        queue.append(i)
                        visited[i] = True
                        #print('Q', queue)
                    i = other_endpoint
                else:
                    i = (i+1)%self.n
                #print(i)
            ctr += 1
            # t.end_fill()
            #print('room', room)
            self.rooms.append(room)
        r = len(self.rooms)
        self.room_graph = [[None for x in range(r)] for y in range(r)]

    def find_adjacent_rooms(self, door):
        u = self.V.index(door[0])
        v = self.V.index(door[1])
        for (ri, rj) in combinations(self.rooms, 2):  # 2 for pairs, 3 for triplets, etc
            if (set(ri) & set(rj)) == set([u,v]):
                return ri, rj
   
    def build_room_graph(self):
        for door in self.doors:
            u, v = self.find_adjacent_rooms(door)
            self.room_graph[u][v] = door
            self.room_graph[v][u] = door
            self.door_graph[door] = [u,v]
    
    def get_adjacent_room(self, room, door):
        u, v = self.door_graph[door]
        if room == u:
            return v
        else:
            return u
        
    def compute_smart_angles(self):
        self.decompose()
        #print(self.polygon)
        subpolygons = []
        angles_wp = {}
        total_area=self.polygon.area
        for r in self.rooms:
            vertices = []
            for i in r:
                vertices.append(self.V[i])
            subpolygons.append(Polygon(*vertices))
        min_side_len = oo
        max_side_len = -oo
        for poly in subpolygons:
            prob = compute_safe_angles_wp(poly)
            print(prob)
            for side_len in prob:
                if side_len < min_side_len:
                    min_side_len = side_len
                if side_len > max_side_len:
                    max_side_len = side_len
                if side_len in angles_wp:
                    angles_wp[side_len] = angles_wp[side_len] * (poly.area/total_area)*prob[side_len]
                else:
                    angles_wp[side_len] = (poly.area/total_area)*prob[side_len]
        total = sum(angles_wp.values())
        for side_len in angles_wp:
            angles_wp[side_len] = angles_wp[side_len] / total
        prob = {}
        p = 0
        for side_len in angles_wp:
            prob[N(p,5), N(angles_wp[side_len] + p,5)] = N(side_len,5)
            p = angles_wp[side_len]
        #print(prob)
        return prob, max_side_len
        
    
