# Script to test the functions in the preprocessing.py file
import os
import numpy as np
import tempfile
from rdkit import Chem
from hsr import *
import pytest
from rdkit.Chem.rdmolfiles import MolToMolFile

# Create fixture for benzene molecule
@pytest.fixture
def benzene_molecule():
    # the following sdf information was extracted for benzene molecule
    benzene_sdf = """
 Benzene

 12 12  0  0  0  0  0  0  0  0999 V2000
    1.3829   -0.2211    0.0055 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.5068   -1.3064   -0.0076 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.8712   -1.0904   -0.0147 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.3730    0.2110   -0.0046 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.4968    1.2961    0.0109 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.8812    1.0801    0.0137 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.4567   -0.3898    0.0094 H   0  0  0  0  0  0  0  0  0  0  0  0
    0.8977   -2.3203   -0.0126 H   0  0  0  0  0  0  0  0  0  0  0  0
   -1.5537   -1.9359   -0.0279 H   0  0  0  0  0  0  0  0  0  0  0  0
   -2.4466    0.3794   -0.0086 H   0  0  0  0  0  0  0  0  0  0  0  0
   -0.8877    2.3100    0.0204 H   0  0  0  0  0  0  0  0  0  0  0  0
    1.5639    1.9256    0.0225 H   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  1  6  2  0  0  0  0
  1  7  1  0  0  0  0
  2  3  2  0  0  0  0
  2  8  1  0  0  0  0
  3  4  1  0  0  0  0
  3  9  1  0  0  0  0
  4  5  2  0  0  0  0
  4 10  1  0  0  0  0
  5  6  1  0  0  0  0
  5 11  1  0  0  0  0
  6 12  1  0  0  0  0
M  END
$$$$
"""
    return Chem.MolFromMolBlock(benzene_sdf, removeHs=False)

# Testing function load_molecules_from_sdf
def test_load_molecules_from_sdf(benzene_molecule):
    with tempfile.NamedTemporaryFile(suffix=".sdf", delete=False) as temp:
        temp_name = temp.name
        writer = Chem.SDWriter(temp_name)
        writer.write(benzene_molecule)
        writer.close()
 
    molecule_H = pre_processing.load_molecules_from_sdf(temp_name, removeHs=False, sanitize=False)
    molecule_noH = pre_processing.load_molecules_from_sdf(temp_name, removeHs=True, sanitize=True)
    os.remove(temp_name)
    assert isinstance(molecule_H[0], Chem.Mol)
    assert isinstance(molecule_noH[0], Chem.Mol)
    assert molecule_H[0].GetNumAtoms() == 12
    assert molecule_noH[0].GetNumAtoms() == 6

def test_read_molecule_from_file(benzene_molecule):
   
    # File .mol
    Chem.MolToMolFile(benzene_molecule, 'benzene.mol')
    molecule_H = pre_processing.read_mol_from_file('benzene.mol', removeHs=False, sanitize=False)
    molecule_noH = pre_processing.read_mol_from_file('benzene.mol', removeHs=True, sanitize=True)
    os.remove('benzene.mol')
    assert isinstance(molecule_H, Chem.Mol)
    assert isinstance(molecule_noH, Chem.Mol)
    assert molecule_H.GetNumAtoms() == 12
    assert molecule_noH.GetNumAtoms() == 6
    
    # File .mol2 (no rdkit function to write mol2 file)
    
    # File .pdb
    Chem.MolToPDBFile(benzene_molecule, 'benzene.pdb')
    molecule_H = pre_processing.read_mol_from_file('benzene.pdb', removeHs=False, sanitize=False)
    molecule_noH = pre_processing.read_mol_from_file('benzene.pdb', removeHs=True, sanitize=True)
    os.remove('benzene.pdb')
    assert isinstance(molecule_H, Chem.Mol)
    assert isinstance(molecule_noH, Chem.Mol)
    assert molecule_H.GetNumAtoms() == 12
    assert molecule_noH.GetNumAtoms() == 6
    
    # File .xyz
    Chem.MolToXYZFile(benzene_molecule, 'benzene.xyz')
    molecule = pre_processing.read_mol_from_file('benzene.xyz')
    os.remove('benzene.xyz')
    assert isinstance(molecule, Chem.Mol)
    assert molecule.GetNumAtoms() == 12
    
    # File .sdf
    with tempfile.NamedTemporaryFile(suffix=".sdf", delete=False) as temp:
        temp_name = temp.name
        writer = Chem.SDWriter(temp_name)
        writer.write(benzene_molecule)
        writer.close()
        
    molecule_H = pre_processing.read_mol_from_file(temp_name, removeHs=False, sanitize=False)
    molecule_noH = pre_processing.read_mol_from_file(temp_name, removeHs=True, sanitize=True)
    os.remove(temp_name)
    assert isinstance(molecule_H, Chem.Mol)
    assert isinstance(molecule_noH, Chem.Mol)
    assert molecule_H.GetNumAtoms() == 12
    assert molecule_noH.GetNumAtoms() == 6
    

def test_molecule_to_ndarray(benzene_molecule):
    ndarray_representation = pre_processing.molecule_to_ndarray(benzene_molecule)
    assert isinstance(ndarray_representation, np.ndarray)
    assert ndarray_representation.shape[0] == benzene_molecule.GetNumAtoms()

    # Assuming there are 3 features: 'protons', 'neutrons', 'charges'
    assert ndarray_representation.shape[1] == 6  # 3 for coordinates + 3 for features

    # Ensure no NaN values
    assert not np.any(np.isnan(ndarray_representation))
    
def test_molecule_to_ndarray(benzene_molecule):
    ndarray_representation = pre_processing.molecule_to_ndarray(benzene_molecule, removeHs=True)
    assert isinstance(ndarray_representation, np.ndarray)
    assert ndarray_representation.shape[0] == benzene_molecule.GetNumAtoms() - 6

    # Assuming there are 3 features: 'protons', 'neutrons', 'charges'
    assert ndarray_representation.shape[1] == 6  # 3 for coordinates + 3 for features

    # Ensure no NaN values
    assert not np.any(np.isnan(ndarray_representation))



