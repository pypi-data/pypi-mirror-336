# HSR: Hyper-Shape Recognition
# This file is part of HSR, which is licensed under the
# GNU Lesser General Public License v3.0 (or any later version).
# See the LICENSE file for more details.

# Script to collect and pre-process molecules from files and 
# convert them in datastructures to compute their similarity based on 
# PCA method considering coordinates and additional features.

import numpy as np
from rdkit import Chem
from rdkit.Chem.rdmolfiles import MolFromMol2File, MolFromMolFile, MolFromPDBFile, MolFromXYZFile, SDMolSupplier
from .utils import *


def read_mol_from_file(path, removeHs=False, sanitize=False):
    """
    General reader for molecules from files.
    
    Parameters
    ----------
    path : str 
        Path to the file.
    removeHs : bool, optional
        Whether to remove hydrogens. Defaults to False.
    sanitize : bool, optional
        Whether to sanitize the molecules. Defaults to False.
    
    Returns
    -------
    rdkit.Chem.rdchem.Mol
        A RDKit molecule object.
    """
    extension = path.split('.')[-1]
    if extension == 'mol':
        return MolFromMolFile(path, removeHs=removeHs, sanitize=sanitize)
    elif extension == 'mol2':
        return MolFromMol2File(path, removeHs=removeHs, sanitize=sanitize)
    elif extension == 'pdb':
        return MolFromPDBFile(path, removeHs=removeHs, sanitize=sanitize)
    elif extension == 'xyz':
        return MolFromXYZFile(path)
    elif extension == 'sdf':
        suppl = Chem.SDMolSupplier(path, removeHs=removeHs, sanitize=sanitize)
        return next(suppl, None)
    else:
        print(f"Unsupported file format: {extension}")
        return None

def load_molecules_from_sdf(path, removeHs=False, sanitize=False):
    """
    Load a list of molecules from an SDF file.
    
    Parameters
    ----------
    path : str
        Path to the SDF file.
    removeHs : bool, optional
        Whether to remove hydrogens. Defaults to False.
    sanitize : bool, optional
        Whether to sanitize the molecules. Defaults to False.

    Returns
    -------
    list of rdkit.Chem.rdchem.Mol
        A list of RDKit molecule objects.
    """
    suppl = Chem.SDMolSupplier(path, removeHs=removeHs, sanitize=sanitize)
    molecules = [mol for mol in suppl if mol is not None]
    return molecules

def molecule_to_ndarray(molecule, features=DEFAULT_FEATURES, removeHs=False):
    """
    Generate a numpy array representing the given molecule in N dimensions.
    
    This function converts a molecule into an N-dimensional numpy array based on specified features. 
    Each feature is computed using a function defined in the 'features' dictionary.

    Parameters
    ----------
    molecule : rdkit.Chem.rdchem.Mol
        The input RDKit molecule object.
    features : dict[str, callable], optional
        A dictionary where each key is a feature name (str) and the value is a callable 
        function to compute that feature. The function takes an RDKit atom object as input 
        and returns a feature value (a numeric type).
        Defaults to DEFAULT_FEATURES.
    removeHs : : bool, optional
        If True, hydrogen atoms will not be included in the array representation.
        Defaults to False.

    Returns
    -------
    numpy.ndarray
        Array with shape (number of atoms, 3 spatial coordinates + number of features),
        representing the molecule.
    """
    
    molecule_info = {'coordinates': []}

    if features:
        for key in features:
            molecule_info[key] = []

    for atom in molecule.GetAtoms():
        # Skip hydrogens if removeHs is True
        if removeHs and atom.GetAtomicNum() == 1:
            continue
        position = molecule.GetConformer().GetAtomPosition(atom.GetIdx())
        molecule_info['coordinates'].append([position.x, position.y, position.z])

        if features:
            for key, func in features.items():
                value = func(atom)
                molecule_info[key].append(value)

    arrays = []
    for key in molecule_info:
        if key == 'coordinates':
            arrays.append(np.array(molecule_info[key]))  
        else:
            arrays.append(np.array(molecule_info[key]).reshape(-1, 1))
    mol_nd = np.hstack(arrays)
    # Centering data
    mol_nd = mol_nd - np.mean(mol_nd, axis=0)
    return mol_nd


