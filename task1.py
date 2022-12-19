from math import sqrt
from math import acos
from math import pi
# splited = input("Введите Ax, Ay, Bx, By: ").split()
# Ax = int(splited[0])
# Ay = int(splited[1])
# Bx = int(splited[2])
# By = int(splited[3])

e = 0.0000000001

def det(a, b, c, d):
	return a*d - b*c

def maxAndleOX(Ax: int, Ay: int, Bx: int, By: int) -> str:
	U1 = Ax / sqrt(Ax**2 + Ay**2)
	U2 = Bx / sqrt(Bx**2 + By**2)
	if Ay > 0 and By > 0:
		return("A" if U1 < U2 else "B")
	if Ay < 0 and By < 0:
		return("A" if U1 > U2 else "B")
	if (Ay < 0 and By > 0) or (Ay > 0 and By < 0):
		return("A" if Ay < By else "B") 


def FuckingLyingScalarMult(Ax: int, Ay: int, Bx: int, By: int) -> int:
	return(Ax * By - Ay * Bx)


def ScalarMult(Ax: int, Ay: int, Bx: int, By: int) -> int:
	return(Ax * Bx + Ay * By)


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


def LineSegmentIntersection(l: Line, s: Segment):
	l1 = l
	l2 = Line.fromSegment(s)
	if Line.IsParallel(l1, l2):
		return False

	u = det(l1.A, l1.B, l2.A, l2.B)
	d = Point(-det(l1.C, l1.B, l2.C, l2.B) / u, -det(l1.A, l1.C, l2.A, l2.C) / u)
		
	return dotOnVector(d.x, d.y, s.A.x, s.A.y, s.B.x, s.B.y)





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
	print(LineSegmentIntersection(Line(1, -1, 0), Segment(Point(5, 0), Point(5, 7))))