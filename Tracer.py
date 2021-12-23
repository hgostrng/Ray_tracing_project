"""The Tracer issues the ray tracing"""

import Objects as obj  # including Vectors
import Vectors
import Vectors as vec


def ray_trace(objects, maximum_light_bounces, lights, pixel, camera, bg_color):
    """returns the final pixel color as a vector (RGB)"""
    c_p_tot = vec.Vector(0, 0, 0)
    for light_source in lights:
        color = _trace(objects, maximum_light_bounces, light_source, pixel, camera, bg_color)
        c_p_tot = vec.add_vectors(c_p_tot, color)
    return c_p_tot


def _trace(objects, maximum_light_bounces, light, pixel, camera, bg_col):
    """ray_trace help function; returns the pixel color generated from one light source 'light'"""
    c_p = vec.Vector(0, 0, 0)

    start_pixel = pixel
    start_camera = camera

    scaler = 1
    current_reflected = None
    current_reflected_object = None

    for i in range(maximum_light_bounces):

        ref = obj.inf_appr
        point = None
        #view_vector = None
        current_object = None

        # find the closest object
        for object in objects:
            if current_reflected_object is object:
                continue
            temporary_point = obj.check_intersection_ray_object(object, start_pixel, start_camera)
            if temporary_point is not None:
                dist = temporary_point.get_length_of_vector()
                if dist < ref:
                    ref = dist
                    point = temporary_point
                    current_object = object
        if current_object is None:
            if i == 0:
                return bg_col
            else:
                return c_p
        else:

            view_vector = vec.sub_vectors(camera, point)

            shadowed = obj.is_object_shadowed(current_object, point, objects, light)

            normal_vector = current_object.get_normal_vector(point)
            normal_copy = vec.Vector(normal_vector.x, normal_vector.y, normal_vector.z)
            normal_copy.normalize_vector()

            if i == 0:
                incoming_ray = vec.sub_vectors(vec.Vector(0,0,0), point)

            else:
                incoming_ray = vec.sub_vectors(vec.Vector(0,0,0), current_reflected)

            incoming_copy = vec.Vector(incoming_ray.x, incoming_ray.y, incoming_ray.z)
            incoming_copy.normalize_vector()
            current_reflected_object = current_object

            reflected = vec.reflected_ray(normal_copy, incoming_copy)

            current_reflected = vec.Vector(reflected.x, reflected.y, reflected.z)

            if shadowed is False:
                light_vector = vec.sub_vectors(light, point)
                light_vector.normalize_vector()
                normal_vector.normalize_vector()
                view_vector.normalize_vector()
                reflection_light = vec.reflected_ray(vec.Vector(normal_vector.x, normal_vector.y, normal_vector.z),
                                                     vec.Vector(light_vector.x, light_vector.y, light_vector.z))
                reflection_light.normalize_vector()

                if type(current_object) is obj.Cube:
                    if current_object.pattern != []:
                        current_object.get_pattern_color(point)

                c_p = vec.add_vectors(c_p, vec.scale_vector(Illumination(current_object.ambient,
                                                                         current_object.diffuse,
                                                                         current_object.specular,
                                                    light.ambient, light.diffuse, light.specular,
                                                    light_vector, normal_vector, view_vector, reflection_light,
                                                                         current_object.shininess), scaler))

            #reflected = vec.Vector(reflected.x, reflected.y, reflected.z)
            scaler = scaler * current_object.reflection
            start_camera = point
            start_pixel = vec.add_vectors(point, reflected)

    return c_p


def Illumination(Ka, Kd, Ks, Ia, Id, Is, L, N, V, R, alpha):
    """Returns the illumination (as a vector # RGB) of a pixel using Phong shading model"""
    ka_ia = vec.vector_mult(Ka,Ia)
    kd_id_dot = vec.scale_vector(vec.vector_mult(Kd,Id),vec.dot_product(L,N))
    ks_is = vec.scale_vector(vec.vector_mult(Ks,Is), (vec.dot_product(R, V))**(alpha))
    v1 = vec.add_vectors(ka_ia, kd_id_dot)
    return vec.add_vectors(v1, ks_is)




