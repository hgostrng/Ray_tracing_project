"""The Renderer renders an image from a scene consisting of a light source and objects using
   ray tracing. The graphic module PIL is used to display the rendered image.
   The color model used to display the image is RGB, however, in the usage of the rendering
   module one has to use the scale RGB/255 (see example code in main_scene) .
   """


from PIL import Image  # requires PILLOW installed
import Tracer  # including Objects and Vectors
import Vectors as vec


class Screen:

    """A screen with attributes width (x-axis), height (z-axis), camera (vector), light(s) (vector(s)) and none or
       more objects"""

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.__pixels = []
        self.lights = []
        self.objects = []
        self.bg_color = vec.Vector(0, 0, 0)  # background color, default = black
        self.camera = vec.Vector(0, -1, 0)  # default

        self.__generate_pixels()

    def __normalize_scale(self, realscale, minim, maxim):
        """Private method that sets screen scale to -minim < axis < maxim"""
        realsteps = realscale
        newsteps = maxim - minim
        stepsize = newsteps / realsteps
        newscale = [minim]
        appendval = minim
        while appendval <= maxim:
            appendval += stepsize
            # print('hej')
            newscale.append(appendval)
        return newscale

    def __generate_pixels(self):

        ratio = self.width/self.height

        pixel_scale_x = self.__normalize_scale(self.width, -ratio, ratio)
        pixel_scale_z = self.__normalize_scale(self.height, -1, 1)

        #pixels = []  # inner lists represents columns
        for i in range(self.width):
            self.__pixels.append([])

        for i in range(self.width):  # i are rows j are columns
            for j in range(self.height):
                pixel = vec.Vector(pixel_scale_x[i], 0,  pixel_scale_z[j])
                self.__pixels[i].append(pixel)
        return


    def generate_light_source(self, placement):
        """Append light source to lights"""
        light = vec.Vector(placement[0], placement[1], placement[2])
        light.ambient = vec.Vector(1, 1, 1)
        light.diffuse = vec.Vector(1, 1, 1)
        light.specular = vec.Vector(1, 1, 1)
        self.lights.append(light)
        return

    def generate_object(self, object):
        """Append object to objects"""
        self.objects.append(object)
        return

    def render_image(self):
        """Render and display screen"""
        for pixelrow in self.__pixels:
            for pixel in pixelrow:
                color = Tracer.ray_trace(self.objects, 3, self.lights, pixel, self.camera, self.bg_color)

                if color.x < 0:
                    red = 0
                elif color.x > 1:
                    red = 1
                else:
                    red = color.x
                if color.y < 0:
                    green = 0
                elif color.y > 1:
                    green = 1
                else:
                    green = color.y
                if color.z < 0:
                    blue = 0
                elif color.z > 1:
                    blue = 1
                else:
                    blue = color.z

                pixel.color = [255 * red, 255 * green, 255 * blue]

        img = Image.new('RGB', (self.width, self.height))
        for i in range(self.width):
            for j in range(self.height):
                colors = self.__pixels[i][j].color
                rgb = (int(colors[0]), int(colors[1]), int(colors[2]))
                img.putpixel((i, self.height - 1 - j), rgb)
        img.show()



