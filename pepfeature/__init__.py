#__init__.py
# Version of pepfeature package
__version__ = "1.0.9"

"""Import all modules that exist in the current directory."""
from importlib import import_module
from pathlib import Path
#Code piece adapted from: https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
for f in Path(__file__).parent.glob("*.py"):
    module_name = f.stem
    if (module_name not in globals()):
        import_module(f".{module_name}", __package__)
    del f, module_name
del import_module, Path

__all__ = ["aa_all_feat", "aa_composition", "aa_CT", "aa_descriptors","aa_kmer_composition", "aa_molecular_weight"
           , "aa_num_of_atoms", "aa_proportion", "aa_seq_entropy", "_test"]
