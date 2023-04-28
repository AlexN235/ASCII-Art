# ASCII-Art
Converts shapes into images represented by ASCII art.

To run, use the command:

python ascii_displayer.py *shape*

where *shape* is either "cube" or "donut".

## ASCIIConverter
Takes an image or 2D array and converts it into an ascii image.

### convert()
Converts the original image/2D array into an ascii image

### get_ascii()
Returns the ascii representation of the image


## ASCIIDisplayer
Displays our 2D image or animated image.

### display()
Displays the ascii art of the current shape

### displayGIF()
Displays a rotating shape in ascii art form


## ShapeDrawer
Draw different shapes: cube, sphere, cylinder etc. Represents these shapes in a 3D numpy matrix. Rotate shapes on different axis.

### rotate()
Rotates along either x, y, z axis. Input is a string that is either 'x', 'y', 'z' for each respective axis.

### getShape()
Returns the represented shape on the 3D plane.

### project()
Returns a 2D array that is a projection of the 3D model onto one of the planes.


## Shape
Class representing the different shapes that will be drawn. The shape is represented by a smaller amount of points that draws a mesh of the shape. Transform the shapes through translations and rotations. All points are then generated during output in the ShapeDrawer class.

### rotate()
Rotates the shape around the center of the shape.

### generateShape()
Takes the mesh of the shape and draws the squares polygons for the cube.

### drawShape() (i.e drawCube, drawDonut)
Initialize shape by generating the mesh for the shape.

