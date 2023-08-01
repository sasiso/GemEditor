import vtk

class GemModel:
    def __init__(self):
        self.stlActor = None
        self.cubeActor = None

    def loadSTLModel(self, filepath):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filepath)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        self.stlActor = vtk.vtkActor()
        self.stlActor.SetMapper(mapper)

        return self.stlActor

    # Add any other model-related operations here
