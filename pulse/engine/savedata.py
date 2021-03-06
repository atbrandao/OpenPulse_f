import h5py
import os

class SaveData:

    def __init__(self,
                connectivity,
                nodal_coordinates, 
                data_K, 
                data_M, 
                I,
                J,
                dofs_free, 
                **kwargs):

        self.connectivity = connectivity
        self.nodal_coordinates = nodal_coordinates
        self.data_K = data_K
        self.data_M = data_M
        self.I = I
        self.J = J
        self.dofs_free = dofs_free
        self.dofs_prescribed = kwargs.get("dofs_prescribed", None)
        self.natural_frequencies_structural = kwargs.get("natural_frequencies", None)
        self.eigenVectors = kwargs.get("eigenVectors", None)
        self.eigenVectors_Uxyz = kwargs.get("eigenVectors_Uxyz", None)
        self.eigenVectors_Rxyz = kwargs.get("eigenVectors_Rxyz", None)
        self.frequency_analysis = kwargs.get("frequency_analysis", None)
        self.U_out = kwargs.get("U_out", None)
        self.file_name = kwargs.get("file_name", "results_data.hdf5")
        self.folder_name = kwargs.get("folder_name", "output_data")
    
    #%% Save obtained results in HDF5 format
        
    def store_data(self):
        """ This method stores relevant output data obtained with model solution

        """

        path = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]
        os.chdir(path)

        if not os.path.exists(self.folder_name):

            os.mkdir(self.folder_name)
            os.chdir(self.folder_name)
        else:
            os.chdir(self.folder_name)
      
        if os.path.exists(self.file_name):
            f = h5py.File(self.file_name)
            f.close()
            print("\nThe already existing '" + self.file_name + "' file has been overwritten.")
            print("Folder path:", os.getcwd())
            flag = False
        else:
            flag = True

        f = h5py.File(self.file_name, 'w')
        f.create_dataset('/input/nodal_coordinates', data = self.nodal_coordinates, dtype = 'float64')
        f.create_dataset('/input/connectivity', data = self.connectivity, dtype = 'int')
        f.create_dataset('/global_matrices/I', data = self.I, dtype = 'int')
        f.create_dataset('/global_matrices/J', data = self.J, dtype = 'int')
        f.create_dataset('/global_matrices/data_K', data = self.data_K, dtype = 'float64')
        f.create_dataset('/global_matrices/data_M', data = self.data_M, dtype = 'float64')
        f.create_dataset('/global_matrices/dofs_free', data = self.dofs_free, dtype = 'float64')
        if self.dofs_prescribed.all() != None:
            f.create_dataset('/results/dofs_prescribed', data = self.dofs_prescribed, dtype = 'float64')
        if self.natural_frequencies_structural.all() != None:    
            f.create_dataset('/results/natural_frequencies', data = self.natural_frequencies_structural, dtype = 'float64')
        if self.eigenVectors.all() != None:
            f.create_dataset('/results/eigenVectors', data = self.eigenVectors, dtype = 'float64')
        if self.eigenVectors_Uxyz.all() != None:
            f.create_dataset('/results/eigenVectors_Uxyz', data = self.eigenVectors_Uxyz, dtype = 'float64')
        if self.frequency_analysis.all() != None:    
            f.create_dataset('/results/frequency_analysis', data = self.frequency_analysis, dtype = 'float64')
        if self.U_out.all() != None:    
            f.create_dataset('/results/U_out', data = self.U_out, dtype = complex)
        f.close()
        if flag:
            print("\nData has been stored in hard disk.")
            print("File name: '" + self.file_name + "'" )
            print("Folder path:", os.getcwd())
        return #os.getcwd()