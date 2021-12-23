"""Object is an object of type Sphere, Cube, Triangle or surface (too be implemented) etc."""

from math import cos, sin, acos, atan2
import Vectors as vec

inf_appr = 1000000
zero_appr = 0.00001


class Sphere:
    """a sphere with radius of type float and center_coordinates [x,y,z]"""

    def __init__(self, radius, center_coordinates):
        self.r = radius
        self.center = center_coordinates
        # Color properties
        self.ambient = vec.Vector(0.1, 0, 0)  # default
        self.diffuse = vec.Vector(0.7, 0, 0)  # default
        self.specular = vec.Vector(1, 1, 1)   # default
        self.shininess = 100              # default
        self.reflection = 0.5             # default

    def get_normal_vector(self, surface_point):
        """returns the normal vector (outward direction) of the sphere at surface_point"""
        x, y, z = -(self.center[0]-surface_point.x), -(self.center[1]-surface_point.y), -(self.center[2]-surface_point.z)
        r = (x ** 2 + y ** 2 + z ** 2)**(1/2)  # SHOULD EQUAL self.r !!!
        theta = acos(z / r)
        phi = atan2(y, x)
        jac = r ** 2 * sin(theta)
        vec_x = jac * sin(theta) * cos(phi)
        vec_y = jac * sin(theta) * sin(phi)
        vec_z = jac * cos(theta)
        n_vector = vec.Vector(vec_x, vec_y, vec_z)
        return n_vector

class Cube:

    def __init__(self, side_length, center_coordinates):
        self.a = side_length/2
        self.x = center_coordinates[0]
        self.y = center_coordinates[1]
        self.z = center_coordinates[2]
        self.center =center_coordinates
        # Color properties
        self.ambient = vec.Vector(0.1, 0, 0)
        self.diffuse = vec.Vector(0.7, 0, 0)
        self.specular = vec.Vector(1, 1, 1)
        self.shininess = 100
        self.reflection = 0.5
        self.pattern = []

    def get_normal_vector(self, surface_point):
        center_vec = vec.Vector(self.x, self.y, self.z)
        diff_vec = vec.sub_vectors(surface_point, center_vec)
        dx = diff_vec.x
        dy = diff_vec.y
        dz = diff_vec.z

        if abs(dx) == max(abs(dx), abs(dy), abs(dz)):
            if dx < 0:
                return vec.Vector(-1, 0, 0)
            else:
                return vec.Vector(1,0,0)

        if abs(dy) == max(abs(dx), abs(dy), abs(dz)):
            if dy < 0:
                return vec.Vector(0, -1, 0)
            else:
                return vec.Vector(0,1,0)

        if abs(dz) == max(abs(dx), abs(dy), abs(dz)):
            if dz < 0:
                return vec.Vector(0, 0, -1)
            else:
                return vec.Vector(0,0,1)

    def set_pattern_intervals(self):
        scale = 0.5
        interval = self.a
        xstart = self.x-self.a
        ystart = self.y-self.a
        for i in range(1,int(2*interval/scale+1)):  # x
            for j in range(1,int(2*interval/scale+1)):  # y
                if (i+j)//2 == (i+j)/2:  # even sum
                    self.pattern.append([xstart, xstart+scale, ystart, ystart+scale])
                ystart += scale
            xstart += scale
            ystart = self.y-self.a
        return

    def get_pattern_color(self, point):
        px = point.x
        py = point.y
        for interval in self.pattern:
            if interval[0] <= px <= interval[1] and interval[2] <= py <= interval[3]:
                self.ambient = vec.Vector(0, 0.4, 0.2)
                self.diffuse = vec.Vector(0, 0.4, 0.2)
                return
            else:
                continue
        self.ambient = vec.Vector(0.8, 0.8, 0.8)
        self.diffuse = vec.Vector(0.8, 0.8, 0.8)
        return self


class Triangle:
    """a triangle has 3 points in space, each point is of type vector"""

    def __init__(self, point_a, point_b, point_c):
        self.a = point_a  # (x0, y0, z0)
        self.b = point_b  # (x1, y1, z1)
        self.c = point_c  # (x2, y2, z2)
        # Color properties
        self.ambient = vec.Vector(0.1, 0, 0)  # default
        self.diffuse = vec.Vector(0.7, 0, 0)  # default
        self.specular = vec.Vector(1, 1, 1)  # default
        self.shininess = 100  # default
        self.reflection = 0.1  # default
        self.normal = None

    def get_normal_vector(self, point):  # point a is closest to screen
        """returns normal vector of triangle"""
        if self.normal is None:
            ac = vec.sub_vectors(self.c, self.a)
            ab = vec.sub_vectors(self.b, self.a)
            norm = vec.cross_product(ac, ab)
            self.normal = norm
            return norm
        else:
            return self.normal

    #def get_triangle_are(self):
     #   ab = vec.sub_vectors(self.b, self.c)
      #  ac = vec.sub_vectors(self.c, self.b)

       # e = vec.dot_product(ab, ac)

        #d = (ab.get_length_of_vector()**2-e**2)**(1/2)

        #return (ac.get_length_of_vector() * d)/2


def check_cube_intersection_plane(direction_string, camera, direction_vector, cube):

    if direction_string == 'bottom':
        if direction_vector.z == 0:
            t = (cube.z - cube.a - camera.z)/zero_appr
        else:
            t = (cube.z - cube.a - camera.z)/direction_vector.z

        alpha = camera.x + direction_vector.x * t - cube.x

        beta = camera.y + direction_vector.y * t - cube.y

    if direction_string == 'top':
        if direction_vector.z == 0:
            t = (cube.z + cube.a - camera.z) / zero_appr
        else:
            t = (cube.z + cube.a - camera.z) / direction_vector.z

        alpha = camera.x + direction_vector.x * t - cube.x

        beta = camera.y + direction_vector.y * t - cube.y

    if direction_string == 'front':
        if direction_vector.y == 0:
            t = (cube.y - cube.a - camera.y) / zero_appr
        else:
            t = (cube.y - cube.a - camera.y) / direction_vector.y

        alpha = camera.x + direction_vector.x * t - cube.x

        beta = camera.z + direction_vector.z * t - cube.z

    if direction_string == 'back':
        if direction_vector.y == 0:
            t = (cube.y + cube.a - camera.y) / zero_appr
        else:
            t = (cube.y + cube.a - camera.y) / direction_vector.y

        alpha = camera.x + direction_vector.x * t - cube.x

        beta = camera.z + direction_vector.z * t - cube.z

    if direction_string == 'right':
        if direction_vector.x == 0:
            t = (cube.x + cube.a - camera.x) / zero_appr
        else:
            t = (cube.x + cube.a - camera.x) / direction_vector.x

        alpha = camera.y + direction_vector.y * t - cube.y

        beta = camera.z + direction_vector.z * t - cube.z

    if direction_string == 'left':
        if direction_vector.x == 0:
            t = (cube.x - cube.a - camera.x) / zero_appr
        else:
            t = (cube.x - cube.a - camera.x) / direction_vector.x

        alpha = camera.y + direction_vector.y * t - cube.y

        beta = camera.z + direction_vector.z * t - cube.z

    if isinstance(alpha, complex) is False and isinstance(beta, complex) is False and \
        -cube.a <= alpha <= cube.a and -cube.a <= beta <= cube.a and t>0:
            return (True, t)
    else:
        return (None, None)


def check_intersection_ray_object(object, dir_point1, dir_point2):
    """returns the nearest (positive solution) intersection point between ray (dir_point1 - dir_point2) and
       object where dir_point1 and dir_point2 are vectors.
       If no intersection is detected - the functions returns None"""

    direction_vector = vec.sub_vectors(dir_point1, dir_point2)
    direction_vector.normalize_vector()

    solution_one, solution_two = None, None

    if type(object) is Sphere:

        center_vector = vec.Vector(object.center[0], object.center[1], object.center[2])

        dir2_min_sphere_center = vec.sub_vectors(dir_point2, center_vector)

        t_1 = 2*vec.dot_product(direction_vector, dir2_min_sphere_center)
        t_0 = vec.dot_product(dir2_min_sphere_center, dir2_min_sphere_center) - object.r**2

        if (t_1 ** 2)/4 - t_0 <= 0:  # complex solution or only one real solution
            return None
        else:
            # solution_one = -(t_1 / 2) + ((t_1 ** 2) / 4 - t_0) ** (1 / 2)
            solution_two = -(t_1 / 2) - ((t_1 ** 2) / 4 - t_0) ** (1 / 2)
            if solution_two < 0:
                return None

    if type(object) is Triangle:

        a = object.a
        v = vec.sub_vectors(object.b, a)
        u = vec.sub_vectors(object.c, a)

        ax, ay, az = a.x, a.y, a.z
        vx, vy, vz = v.x, v.y, v.z
        ux, uy, uz = u.x, u.y, u.z

        cx, cy, cz = dir_point2.x, dir_point2.y, dir_point2.z

        dx, dy, dz = direction_vector.x, direction_vector.y, direction_vector.z

        psi_one = cx-ax
        psi_two = cy*vx-ay*vx-psi_one*vy

        phi = dy*vx-dx*vy
        theta = uy*vx-ux*vy

        A = az + (psi_one*vz)/vx - (psi_two*ux*vz)/(theta*vx) + (psi_two*uz)/theta - cz
        B = dz - (phi*uz)/theta - (dx*vz)/vx + (phi*ux*vz)/(theta*vx)

        t = A/B

        w2 = (phi*t+psi_two)/(theta)
        w1 = (dx*t-(phi*ux*t)/theta-(psi_two*ux)/theta+psi_one)/vx
        if 0 < w1 < 1 and 0 < w2 < 1 and 0<(w1+w2)<1 and t>0:
            solution_two = t
        else:
            return None

    if type(object) is Cube:
        counter = 0
        solution_first = None
        solution_scnd = None
        shortest_sol = None
        for dir in ['bottom', 'top', 'front', 'back', 'right', 'left']:
            result = check_cube_intersection_plane(dir, dir_point2, direction_vector, object)
            if result[0] is True:
                counter += 1
                if counter == 1:
                    solution_first = result[1]
                if counter == 2:
                    solution_scnd = result[1]
                    shortest_sol = min(solution_first, solution_scnd)

        if shortest_sol is None:
            return None
        else:
            solution_two = shortest_sol

    point = vec.add_vectors(dir_point2, vec.scale_vector(direction_vector, solution_two))
    return point




def is_object_shadowed(object, object_surface_point, all_objects, light):
    """returns True if object_surface_point is shadowed and False if not.
       returns 0 if light doesn't strike object at all"""
    light_point_on_object = check_intersection_ray_object(object, object_surface_point, light)
    TOL = 0.0001
    if light_point_on_object is None:
        return 0
    else:

        if vec.sub_vectors(object_surface_point, light_point_on_object).get_length_of_vector() < TOL:
            distance_object_to_light = vec.sub_vectors(light, object_surface_point).get_length_of_vector()
            for sub_object in all_objects:
                if sub_object is object:
                    continue
                else:
                    light_point_on_sub_object = check_intersection_ray_object(sub_object, light, object_surface_point)
                    if light_point_on_sub_object is not None:
                        dist = vec.sub_vectors(light, light_point_on_sub_object).get_length_of_vector()
                        if dist < distance_object_to_light:
                            return True
            return False
        return True


