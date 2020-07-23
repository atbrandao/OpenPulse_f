from time import time
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
from pulse.utils import timer, error

from pulse.preprocessing.node import DOF_PER_NODE_ACOUSTIC
from pulse.preprocessing.acoustic_element import ENTRIES_PER_ELEMENT, DOF_PER_ELEMENT

class AssemblyAcoustic:
    def __init__(self, mesh, frequencies):
        self.mesh = mesh
        self.frequencies = frequencies

    def get_prescribed_indexes(self):
        global_prescribed = []
        for node in self.mesh.nodes.values():
            starting_position = node.global_index * DOF_PER_NODE_ACOUSTIC
            dofs = np.array(node.get_acoustic_boundary_condition_indexes()) + starting_position
            global_prescribed.extend(dofs)
        return global_prescribed

    def get_prescribed_values(self):
        global_prescribed = []
        for node in self.mesh.nodes.values():
            if node.acoustic_pressure is not None:
                global_prescribed.extend([node.acoustic_pressure])
        return global_prescribed

    def get_unprescribed_indexes(self):
        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.mesh.nodes)
        all_indexes = np.arange(total_dof)
        prescribed_indexes = self.get_prescribed_indexes()
        unprescribed_indexes = np.delete(all_indexes, prescribed_indexes)
        return unprescribed_indexes

    def get_global_matrices(self):

        ones = np.ones(len(self.frequencies), dtype='float64')

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.mesh.nodes)
        total_entries = ENTRIES_PER_ELEMENT * len(self.mesh.acoustic_elements)

        rows, cols = self.mesh.get_global_acoustic_indexes()
        data_k = np.zeros([len(self.frequencies), total_entries], dtype = complex)

        for index, element in enumerate(self.mesh.acoustic_elements.values()):

            start = index * ENTRIES_PER_ELEMENT
            end = start + ENTRIES_PER_ELEMENT 
            # data arrangement: pressures are arranged in columns and each row corresponds to one frequency of the analysis
            data_k[:, start:end] = element.matrix(self.frequencies, ones)
            
        full_K = [csr_matrix((data, (rows, cols)), shape=[total_dof, total_dof], dtype=complex) for data in data_k]

        prescribed_indexes = self.get_prescribed_indexes()
        unprescribed_indexes = self.get_unprescribed_indexes()

        K = [full[unprescribed_indexes, :][:, unprescribed_indexes] for full in full_K]
        Kr = [full[:, prescribed_indexes] for full in full_K]

        return K, Kr
            
    def get_lumped_matrices(self):

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.mesh.nodes)

        prescribed_indexes = self.get_prescribed_indexes()
        unprescribed_indexes = self.get_unprescribed_indexes()
        
        data_Klump = []
        ind_Klump = []
        area_fluid = None

        elements = self.mesh.acoustic_elements.values()

        # processing external elements by node
        for node in self.mesh.nodes.values():

            if node.specific_impedance is None:
                node_specific_impedance = 0
            else:
                node_specific_impedance = node.specific_impedance

            if node.radiation_impedance is None:
                node_radiation_impedance = 0
            else:
                node_radiation_impedance = node.radiation_impedance

            if np.sum(node_specific_impedance + node_radiation_impedance) != 0:
                position = node.global_index
                area_fluid = []

                for element in elements:
                    if element.first_node.global_index == position or element.last_node.global_index == position:
                        area_fluid.append(element.cross_section.area_fluid)

                if np.var(area_fluid) != 0:
                    error(" All the elements should to have an uniform Cross-Section! ")
                    return
                else:
                    area_fluid = np.mean(area_fluid)

                ind_Klump.append(position)
                if data_Klump == []:
                    data_Klump = node.admittance(area_fluid, self.frequencies)
                else:
                    data_Klump = np.c_[data_Klump, node.admittance(area_fluid, self.frequencies)]

        if area_fluid is None:
            full_K = [csr_matrix((total_dof, total_dof)) for _ in self.frequencies]
        else:
            full_K = [csr_matrix((data, (ind_Klump, ind_Klump)), shape=[total_dof, total_dof]) for data in data_Klump]
        
        K_lump = [full[unprescribed_indexes, :][:, unprescribed_indexes] for full in full_K]
        Kr_lump = [full[:, prescribed_indexes] for full in full_K]

        return K_lump, Kr_lump  

    def get_global_volume_velocity(self):

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.mesh.nodes)
        volume_velocity = np.zeros([len(self.frequencies), total_dof], dtype=complex)

        for node in self.mesh.nodes.values():
            if node.volume_velocity is not None:
                position = node.global_index
                volume_velocity[:, position] += node.get_volume_velocity(self.frequencies)
        
        unprescribed_indexes = self.get_unprescribed_indexes()
        volume_velocity = volume_velocity[:, unprescribed_indexes]

        return volume_velocity