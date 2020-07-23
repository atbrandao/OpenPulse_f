import numpy as np
from pulse.utils import error

DOF_PER_NODE_STRUCTURAL = 6
DOF_PER_NODE_ACOUSTIC = 1

def distance(a, b):
    return np.linalg.norm(a.coordinates - b.coordinates)

class Node:
    def __init__(self, x, y, z, global_index=None, external_index=None):
        self.x = x
        self.y = y
        self.z = z

        # Structural boundary conditions 
        self.loads = [None, None, None, None, None, None]
        self.there_are_nodal_loads = False
        self.loaded_table_for_nodal_loads = False
        
        self.prescribed_dofs = [None, None, None, None, None, None]
        self.there_are_prescribed_dofs = False
        self.loaded_table_for_prescribed_dofs = False
        self.there_are_constrained_dofs = False
        
        self.lumped_masses = [None, None, None, None, None, None]
        self.there_are_lumped_masses = False
        self.loaded_table_for_lumped_masses = False

        self.lumped_stiffness = [None, None, None, None, None, None]
        self.there_are_lumped_stiffness = False
        self.loaded_table_for_lumped_stiffness = False

        self.lumped_dampings = [None, None, None, None, None, None]
        self.there_are_lumped_dampings = False
        self.loaded_table_for_lumped_dampings = False

        # Acoustic boundary conditions
        self.acoustic_pressure = None
        self.volume_velocity = None

        self.specific_impedance = None
        self.radiation_impedance = 0
        
        self.global_index = global_index
        self.external_index = external_index

    @property
    def coordinates(self):
        return np.array([self.x, self.y, self.z])

    @property
    def local_dof(self):
        return np.arange(DOF_PER_NODE_STRUCTURAL)

    @property
    def global_dof(self):
        return self.local_dof + self.global_index * DOF_PER_NODE_STRUCTURAL
 
    def distance_to(self, other):
        return np.linalg.norm(self.coordinates - other.coordinates)

    # Structural Boundary Condition
    def set_prescribed_dofs_bc(self, boundary_condition):
        self.prescribed_dofs = boundary_condition

    def getStructuralBondaryCondition(self):
        return self.prescribed_dofs

    def get_prescribed_dofs_bc_indexes(self):
        return [i for i, j in enumerate(self.prescribed_dofs) if j is not None]

    def get_prescribed_dofs_bc_values(self):
        return [value for value in self.prescribed_dofs if value is not None]

    # def haveBoundaryCondition(self):
    #     if None in self.prescribed_dofs:
    #         if list(self.prescribed_dofs).count(None) != 6:
    #             return True
    #         else:
    #             return False
    #     elif len(self.prescribed_dofs) == 6:
    #         return True
    
    # def haveForce(self):
    #     for bc in self.loads:
    #         if isinstance(bc, complex):
    #             return True
    #         elif isinstance(bc, np.ndarray):
    #             return True
    #         else:
    #             return False
                
    def set_prescribed_loads(self, loads):
        self.loads = loads

    def get_prescribed_loads(self):
        return self.loads
    
    # Acoustic Boundary Condition
    def set_acoustic_boundary_condition(self, acoustic_boundary_condition):
        self.acoustic_boundary_condition = acoustic_boundary_condition

    def getAcousticBoundaryCondition(self):
        return self.acoustic_boundary_condition
    
    def get_acoustic_boundary_condition_indexes(self):
        return [i for i, j in enumerate([self.acoustic_pressure]) if j is not None]
    
    def get_acoustic_pressure_bc_values(self):
        return [i for i in [self.acoustic_pressure] if i is not None]
    
    def haveAcousticBoundaryCondition(self):
        return self.acoustic_boundary_condition.count(None) != 1

    def set_prescribed_volume_velocity(self, volume_velocity):
        self.volume_velocity = volume_velocity

    #TODO: load a table of real+imaginary components    

    def get_volume_velocity(self, frequencies):
        if isinstance(self.volume_velocity, np.ndarray):
            if len(self.volume_velocity) == len(frequencies):
                return self.volume_velocity
            else:
                error("The frequencies vector should have same length.\n Please, check the frequency analysis setup.")
                return
        else:
            return self.volume_velocity * np.ones_like(frequencies)

    def haveVolumeVelocity(self):
        return self.volume_velocity.count(0) != 1
    
    def admittance(self, area_fluid, frequencies):
        # Only one impedance can be given.
        # More than one must raise an error

        if self.specific_impedance is not None:
            Z = self.specific_impedance / area_fluid
        elif self.radiation_impedance != 0:
            Z = self.radiation_impedance / area_fluid
        
        if isinstance(self.specific_impedance, np.ndarray):
            admittance = np.divide(1,Z)
        elif isinstance(self.specific_impedance, complex) or isinstance(self.specific_impedance, float):
            admittance = 1/Z * np.ones_like(frequencies)
        elif len([Z]) != len(frequencies):
            error(" The vectors of Impedance Z and frequencies must be\n the same lengths to calculate the admittance properly!")
            return

        # if isinstance(Z, float):
        #     admittance = 1/Z * np.ones_like(frequencies)
        # elif len([Z]) != len(frequencies):
        #     error(" The vectors of Impedance Z and frequencies must be\n the same lengths to calculate the admittance properly!")
        #     return
        # else:
        #     admittance = np.divide(1,Z)

        return admittance.reshape([len(frequencies),1])