"""Simple vector module consisting of vectors as objects and basic vector operations"""


class Vector:
    """A vector is a 3-dimensional array with direction (x,y,z) and length"""

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def get_length_of_vector(self):
        """returns the length of the vector"""
        return (self.x**2 + self.y**2 + self.z**2)**(1/2)

    def normalize_vector(self):
        """normalizes the vector if the vectors length is different from 0"""
        if self.get_length_of_vector() != 1 and self.get_length_of_vector() != 0:
            mag = self.get_length_of_vector()
            self.x, self.y, self.z = self.x / mag, self.y / mag, self.z / mag
        return


def dot_product(u1, u2):
    """returns the dot product of vectors u1 and u2"""
    return u1.x*u2.x+u1.y*u2.y+u1.z*u2.z


def reflected_ray(normal, incoming_ray):
    """returns a new vector that represents incoming_ray reflected against normal vector"""
    inc_dot_n = dot_product(incoming_ray, normal)
    n_scaled = scale_vector(normal, inc_dot_n*2)
    reflected_vector = sub_vectors(n_scaled, incoming_ray)
    return reflected_vector


def cross_product(u1, u2):
    """returns the cross product vector of vectors u1 and u2"""
    x = u1.y*u2.z-u1.z*u2.y
    y = -(u1.x*u2.z-u1.z*u2.x)
    z = u1.x*u2.y-u1.y*u2.x
    cross_vector = Vector(x, y, z)
    return cross_vector


def add_vectors(u1, u2):
    """returns vector u1+u2 where u1 and u2 are vectors"""
    x = u1.x+u2.x
    y = u1.y+u2.y
    z = u1.z+u2.z
    new_vector = Vector(x, y, z)
    return new_vector


def sub_vectors(u1, u2):  # u1-u2
    """returns vector u1-u2 where u1 and u2 are vectors"""
    x = u1.x - u2.x
    y = u1.y - u2.y
    z = u1.z - u2.z
    new_vector = Vector(x, y, z)
    return new_vector


def scale_vector(v, factor):
    """returns vector factor*v where factor is float and v is vector"""
    v.x = v.x * factor
    v.y = v.y * factor
    v.z = v.z * factor
    return v


def vector_mult(v1,v2):
    """returns vector (v1.x*v2.x, v1.y*v2.y, v1.z*v2.z) where v1 and v2 are vectors"""
    x = v1.x*v2.x
    y = v1.y*v2.y
    z = v1.z*v2.z
    vec = Vector(x,y,z)
    return vec

