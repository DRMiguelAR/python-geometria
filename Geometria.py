from dataclasses import dataclass
from typing import NewType
from math import cos, sin, pi
import math

Punto= NewType("Punto", object)
Vector= NewType("Vector", object)

def iguales(a: float, b: float, eps=10**-3) -> bool:
    if type(a)==Vector and type(b)==Vector:
        return a==b
    else:
        #return math.isclose(a,b, abs_tol=eps)
        return abs(a- b)< eps

class Vector:
    def __len__(self):
        return len(self.coords)
    def __iter__(self):
        return iter(self.coords)
    def __repr__(self):
        return str(self.coords)
    def __init__(self, *args, p1=0, p2=0):
        if len(args)==2 and type(args[0]) == type(args[1]) == Punto:
            p1= args[0]
            p2= args[1]
            self.coords= (p2.x-p1.x, p2.y-p1.y)
            self.x, self.y= self.coords
        else:
            self.coords= args
    def __eq__(self, other):
        if len(self)==len(other):
            return all( [iguales(a,b) for a,b in zip(self,other)] )
        else:
            raise ArithmeticError   
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return sum([hash(coord)*(10**6)**i for i,coord in enumerate(self.coords)])
    
class Punto(Vector):
    def __init__(self, *args):
        self.x, self.y= args[0], args[1]
        super().__init__(*args)

    def distancia(p1: Punto, p2: Punto) -> float: 
        """Regresa la distancia entre los puntos"""
        dx= p1.x - p2.x
        dy= p1.y - p2.y
        return math.hypot(dx, dy) # Saca la hipotenusa dados los catetos

    def transladar(self, dx: float, dy: float) -> Punto:
        self.x+= dx
        self.y+= dy
        return self

    def rotar(self, theta) -> Punto: 
        """Rota el punto theta grados"""
        theta= theta*pi/180
        x= self.x
        y= self.y
        self.x= x*cos(theta)-y*sin(theta)
        self.y= x*sin(theta)+y*cos(theta)
        return self

    
class Linea(Vector):
    def __init__(self, p1: Punto= None, p2: Punto= None, A=1, B=0, C=0):
        if p1 and p2:
            self.A= p1.y- p2.y
            self.B= p2.x- p1.x
            self.C= p2.y* p1.x - p1.y* p2.x
        else:
            self.A= A
            self.B= B
            self.C= C
        super().__init__(self.A,self.B, self.C)
    def __repr__(self):
        return f"A:{self.A}, B:{self.B}, C:{self.C}"
    
    def simplificar(self):
        A, B, C= self.A, self.B, self.C
        if A:
            A,B,C= 1, B/A, C/A
        else:
            B,C= 1, C/B
        return A, B, C
    
    def __eq__(self, other): 
        v1= Vector(*self.simplificar())
        v2= Vector(*other.simplificar())
        return v1==v2
        
@dataclass
class Segmento:
    p1: Punto
    p2: Punto
    def __hash__(self):
        return hash(self.p1)+hash(self.p2)