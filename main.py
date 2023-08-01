import sys
import vtk
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QPushButton
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from cube_handler import CubeHandler
from sphere_handler import SphereHandler
#from hemisphere_handler import HemisphereHandler
#from cone_handler import ConeHandler
#from tetrahedron_handler import TetrahedronHandler
#from square_pyramid_handler import SquarePyramidHandler
#from cylinder_handler import CylinderHandler
#from triangular_prism_handler import TriangularPrismHandler
#from cuboid_handler import CuboidHandler
#from pentagon_handler import PentagonHandler
#from hexagon_handler import HexagonHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)

        self.stlActor = None
        self.shape_handler = None

        layout = QVBoxLayout()
        layout.addWidget(self.vtkWidget)

        tool_panel = QWidget(self)
        tool_layout = QGridLayout(tool_panel)

        for i, shape_name in enumerate(["Cube", "Sphere", "Hemisphere", "Cone", "Tetrahedron",
                                        "Square Pyramid", "Cylinder", "Triangular Prism",
                                        "Cuboid", "Pentagon", "Hexagon"]):
            button = QPushButton(f'{shape_name}')
            button.clicked.connect(lambda _, shape=shape_name: self.onButtonClick(shape))
            tool_layout.addWidget(button, i // 5, i % 5)

        layout.addWidget(tool_panel)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()

    def loadSTLModel(self, filepath):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filepath)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        self.stlActor = vtk.vtkActor()
        self.stlActor.SetMapper(mapper)

        self.ren.RemoveAllViewProps()
        self.ren.AddActor(self.stlActor)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    def onButtonClick(self, shape_name):
        if self.stlActor:
            if shape_name == "Cube":
                self.shape_handler = CubeHandler(self.stlActor)
            elif shape_name == "Sphere":
                self.shape_handler = SphereHandler(self.stlActor)
            elif shape_name == "Hemisphere":
                self.shape_handler = HemisphereHandler(self.stlActor)
            elif shape_name == "Cone":
                self.shape_handler = ConeHandler(self.stlActor)
            elif shape_name == "Tetrahedron":
                self.shape_handler = TetrahedronHandler(self.stlActor)
            elif shape_name == "Square Pyramid":
                self.shape_handler = SquarePyramidHandler(self.stlActor)
            elif shape_name == "Cylinder":
                self.shape_handler = CylinderHandler(self.stlActor)
            elif shape_name == "Triangular Prism":
                self.shape_handler = TriangularPrismHandler(self.stlActor)
            elif shape_name == "Cuboid":
                self.shape_handler = CuboidHandler(self.stlActor)
            elif shape_name == "Pentagon":
                self.shape_handler = PentagonHandler(self.stlActor)
            elif shape_name == "Hexagon":
                self.shape_handler = HexagonHandler(self.stlActor)

            self.calculate_and_display_shape()

    def calculate_and_display_shape(self):
        if self.shape_handler:
            self.shape_handler.centre = self.stlActor.GetCenter()
            self.shape_handler.calculate_shape_dimensions()
            
            # Create the shape actor with the specified dimensions
            self.shape_handler.create_shape_actor()

            # Find the position for the shape using collision detection
            if self.shape_handler.find_valid_shape_position():
                # Set transparency for both shape and STL model actors
                self.shape_handler.shape_actor.GetProperty().SetOpacity(0.5)  # Adjust the transparency value as needed
                self.stlActor.GetProperty().SetOpacity(0.3)   # Adjust the transparency value as needed

                # Add the shape actor to the renderer
                self.ren.AddActor(self.shape_handler.shape_actor)

                # Render the scene with the shape and transparent STL model
                self.vtkWidget.GetRenderWindow().Render()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Replace 'path_to_your_stl_file.stl' with the actual path to your STL model
    window.loadSTLModel('path_to_your_stl_file.stl')

    sys.exit(app.exec_())
