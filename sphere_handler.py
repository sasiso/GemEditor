import vtk

class SphereHandler:
    def __init__(self, stl_actor):
        self.stl_actor = stl_actor
        self.sphere_actor = None
        self.dimensions = None

    def calculate_shape_dimensions(self):
        if not self.stl_actor:
            return None

        bounds = self.stl_actor.GetBounds()
        width = bounds[1] - bounds[0]
        height = bounds[3] - bounds[2]
        length = bounds[5] - bounds[4]
        diameter = min(width, height, length)

        self.dimensions = diameter

    def create_shape_actor(self):
        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(self.dimensions / 2.0)

        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

        self.sphere_actor = vtk.vtkActor()
        self.sphere_actor.SetMapper(sphere_mapper)

    def find_valid_shape_position(self):
        if not self.stl_actor:
            return False

        center = self.stl_actor.GetCenter()

        # Create a bounding sphere for the collision detection
        diameter = self.sphere_actor.GetMapper().GetInput().GetLength()
        bounding_sphere = vtk.vtkSphere()
        bounding_sphere.SetCenter(center)
        bounding_sphere.SetRadius(diameter / 2.0)

        # Use vtkCollisionDetectionFilter for collision detection
        collision_filter = vtk.vtkCollisionDetectionFilter()
        collision_filter.SetInputData(0, self.stl_actor.GetMapper().GetInput())
        collision_filter.SetCollisionModeToAllContacts()
        #collision_filter.SetBoundingObject(bounding_sphere)
        collision_filter.GenerateScalarsOn()
        collision_filter.Update()

        # Check if there are any collisions
        num_collisions = collision_filter.GetNumberOfContacts()
        return num_collisions == 0
