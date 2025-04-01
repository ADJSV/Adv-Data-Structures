#Angel Salges HW2, Plane Sweep
from sortedcontainers import SortedDict
from collections import namedtuple

Event = namedtuple('Event', ['x', 'y', 'segment', 'is_start'])

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    return 0 if val == 0 else (1 if val > 0 else -1)

def do_intersect(seg1, seg2):
    p1, q1 = seg1
    p2, q2 = seg2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True  

    return False  #No intersection

def find_intersection(seg1, seg2):
    (x1, y1), (x2, y2) = seg1
    (x3, y3), (x4, y4) = seg2

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  #If parallel

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

    return (px, py)

def plane_sweep(upper_points, lower_points):
    events = []
    active_segments = SortedDict()
    
    segments = list(zip(upper_points, lower_points))
    
    for segment in segments:
        start, end = segment
        events.append(Event(start[0], start[1], segment, True))
        events.append(Event(end[0], end[1], segment, False))
    
    #Sort events by x then y
    events.sort()

    intersections = []

    for event in events:
        x, y, segment, is_start = event
        
        if is_start:
            active_segments[x] = segment

            #Check for intersections with neighbors
            keys = list(active_segments.keys())
            idx = keys.index(x)

            if idx > 0:
                left_segment = active_segments[keys[idx - 1]]
                if do_intersect(left_segment, segment):
                    intersection = find_intersection(left_segment, segment)
                    if intersection:
                        intersections.append(intersection)

            if idx < len(keys) - 1:
                right_segment = active_segments[keys[idx + 1]]
                if do_intersect(right_segment, segment):
                    intersection = find_intersection(right_segment, segment)
                    if intersection:
                        intersections.append(intersection)

        else:
            if x in active_segments:
                del active_segments[x]

    return intersections
##########################################################################################################
#Main:
#Input
list1 = [(5, 6), (3, 7)]
list2 = [(0, 2), (4, 1)]

#Find intersections
intersections = plane_sweep(list1, list2)
print("Intersection points:", intersections)
