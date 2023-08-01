import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QPushButton
from gem_viewer import GemViewer
from gem_model import GemModel
import vtk

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stlActor = None

        self.gem_viewer = GemViewer(self)
        self.gem_model = GemModel()

        layout = QVBoxLayout()
        layout.addWidget(self.gem_viewer)

        tool_panel = QWidget(self)
        tool_layout = QGridLayout(tool_panel)

        for i in range(10):
            button = QPushButton(f'Button {i + 1}')
            button.clicked.connect(self.onButtonClick)
            tool_layout.addWidget(button, i // 5, i % 5)

        layout.addWidget(tool_panel)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def calculateInscribedCubeDimensions(self):
        if not self.stlActor:
            return None

        bounds = self.stlActor.GetBounds()
        width = bounds[1] - bounds[0]
        height = bounds[3] - bounds[2]
        length = bounds[5] - bounds[4]
        side_length = min(width, height, length)
        return side_length, side_length, side_length
    
    def findValidCubePosition(self, width, height, length):
        if not self.stlActor:
            return False

        # Create an OBB (Oriented Bounding Box) tree for the STL model
        obb_tree = vtk.vtkOBBTree()
        obb_tree.SetDataSet(self.stlActor.GetMapper().GetInput())
        obb_tree.BuildLocator()

        # Calculate the center of the STL model
        center = self.stlActor.GetCenter()

        # Check if the cube can fit at the center position
        if self.isCubeValid(center, width, height, length, obb_tree):
            self.cubeActor.SetPosition(center[0] - width / 2, center[1] - height / 2, center[2] - length / 2)
            return True

        # If the cube cannot fit at the center position, search for a valid position using a grid-based approach
        grid_step = min(width, height, length) / 10.0  # Adjust the grid step as needed
        for x in range(-5, 6):
            for y in range(-5, 6):
                for z in range(-5, 6):
                    new_center = (center[0] + x * grid_step, center[1] + y * grid_step, center[2] + z * grid_step)
                    if self.isCubeValid(new_center, width, height, length, obb_tree):
                        self.cubeActor.SetPosition(new_center[0] - width / 2, new_center[1] - height / 2, new_center[2] - length / 2)
                        return True

        # If no valid position is found, return False
        return False
    def onButtonClick(self):
        if self.stlActor:
            # Calculate the dimensions of the inscribed cube
            cube_dimensions = self.calculateInscribedCubeDimensions()
            if cube_dimensions:
                width, height, length = cube_dimensions
                volume = width * height * length

                print(f"Width: {width:.2f}, Height: {height:.2f}, Length: {length:.2f}")
                print(f"Volume: {volume:.2f}")

                # Create the cube actor with the specified dimensions
                cube_source = vtk.vtkCubeSource()
                cube_source.SetXLength(width)
                cube_source.SetYLength(height)
                cube_source.SetZLength(length)

                cube_mapper = vtk.vtkPolyDataMapper()
                cube_mapper.SetInputConnection(cube_source.GetOutputPort())

                self.cubeActor = vtk.vtkActor()
                self.cubeActor.SetMapper(cube_mapper)
                self.stlActor.GetProperty().SetOpacity(0.3)   # Adjust the transparency value as needed
                # Find the position for the cube at the center of the STL model using collision detection
                if self.findValidCubePosition(width, height, length):
                    # Set transparency for both cube and STL model actors
                    self.cubeActor.GetProperty().SetOpacity(0.5)  # Adjust the transparency value as needed
                    

                    # Add the cube actor to the renderer
                    self.ren.AddActor(self.cubeActor)

                    # Render the scene with the cube and transparent STL model
                    self.vtkWidget.GetRenderWindow().Render()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Replace 'path_to_your_stl_file.stl' with the actual path to your STL model
    stl_actor = window.gem_viewer.loadSTLModel('path_to_your_stl_file.stl')
    window.stlActor = stl_actor

    sys.exit(app.exec_())
