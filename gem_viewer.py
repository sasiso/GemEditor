import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from gem_model import GemModel

class GemViewer(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ren = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.GetRenderWindow().GetInteractor()
        self.iren.Initialize()

        self.stlActor = None
        self.cubeActor = None

    def setSTLActor(self, stlActor):
        self.stlActor = stlActor

    def loadSTLModel(self, filepath):
        # Create a new GemModel instance
        gem_model = GemModel()

        # Load the STL model and get the actor
        stl_actor = gem_model.loadSTLModel(filepath)

        # Set the STL actor to the viewer
        self.setSTLActor(stl_actor)

        # Add the STL actor to the renderer
        self.ren.RemoveAllViewProps()
        self.ren.AddActor(stl_actor)
        self.ren.ResetCamera()
        self.GetRenderWindow().Render()
        return stl_actor

    # Add any other viewer-related operations here
