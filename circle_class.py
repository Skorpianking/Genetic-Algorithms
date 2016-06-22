# Basic circle class... well ok, it does some cool stuff like returning the area
# where two circles intersect (only 2 circles).  It will also allow one to test
# if two circles actually intersect, or if one is contained by the other.

import math

class Circle:
    radius = 0.00
    x = 0
    y = 0

    # original constructor
    def __init__(self, x, y, rad):
        self.radius = rad
        self.x = x
        self.y = y

    # helps print these objects
    def __repr__(self):
        return 'X: ' + str(self.x) + ' Y: ' + str(self.y) + ' Radius: ' + str(self.radius)

    # Test if two circles intersect
    def intersects(self, circ):
        distX = self.x - circ.x
        distY = self.y - circ.y
        dist = pow(pow(distX,2) + pow(distY,2), .5) # Good ol' Pythagorus
        
        sumRadii = self.radius + circ.radius
        if(dist <= (sumRadii) or dist <= abs(sumRadii)):
            return True
        return False

    # Tests if one circle is inside another
    def containsCircle(self, circ):
        distX = self.x - circ.x
        distY = self.y - circ.y
        dist = pow(pow(distX,2) + pow(distY,2), .5)
        diffRadii = self.radius - circ.radius
        if dist <= abs(diffRadii):
            return True
        return False

    # Returns the circle's area
    def area(self):
        return self.radius*self.radius*math.pi

    def setRadius(self, radius):
        self.radius = radius

    def getRadius(self):
        return self.radius

    def setOrigin(self, x,y):
        self.x = x
        self.y = y

    # Returns the area of the intersection. Based on https://www.youtube.com/watch?v=uT480Q31FkI&feature=youtu.be
    # tutorial for finding the area of intersect for two circles.  This function
    # needs work: it ends up busting the bounds of arcsin and sin at times which
    # I don't think it true (as in, it shouldn't happen)
    def lensArea(self,circ):
        # First test if one is inside the other
        if self.containsCircle(circ) == True:
            return circ.area()
        if circ.containsCircle(self) == True:
            return self.area()
        # Second test if their is an intersection, if not, return 0
        if self.intersects(circ) == False:
            return 0
        # 1. Calculate the distance between the centers
        distX = abs(self.x - circ.x)
        distY = abs(self.y - circ.y)
        dist = pow(pow(distX,2) + pow(distY,2), .5)
        #print(dist)
        # 2. Derive angles theta and alpha. Angles formed by radii at points of itersection measured at center of circle
        theta = circ.radius/dist
        #print(theta)
        alpha = self.radius/dist
        #print(alpha)                
        # 3. Get areas of each lens regions
        lensOne = (1/2)*pow(circ.radius,2)*(2*math.asin(alpha)-math.sin(2*math.asin(alpha)))
        lensTwo = (1/2)*pow(self.radius,2)*(2*math.asin(theta)-math.sin(2*math.asin(theta)))

        # Add areas together
        return lensOne + lensTwo

#def main():
#    c = Circle(0,0,3)
#    d = Circle(5,0,4)
#    print(c.lensArea(d))


#main()
