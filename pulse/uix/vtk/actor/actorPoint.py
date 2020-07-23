import vtk
from pulse.uix.vtk.vtkActorBase import vtkActorBase
import numpy as np

class ActorPoint(vtkActorBase):
    def __init__(self, node, tag = -1, u_def=[]):
        super().__init__()

        self.node = node
        if u_def == []:
            self.x = node.x
            self.y = node.y
            self.z = node.z
        else:
            self.x = u_def[0]
            self.y = u_def[1]
            self.z = u_def[2]   

        self.color = [0,0,1]
        self.special = True
        self.setColor()
        self.tag = tag

        self.sphere = vtk.vtkSphereSource()
        self.cube = vtk.vtkCubeSource()

        self._object = vtk.vtkPolyData()

        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)

        self._mapper = vtk.vtkPolyDataMapper()

    def setColor(self):
        if self.node.there_are_prescribed_dofs and self.node.there_are_nodal_loads:
            self.color = [0,1,0]
        elif self.node.there_are_prescribed_dofs:
            if True in [True if value is not None else False for value in self.node.prescribed_dofs]:
                if True in [True if isinstance(value, np.ndarray) else False for value in self.node.prescribed_dofs]:
                    self.color = [1,1,1]
                elif sum([value if value is not None else complex(0) for value in self.node.prescribed_dofs]) != complex(0):
                    self.color = [1,1,1]
                else:
                    self.color = [0,0,0]
        elif self.node.there_are_nodal_loads:
            self.color = [0,1,1]
        else:
            self.special = False

    def source(self):
        self.sphere.SetRadius(0.03)
        self.sphere.SetCenter(self.x, self.y, self.z)
        self.sphere.SetPhiResolution(11)
        self.sphere.SetThetaResolution(21)

        self.cube.SetXLength(0.01)
        self.cube.SetYLength(0.01)
        self.cube.SetZLength(0.01)
        self.cube.SetCenter(self.x, self.y, self.z)

    def filter(self):
        pass

    def map(self):
        if self.special:
            self._mapper.SetInputConnection(self.sphere.GetOutputPort())
        else:
            self._mapper.SetInputConnection(self.cube.GetOutputPort())
        self._mapper.ScalarVisibilityOff()

    def actor(self):
        self._actor.SetMapper(self._mapper)
        #self._actor.GetProperty().SetDiffuseColor(1,0,.5)
        self._actor.GetProperty().SetColor(self.color)
        self._actor.GetProperty().SetDiffuse(.8)
        self._actor.GetProperty().SetSpecular(.5)
        self._actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
        self._actor.GetProperty().SetSpecularPower(30.0)