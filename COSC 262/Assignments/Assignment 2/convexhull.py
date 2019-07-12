"""
   Convex Hull Assignment: COSC262 (2018)
   Student Name: Zachary Sanson
   Usercode: zts12
"""

# ########################## #
# ###   Sub Functions    ### #
# ########################## #


def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]
    """
    with open(filename) as file:
        list_pts = [tuple([float(item) for item in line.split()]) for line in file]
    return list_pts[:N]


def min_num(listPts):
    """Find min value in the list of points"""
    list_pts, min_pt, min_no = listPts, [float('inf'), float('inf')], float('inf')
    for number in range(len(list_pts)):
        # If points are on separate y-levels
        if list_pts[number][1] < min_pt[1]:
            min_pt, min_no = list_pts[number], number
        # If multiple points are on the same y-level / Select the rightmost point
        elif list_pts[number][1] == min_pt[1] and list_pts[number][0] > min_pt[0]:
            min_pt, min_no = list_pts[number], number
    return min_pt, min_no


def theta(point_a, point_b):
    """Find our theta from our list of points"""
    dx, dy = (point_b[0] - point_a[0]), (point_b[1] - point_a[1])
    if (abs(dx) < 1.e-6) and (abs(dy) < 1.e-6):
        t = 0
    else:
        t = dy/(abs(dx) + abs(dy))
    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = 4 + t
    elif t == 0:
        return 360.0
    return t * 90


def isCCW(ptA, ptB, ptC):
    """Finds if the provided points are counter-clockwise"""
    return (ptB[0] - ptA[0]) * (ptC[1] - ptA[1]) - (ptB[1] - ptA[1]) * (ptC[0] - ptA[0]) > 0


# ########################### #
# ###   Main Algorithms   ### #
# ########################### #


# |-------------------------|
# | Gift Wrapping Algorithm |
# |-------------------------|
# Uses the sub-functions: min_num(listPts), theta(point_a, point_b)


# ToDo: 1.0.* Implement Gift Wrapping Algorithm
def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          Gift Wrapping algorithm as a list of m tuples
          [(u0,v0), (u1,v1), ...]
    """
    list_pts = listPts
    # Find smallest point on y-axis
    # => def min_num(listPts):
    min_pt, min_no = min_num(list_pts)
    # Declare variables
    array_size, index, prv_angle, chull, list_pts[array_size] = (len(list_pts) - 1), 0, 0, [], min_pt
    # Repeat
    while min_no != array_size:
        list_pts[index], list_pts[min_no] = list_pts[min_no], list_pts[index]
        chull.append(list_pts[index])
        min_angle = 361
        for point in range(index + 1, array_size + 1):
            # Find angle(theta) between two points
            # => def theta(list_pts):
            angle = theta(list_pts[index], list_pts[point])
            if min_angle > angle > prv_angle and list_pts[point] != list_pts[index]:
                min_angle, min_no = angle, point
        index, prv_angle = (index + 1), min_angle
    # Return convex hull
    return chull


# |-----------------------|
# | Graham Scan Algorithm |
# |-----------------------|
# Uses  the sub-functions: min_num(listPts), theta(point_a, point_b), isCCW(ptA, ptB, ptC)


# ToDo: 2.0.* Implement Graham Scan Algorithm
def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham Scan algorithm as a list of m tuples
         [(u0,v0), (u1,v1), ...]
    """
    list_pts = listPts
    # Find smallest point on y-axis
    # => def min_num(list_pts):
    min_pt, min_no = min_num(list_pts)
    # Sort by angle(theta) about horizontal line --> list
    # => def theta(ptA, ptB):
    pt_angles = sorted(list_pts, key=lambda x: theta(min_pt, x))
    pt_stack, pt_list = [min_pt, pt_angles[0], pt_angles[1]], pt_angles[2:-1]
    for point in pt_list:
        # Check if point is counter-clockwise
        # => isCCW(ptA, ptB, ptC):
        while not isCCW(pt_stack[-2], pt_stack[-1], point):
            pt_stack.pop()
        pt_stack.append(point)
    return pt_stack


# |--------------------------|
# | Monotone Chain Algorithm |
# |--------------------------|
# Uses sub-functions: isCCW(ptA, ptB, ptC)


# ToDo: 3.0.* Implement Method of Choosing (Monotone Chain)
def chain(listPts):
    """Returns the convex hull vertices computed using
          Monotone Chain as a list of m tuples
         [(u0,v0), (u1,v1), ...]
    """
    list_pts, Lower, Upper = sorted(listPts, key=lambda x: (x[0], x[1])), [], []
    if len(list_pts) <= 1:
        return list_pts
    # Lower bound
    for point_l in list_pts:
        while len(Lower) >= 2 and not(isCCW(Lower[-2], Lower[-1], point_l)):
            Lower.pop()
        Lower.append(point_l)
    # Upper bound
    for point_u in reversed(list_pts):
        while len(Upper) >= 2 and not(isCCW(Upper[-2], Upper[-1], point_u)):
            Upper.pop()
        Upper.append(point_u)
    return Lower[:-1] + Upper[:-1]


# |------------------|
# | Chan's Algorithm |
# |------------------|
# Attempt to create Chan's Algorithm - Couldn't get it to correctly work


# def chans(listPts):
#     """
#     n = no_input_points
#     h = no_output_points
#     pick small m
#     partition set into groups of size m
#     Graham scan those groups
#     Then gift wrap for all h
#     Use largest angle?
#     m < h
#     Dont exceed h iterations of gift wrapping
#     Stop after m iterations
#     Increment m until it equals h
#     m = 2^2^t, t = current itteration number
#     """
#     # First stage of Chan's Algorithm
#     P = listPts
#     p_1, _ = min_num(P)  # PICK_START(P), min of P
#     p_0 = (float('-inf'), 0.0)
#     for t in range(1, 100000000):
#         m = min(2**2**t, len(P))  # Magic number
#         print('m:', m)
#         K = len(P) // m  # K = [n/m]
#         Complete = [p_1]  # C := (), Empty list to store points of convex hull
#         # Complete[0] = [p_1]  # ADD(C, p1), Add first point to hull
#         Convex_Hulls = [None for _ in range(K)]
#         Quotients = [P[x:x + m] for x in range(0, len(P), m)]  # SPLIT(P, m), split into K many sub-lists
#         for k in range(1, K):  # Compute hull of all sub-lists
#             Convex_Hulls[k] = grahamscan(Quotients[k])
#         print('CH:', Convex_Hulls)
#
#         result = [(72.0, 15.0), (979.3, 560.0), (432.0, 993.0)]
#         # Using modified Jarvis march algorithm
#         # Second stage of Chan's Algorithm
#         temp_P = Convex_Hulls
#         p = [p_0, p_1]
#         for i in Convex_Hulls[1:]:
#             p.extend(i)
#         z = [None for _ in range(K)]
#         for i in range(1, m):
#             for k in range(1, K):
#                 if i == 1:
#                      z[0] = [p_1]
#                 else:
#                     z[k] = JARVIS_BINARY_SEARCH(p[i - 1], p[i], Convex_Hulls[k])
#         #             choose point z which maximises angle of ^
#         #     Choose the next point on the convex hull P that maximises z
#             if i != 1:
#
#                 p_ahead = JARVIS_NEXT_CH_POINT(p[i - 1], p[i], z)
#                 if p_ahead == p_1 and i != 1:
#                     return Complete
#                 else:
#                     Complete.append(p_ahead)
#
#
# def JARVIS_BINARY_SEARCH(ptA, ptB, setC):
#     # Angle between p[i], p[i - 1] and p[i], d
#     # Angle between ptB, ptA, ptC
#     angles = []
#     if len(setC) <= 1:
#         return setC[0]
#     for ptC in setC:
#         try:
#             angle_1 = theta(ptB, ptA)
#             angle_2 = theta(ptB, ptC)
#             angle = angle_1 - angle_2
#             angles.append((angle, ptC))
#         except:
#             print('here', ptA, ptB, ptC[0])
#             return setC[0]
#
#     new_angles = []
#     for i in angles:
#         if i[0] >= 1:
#             new_angles.append(i)
#     new_angles.sort(key=lambda x: x[0])
#
#     if new_angles == []:
#         print('yes', ptC, setC)
#     # Return max or min? pos 0??
#     return new_angles[0][1]
#
#
# def JARVIS_NEXT_CH_POINT(ptA, ptB, ptC):
#     # Angle between p[i], p[i - 1] and p[i], z
#     if len(ptC) == 1:
#         return ptC
#     return JARVIS_BINARY_SEARCH(ptA, ptB, ptC)


def main():
    listPts = readDataPts('A_3000.dat', 3000)  # File name, numPts given as example only
    print(giftwrap(listPts))  # You may replace these three print statements
    print(grahamscan(listPts))  # with any code for validating your outputs
    print(chain(listPts))


if __name__ == "__main__":
    main()
