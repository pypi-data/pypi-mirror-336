import os
import glob
from qtrlb.config.config import Config, MetaManager
from qtrlb.config.variable_manager import VariableManager




class GateManager(MetaManager):
    """ A container for all gate Config to be accessible through one object.
        Each of their name will become an attribute of this GateManager.
        And this one itself can become an attribute of MetaManager.
        It also bring high-level interface for load, save, get, set, delete.

        Note from Zihao(04/17/2023):
        Yes, this class inherit MetaManager instead of Config, even though it takes Config-like \
        parameters to initialize. I don't think this is hack, and I believe it's the perfect \
        example of OOP.
    """
    def __init__(self, 
                 yamls_path: str, 
                 varman: VariableManager = None,
                 splitter: str = ':'):
        
        yamls_path = os.path.join(yamls_path, 'Gates')
        files_path_list = glob.glob(os.path.join(yamls_path, '*.yaml'))
        manager_dict = {}

        for file_path in files_path_list:
            gate_name = os.path.basename(file_path).split('.')[0]
            manager_dict[gate_name] = Config(yamls_path=yamls_path, suffix=gate_name, varman=varman)

        super().__init__(manager_dict=manager_dict, working_dir=None, splitter=splitter)
        self.load()