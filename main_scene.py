"""Example code: how to use the Renderer"""


import Renderer  # including Tracer, Objects and Vectors
import Objects as obj
import Vectors


if __name__=="__main__":

    width, height = 1280, 720

    screen = Renderer.Screen(width, height)
    #screen.generate_light_source([3, -3, 3])
    #screen.generate_light_source([-3, -3, 3])
    screen.generate_light_source([20,5,2])

    #set background color
    #screen.bg_color = Vectors.Vector(17/255,29/255,29/255)
    screen.bg_color = Vectors.Vector(102/255,178/255,255/255)
    screen.bg_color = Vectors.Vector(0,0.2,1)


    # FLOOR CUBE
    floor_cube = obj.Cube(100, [0, 20,-51])
    floor_cube.ambient = Vectors.Vector(0.1, 0.1, 0.1)
    floor_cube.diffuse = Vectors.Vector(0.2, 0.2, 0.2)
    floor_cube.reflection = 0.45
    floor_cube.set_pattern_intervals()
    screen.generate_object(floor_cube)

    # CUBES
    cube1 = obj.Cube(0.45, [1, 0.73, -0.75])
    cube1.ambient = Vectors.Vector(0.8, 0.1, 0)
    cube1.diffuse = Vectors.Vector(0.7, 0.1, 0)
    cube1.reflection = 0.07
    screen.generate_object(cube1)

    cube2 = obj.Cube(5, [-7, 3, 1])
    cube2.ambient = Vectors.Vector(1, 0.05, 0.1)
    cube2.diffuse = Vectors.Vector(0.7, 0.1, 0.1)
    cube2.reflection = 0.75
    screen.generate_object(cube2)


    # SPHERES

    sphere1 = obj.Sphere(0.85, [-0.65, 1.55, 0.1])
    sphere1.ambient = Vectors.Vector(0.05, 0.05, 0.05)
    sphere1.diffuse = Vectors.Vector(0.85, 0.85, 0.85)
    sphere1.reflection = 0.86

    sphere2 = obj.Sphere(0.2, [-1, 0.25, -0.2])
    sphere2.ambient = Vectors.Vector(0.2, 0.1, 0)
    sphere2.diffuse = Vectors.Vector(0.7, 0.7, 0)
    sphere2.specular = Vectors.Vector(0.5, 0.5, 0.5)

    screen.generate_object(sphere2)

    screen.generate_object(sphere1)

    # PAPER PLANES FROM TRIANGLES
    c_all = Vectors.Vector(0.6, 0.77, 0)
    a1 = Vectors.Vector(c_all.x-0.3, c_all.y-0.4, c_all.z-0.1)
    b1 = Vectors.Vector(c_all.x-0.5, c_all.y-0.35, c_all.z-0.05)
    a2 = Vectors.Vector(c_all.x-0.05, c_all.y-0.33, c_all.z-0.17)
    b2 = Vectors.Vector(c_all.x-0.25, c_all.y-0.38, c_all.z-0.12)
    a3 = Vectors.Vector(c_all.x-0.29, c_all.y-0.4, c_all.z-0.2)
    tri1 = obj.Triangle(a1,b1, c_all)
    tri2 = obj.Triangle(a2, b2, c_all)
    tri3 = obj.Triangle(a1, c_all, a3)
    tri4 = obj.Triangle(a3, b2, c_all)
    screen.generate_object(tri1)
    screen.generate_object(tri2)
    screen.generate_object(tri3)
    screen.generate_object(tri4)

    c_all1 = Vectors.Vector(1.2, 0.89, 0.28)
    a11 = Vectors.Vector(c_all1.x-0.3, c_all1.y-0.4, c_all1.z-0.1)
    b11 = Vectors.Vector(c_all1.x-0.5, c_all1.y-0.35, c_all1.z-0.05)
    a21 = Vectors.Vector(c_all1.x-0.05, c_all1.y-0.33, c_all1.z-0.17)
    b21 = Vectors.Vector(c_all1.x-0.25, c_all1.y-0.38, c_all1.z-0.12)
    a31= Vectors.Vector(c_all1.x-0.29, c_all1.y-0.4, c_all1.z-0.2)
    tri11 = obj.Triangle(a11,b11, c_all1)
    tri11.ambient = Vectors.Vector(0.4, 0.0, 1)
    tri11.diffuse = Vectors.Vector(0.1, 0.0, 0.7)
    tri21 = obj.Triangle(a21, b21, c_all1)
    tri21.ambient = Vectors.Vector(0.4, 0.0, 1)
    tri21.diffuse = Vectors.Vector(0.1, 0.0, 0.7)
    tri31 = obj.Triangle(a11, c_all1, a31)
    tri31.ambient = Vectors.Vector(0.4, 0.0, 1)
    tri31.diffuse = Vectors.Vector(0.1, 0.0, 0.7)
    tri41 = obj.Triangle(a31, b21, c_all1)
    tri41.ambient = Vectors.Vector(0.4, 0.0, 1)
    tri41.diffuse = Vectors.Vector(0.1, 0.0, 0.7)
    screen.generate_object(tri11)
    screen.generate_object(tri21)
    screen.generate_object(tri31)
    screen.generate_object(tri41)


    # RENDER IMAGE

    screen.render_image()



