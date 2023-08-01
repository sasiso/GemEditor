import vtk

class CubeHandler:
    def __init__(self, stl_actor):
        self.stl_actor = stl_actor
        self.shape_actor = None
        self.dimensions = None
        self.centre = None
        self.obb_tree = None

    def calculate_shape_dimensions(self):
        if not self.stl_actor:
            return None

        bounds = self.stl_actor.GetBounds()
        width = bounds[1] - bounds[0]
        height = bounds[3] - bounds[2]
        length = bounds[5] - bounds[4]
        side_length = min(width, height, length)

        self.dimensions =  side_length, side_length, side_length

    def create_shape_actor(self,):
        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(self.dimensions[0])
        cube_source.SetYLength(self.dimensions[1])
        cube_source.SetZLength(self.dimensions[2])

        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube_source.GetOutputPort())

        self.shape_actor = vtk.vtkActor()
        self.shape_actor.SetMapper(cube_mapper)

    def find_valid_shape_position(self):
        if not self.stl_actor:
            return False
        width, height, length = self.dimensions
        # Create the cube for collision detection
        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(width)
        cube_source.SetYLength(height)
        cube_source.SetZLength(length)

        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube_source.GetOutputPort())

        
        
        center = self.centre
        # Set the position of the cube for collision detection
        self.shape_actor.SetPosition(center[0] - width / 2, center[1] - height / 2, center[2] - length / 2)

        # Create the collision detection filter
        collision_filter = vtk.vtkCollisionDetectionFilter()
        t1 = self.stl_actor.GetMapper().GetInput()
        t2 = self.shape_actor.GetMapper().GetInput()
        
        collision_filter.SetInputData(0, self.stl_actor.GetMapper().GetInput())
        collision_filter.SetInputData(1, self.shape_actor.GetMapper().GetInput())
        collision_filter.SetCollisionModeToAllContacts()
        collision_filter.GenerateScalarsOn()
        collision_filter.Update()

        if self.obb_tree:
            collision.SetBoxTree(self.obb_tree)
        

        # Check if there are any collisions
        num_collisions = collision_filter.GetNumberOfContacts()
        return num_collisions == 0
