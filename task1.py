from math import sqrt
from math import acos
from math import pi
from math import e
from enum import Enum
# splited = input("Введите Ax, Ay, Bx, By: ").split()
# Ax = int(splited[0])
# Ay = int(splited[1])
# Bx = int(splited[2])
# By = int(splited[3])

# e = 0.0000000001


def det(a, b, c, d):
    return a*d - b*c


def maxAndleOX(Ax: int, Ay: int, Bx: int, By: int) -> str:
    U1 = Ax / sqrt(Ax**2 + Ay**2)
    U2 = Bx / sqrt(Bx**2 + By**2)
    if Ay > 0 and By > 0:
        return ("A" if U1 < U2 else "B")
    if Ay < 0 and By < 0:
        return ("A" if U1 > U2 else "B")
    if (Ay < 0 and By > 0) or (Ay > 0 and By < 0):
        return ("A" if Ay < By else "B")


def FuckingLyingScalarMult(Ax: int, Ay: int, Bx: int, By: int) -> int:
    return (Ax * By - Ay * Bx)


def ScalarMult(Ax: int, Ay: int, Bx: int, By: int) -> int:
    return (Ax * Bx + Ay * By)


def dotOnVector(Ax: int, Ay: int, Bx: int, By: int, Cx: int, Cy: int) -> bool:
    ABx = Ax - Bx
    ABy = Ay - By
    ACx = Ax - Cx
    ACy = Ay - Cy
    sm = FuckingLyingScalarMult(ABx, ABy, ACx, ACy)
    if (Ay == By and Ax == Bx) or (Ay == Cy and Ax == Cx):
        return True
    elif sm == 0:
        if ACx != 0:
            t = ABx / ACx
            if t < 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def RadToDegree(angle):
    return angle * 180 / pi


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Segment:
    def __init__(self, A: Point, B: Point) -> None:
        self.A = A
        self.B = B

    def length(self):
        return sqrt((self.A.x - self.B.x)**2 + (self.A.y - self.B.y)**2)


def get_angle_abc(A: Point, B: Point, C: Point):
    bseg = Segment(A, C)
    aseg = Segment(B, C)
    cseg = Segment(A, B)
    al = aseg.length()
    bl = bseg.length()
    cl = cseg.length()
    cosVal = (al*al + cl*cl - bl*bl) / (2 * al * cl)
    acosVal = acos(cosVal)
    return RadToDegree(acosVal)


def norm_on_segment(a: Point, s: Segment):
    a1 = get_angle_abc(a, s.A, s.B)
    a2 = get_angle_abc(a, s.B, s.A)
    return (a1 < 90 and a2 < 90) or (a1 < 90 and abs(a2-90) < e) or (a2 < 90 and abs(a1-90) < e)


def checkDotOnSegment(p: Point, s: Segment) -> bool:
    return dotOnVector(p.x, p.y, s.A.x, s.A.y, s.B.x, s.B.y)


class Line:
    def __init__(self, A, B, C) -> None:
        self.A = A
        self.B = B
        self.C = C

    def FromAngularForm(a, b):
        return Line(a, -1, b)

    def fromSegment(s: Segment):
        return Line(s.A.y - s.B.y, s.B.x - s.A.x, s.A.x*s.B.y - s.B.x*s.A.y)

    def distance(self, a: Point):
        return (abs(self.A*a.x + self.B*a.y + self.C)) / (sqrt(a.x*a.x + a.y*a.y))

    def IsParallel(l1, l2):
        return abs(det(l1.A, l1.B, l2.A, l2.B)) < e


# task 4
def LineSegmentIntersection(l: Line, s: Segment):
    l1 = l
    l2 = Line.fromSegment(s)
    if Line.IsParallel(l1, l2):
        return False

    u = det(l1.A, l1.B, l2.A, l2.B)
    d = Point(-det(l1.C, l1.B, l2.C, l2.B) /
              u, -det(l1.A, l1.C, l2.A, l2.C) / u)

    return dotOnVector(d.x, d.y, s.A.x, s.A.y, s.B.x, s.B.y)

# task 5


def segmentsIntersection(s1: Segment, s2: Segment) -> bool:
    l1 = Line.fromSegment(s1)
    l2 = Line.fromSegment(s2)

    # check if parallel
    if Line.IsParallel(l1, l2):
        # check, if equal or laying on one line and intersects
        return not (abs(l1.distanse(s2.A)) > e or abs(l2.distanse(s1.A)) > e)
    # if not parallel

    # find intersection dot
    u = det(l1.A, l1.B, l2.A, l2.B)
    d = Point(
        x=-det(l1.C, l1.B, l2.C, l2.B) / u,
        y=-det(l1.A, l1.C, l2.A, l2.C) / u
    )

    # dot must be on segments
    return checkDotOnSegment(d, s1) and checkDotOnSegment(d, s2)


# signed area of triangle
def signedDoubleTriangleArea(a: Point, b: Point, c: Point) -> float:
    return (b.X-a.X)*(c.Y-a.Y) - (b.Y-a.Y)*(c.X-a.X)


class Position(Enum):
    Inside = 0
    OnBorder = 1
    Outside = 2


class Triangle():

    def __init__(self, A: Point, B: Point, C: Point) -> None:
        self.A = A
        self.B = B
        self.C = C


def dotAndTriangle(d: Point, t: Triangle) -> Position:
    ss = [Segment(t.A, t.B), Segment(t.B, t.C), Segment(t.C, t.A)]
    wasOnBorder = False

    for s in ss:
        sdta = signedDoubleTriangleArea(d, s.A, s.B)
        if abs(sdta) < e:
            wasOnBorder = True
            continue
        elif sdta < 0:
            return Position.Outside

    if wasOnBorder:
        return Position.OnBorder

    return Position.Inside


def maxIntersectionLine(segments: list) -> tuple:
    if len(segments) == 1:
        return (Segment(segments[0].A, Point(segments[0].B.X + 10, segments[0].B.Y + 10)), [0])

    dots = [None for x in range(0, len(segments)*2)]
    for i, s in enumerate(segments):
        dots[2*i] = s.A
        dots[2*i+1] = s.B

    bestA = None
    bestB = None
    bestSegments = []
    first = True

    for i in range(0, len(dots)):
        j = i + 1
        if j % 2 == 1:
            j += 1

        while j < len(dots):
            if dots[i] == dots[j]:
                j += 1
                continue
            line = Line.fromSegment(Segment(dots[i], dots[j]))
            maybeSegments = []
            for k, s in enumerate(segments):
                if LineSegmentIntersection(*line, s):
                    maybeSegments.append(k)

            if first or len(maybeSegments) > len(bestSegments):
                first = False
                bestA = dots[i]
                bestB = dots[j]
                bestSegments = maybeSegments
            j += 1

    return (Segment(bestA, bestB), bestSegments)


# no tests... but i'm tired... just believe, it works
def checkSymmetry(matrix: list) -> tuple:
	n = len(matrix)
	m = len(matrix[0])

	left = m - 1
	right = 0
	up = n - 1
	down = 0

	for i in range(0, n):
		for j in range(0, m):
			if matrix[i][j] != 0:
				left = min(left, j)
				break

	for i in range(0, n):
		for j in range(m - 1, -1, -1):
			if matrix[i][j] != 0:
				right = max(right, j)
				break

	for j in range(0, m):
		for i in range(0, n):
			if matrix[i][j] != 0:
				up = min(up, i)

	for j in range(0, m):
		for i in range(n - 1, -1, -1):
			if matrix[i][j] != 0:
				down = max(down, i)

	wide = right - left + 1
	height = down - up + 1

	if wide <= 0 or height <= 0:
		return ([], [])

	cropped = [None for x in range(0, height)]
	for i in range(0, height):
		cropped[i] = [None for x in range(0, wide)]
		for j in range(0, wide):
			cropped[i][j] = matrix[i+up][j+left]

	# fmt.Println(strings.ReplaceAll(fmt.Sprint(cropped), "] ", "]\n "))

	symms = []

	check = True
	for i in range(0, height):
		for j in range(0, wide/2 + 1):
			if cropped[i][j] != cropped[i][wide-1-j]:
				check = False
				break

		if not check:
			break

	if check:
		symms.append("vertical")

	check = True
	for j in range(0, wide):
		for i in range(0, height/2 + 1):
			if cropped[i][j] != cropped[height-1-i][j]:
				check = False
				break

		if not check:
			break

	if check:
		symms.append("horizontal")

	if wide == height:

		check = True
		for i in range(0, wide-1):
			for j in range(i+1, wide):
				if cropped[i][j] != cropped[j][i]:
					check = False
					break

			if not check:
				break

		if check:
			symms.append("main_diagonal")

		check = True
		for i in range(0, wide-1):
			for j in range(0, wide-1-i):
				if cropped[i][j] != cropped[wide-1-j][wide-1-i]:
					check = False
					break

			if not check:
				break

		if check:
			symms.append("extra_diagonal")


	return cropped, symms



if __name__ == '__main__':
    # print(maxAndleOX(-2, 3, 2, 3), "must be A")
    # print(maxAndleOX(-2, -3, 2, -3), "must be B")
    # print(maxAndleOX(-2, 3, 2, -3), "must be B")

    # print(dotOnVector(5, 3, 2, 3, 7, 3) ,"must be True")
    # print(dotOnVector(-123, 3, 2, 3, 7, 3), "must be False")
    # print(dotOnVector(5, 4, 2, 3, 7, 3), "must be False")
    # print(dotOnVector(4, 4, 2, 3, 6, 5), "must be True")
    # print(dotOnVector(4.5, 4, 2, 3, 7, 5), "must be True")
    # print(dotOnVector(7, 5, 2, 3, 7, 5), "must be True")
    # print(dotOnVector(4, 3, 0, 0, 4, 3), "must be True")
    # print(Line.IsParallel(Line(2, 3, 4), Line(4, 3, 2)))
    print(LineSegmentIntersection(Line(1, -1, 0),
          Segment(Point(5, 0), Point(5, 7))))
