""" feat_utils.py (adapted from SCARF)

Classes to featurize molecules into a graph with onehot concat feats on atoms
and bonds. Inspired by the dgllife library.

"""
from rdkit import Chem
import rdkit.DataStructs as ds
import numpy as np
import torch
import networkx as nx
import torch_geometric as pyg
from copy import deepcopy
import scipy

# from massspecgym.simulation_utils.frag_utils import (
#     CANONICAL_ELEMENT_ORDER,
#     # NODE_FEAT_TO_IDX,
#     # EDGE_FEAT_TO_IDX,
#     # get_node_feats,
#     # get_edge_feats,
# )

CANONICAL_ELEMENT_ORDER = ["C", "H"] + sorted([
	"O",
	"N",
	"P",
	"S",
	"F",
	"Cl",
	"Br",
	"I",
	"Se",
	"Si"
])

atom_feat_registry = {}
bond_feat_registry = {}


def register_bond_feat(cls):
	"""register_bond_feat."""
	bond_feat_registry[cls.name] = {"fn": cls.featurize, "feat_size": cls.feat_size}
	return cls


def register_atom_feat(cls):
	"""register_atom_feat."""
	atom_feat_registry[cls.name] = {"fn": cls.featurize, "feat_size": cls.feat_size}
	return cls

def get_mol_feats_sizes(atom_feats,bond_feats,pe_embed_k):

	mg = MolGraphFeaturizer(atom_feats,bond_feats,pe_embed_k)
	return mg.num_atom_feats,mg.num_bond_feats

class MolGraphFeaturizer:
	def __init__(
		self,
		atom_feats: list = [
			"a_onehot",
			"a_degree",
			"a_hybrid",
			"a_formal",
			"a_radical",
			"a_ring",
			"a_mass",
			"a_chiral",
		],
		bond_feats: list = ["b_degree"],
		pe_embed_k: int = 0,
	):
		"""__init__

		Args:
			atom_feats (list)
			bond_feats (list)
			pe_embed_k (int)

		"""
		self.pe_embed_k = pe_embed_k
		self.atom_feats = atom_feats
		self.bond_feats = bond_feats
		self.a_featurizers = []
		self.b_featurizers = []

		self.num_atom_feats = 0
		self.num_bond_feats = 0

		for i in self.atom_feats:
			if i not in atom_feat_registry:
				raise ValueError(f"Feat {i} not recognized")
			feat_obj = atom_feat_registry[i]
			self.num_atom_feats += feat_obj["feat_size"]
			self.a_featurizers.append(feat_obj["fn"])

		for i in self.bond_feats:
			if i not in bond_feat_registry:
				raise ValueError(f"Feat {i} not recognized")
			feat_obj = bond_feat_registry[i]
			self.num_bond_feats += feat_obj["feat_size"]
			self.b_featurizers.append(feat_obj["fn"])

		self.num_atom_feats += self.pe_embed_k

	def get_mol_graph(
		self,
		mol: Chem.Mol,
		bigraph: str = True,
	) -> dict:
		"""get_mol_graph.

		Args:
			mol (Chem.Mol):
			bigraph (bool): If true, double all edges.

		Return:
			dict:
				"atom_feats": np.ndarray (|N| x d_n)
				"bond_feats": np.ndarray (|E| x d_e)
				"bond_tuples": np.ndarray (|E| x 2)

		"""
		all_atoms = mol.GetAtoms()
		all_bonds = mol.GetBonds()
		bond_feats = []
		bond_tuples = []
		atom_feats = []
		for bond in all_bonds:
			strt = bond.GetBeginAtomIdx()
			end = bond.GetEndAtomIdx()
			bond_tuples.append((strt, end))
			bond_feat = []
			for fn in self.b_featurizers:
				bond_feat.extend(fn(bond))
			bond_feats.append(bond_feat)

		for atom in all_atoms:
			atom_feat = []
			for fn in self.a_featurizers:
				atom_feat.extend(fn(atom))
			atom_feats.append(atom_feat)

		atom_feats = np.array(atom_feats)
		bond_feats = np.array(bond_feats)
		bond_tuples = np.array(bond_tuples)

		# Add doubles
		if bigraph:
			rev_bonds = np.vstack([bond_tuples[:, 1], bond_tuples[:, 0]]).transpose(
				1, 0
			)
			bond_tuples = np.vstack([bond_tuples, rev_bonds])
			bond_feats = np.vstack([bond_feats, bond_feats])
		return {
			"atom_feats": atom_feats,
			"bond_feats": bond_feats,
			"bond_tuples": bond_tuples,
		}

	def get_networkx_graph(self, mol: Chem.Mol, bigraph: str = True):
		"""get_networkx_graph.

		Args:
			mol (Chem.Mol):
			bigraph (bool): If true, double all edges.

		Return:
			networkx graph object
		"""
		mol_graph = self.get_mol_graph(mol, bigraph=bigraph)

		bond_inds = mol_graph["bond_tuples"]
		bond_feats = mol_graph["bond_feats"]
		atom_feats = mol_graph["atom_feats"]

		g = nx.Graph()
		g.add_nodes_from(range(atom_feats.shape[0]))
		g.add_edges_from(bond_inds)

		nx.set_node_attributes(g, values=atom_feats, name="h")
		nx.set_edge_attributes(g, values=bond_feats, name="e")

		return g

	def get_pyg_graph(self, mol: Chem.Mol, bigraph: str = True):

		mol_graph = self.get_mol_graph(mol, bigraph=bigraph)

		bond_inds = mol_graph["bond_tuples"]
		bond_feats = mol_graph["bond_feats"]
		atom_feats = mol_graph["atom_feats"]

		g = pyg.data.Data(
			x=torch.from_numpy(atom_feats).float(),
			edge_index=torch.from_numpy(bond_inds).long().transpose(1, 0),
			edge_attr=torch.from_numpy(bond_feats).float(),
		)

		if self.pe_embed_k > 0:
			pe_embeds = random_walk_pe(
				g,
				k=self.pe_embed_k,
			)
			g.x = torch.cat((g.x, pe_embeds), dim=-1)
		
		return g		

class FeatBase:
	"""FeatBase.

	Extend this class for atom and bond featurizers

	"""

	feat_size = 0
	name = "base"

	@classmethod
	def featurize(cls, x) -> list:
		raise NotImplementedError()


@register_atom_feat
class AtomOneHot(FeatBase):
	name = "a_onehot"
	allowable_set = CANONICAL_ELEMENT_ORDER
	feat_size = len(allowable_set) + 1

	@classmethod
	def featurize(cls, x) -> int:
		return one_hot_encoding(x.GetSymbol(), cls.allowable_set, True)


@register_atom_feat
class AtomDegree(FeatBase):
	name = "a_degree"
	allowable_set = list(range(11))
	feat_size = len(allowable_set) + 1 + 2

	@classmethod
	def featurize(cls, x) -> int:
		deg = [x.GetDegree(), x.GetTotalDegree()]
		onehot = one_hot_encoding(deg, cls.allowable_set, True)
		return deg + onehot


@register_atom_feat
class AtomHybrid(FeatBase):

	name = "a_hybrid"
	allowable_set = [
		Chem.rdchem.HybridizationType.SP,
		Chem.rdchem.HybridizationType.SP2,
		Chem.rdchem.HybridizationType.SP3,
		Chem.rdchem.HybridizationType.SP3D,
		Chem.rdchem.HybridizationType.SP3D2,
	]
	feat_size = len(allowable_set) + 1

	@classmethod
	def featurize(cls, x) -> int:
		onehot = one_hot_encoding(x.GetHybridization(), cls.allowable_set, True)
		return onehot


@register_atom_feat
class AtomFormal(FeatBase):

	name = "a_formal"
	allowable_set = list(range(-2, 3))
	feat_size = len(allowable_set) + 1

	@classmethod
	def featurize(cls, x) -> int:
		onehot = one_hot_encoding(x.GetFormalCharge(), cls.allowable_set, True)
		return onehot


@register_atom_feat
class AtomRadical(FeatBase):

	name = "a_radical"
	allowable_set = list(range(5))
	feat_size = len(allowable_set) + 1

	@classmethod
	def featurize(cls, x) -> int:
		onehot = one_hot_encoding(x.GetNumRadicalElectrons(), cls.allowable_set, True)
		return onehot


@register_atom_feat
class AtomRing(FeatBase):

	name = "a_ring"
	allowable_set = [True, False]
	feat_size = len(allowable_set) * 2

	@classmethod
	def featurize(cls, x) -> int:
		onehot_ring = one_hot_encoding(x.IsInRing(), cls.allowable_set, False)
		onehot_aromatic = one_hot_encoding(x.GetIsAromatic(), cls.allowable_set, False)
		return onehot_ring + onehot_aromatic


@register_atom_feat
class AtomChiral(FeatBase):

	name = "a_chiral"
	allowable_set = [
		Chem.rdchem.ChiralType.CHI_UNSPECIFIED,
		Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW,
		Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW,
		Chem.rdchem.ChiralType.CHI_OTHER,
	]
	feat_size = len(allowable_set) + 1

	@classmethod
	def featurize(cls, x) -> int:
		chiral_onehot = one_hot_encoding(x.GetChiralTag(), cls.allowable_set, True)
		return chiral_onehot


@register_atom_feat
class AtomMass(FeatBase):

	name = "a_mass"
	coef = 0.01
	feat_size = 1

	@classmethod
	def featurize(cls, x) -> int:
		return [x.GetMass() * cls.coef]


@register_bond_feat
class BondDegree(FeatBase):

	name = "b_degree"
	allowable_set = [
		Chem.rdchem.BondType.SINGLE,
		Chem.rdchem.BondType.DOUBLE,
		Chem.rdchem.BondType.TRIPLE,
		Chem.rdchem.BondType.AROMATIC,
	]
	feat_size = len(allowable_set) + 1

	@classmethod
	def featurize(cls, x) -> int:
		return one_hot_encoding(x.GetBondType(), cls.allowable_set, True)


@register_bond_feat
class BondStereo(FeatBase):

	name = "b_stereo"
	allowable_set = [
		Chem.rdchem.BondStereo.STEREONONE,
		Chem.rdchem.BondStereo.STEREOANY,
		Chem.rdchem.BondStereo.STEREOZ,
		Chem.rdchem.BondStereo.STEREOE,
		Chem.rdchem.BondStereo.STEREOCIS,
		Chem.rdchem.BondStereo.STEREOTRANS,
	]
	feat_size = len(allowable_set) + 1

	@classmethod
	def featurize(cls, x) -> int:
		return one_hot_encoding(x.GetStereo(), cls.allowable_set, True)


@register_bond_feat
class BondConj(FeatBase):

	name = "b_ring"
	feat_size = 2

	@classmethod
	def featurize(cls, x) -> int:
		return one_hot_encoding(x.IsInRing(), [False, True], False)


@register_bond_feat
class BondConj(FeatBase):

	name = "b_conj"
	feat_size = 2

	@classmethod
	def featurize(cls, x) -> int:
		return one_hot_encoding(x.GetIsConjugated(), [False, True], False)


def one_hot_encoding(x, allowable_set, encode_unknown=False) -> list:
	"""One_hot encoding.

	Code taken from dgllife library
	https://lifesci.dgl.ai/_modules/dgllife/utils/featurizers.html

	Args:
		x: Val to encode
		allowable_set: Options
		encode_unknown: If true, encode unk

	Return:
		list of bools
	"""

	if encode_unknown and (allowable_set[-1] is not None):
		allowable_set.append(None)

	if encode_unknown and (x not in allowable_set):
		x = None

	return list(map(lambda s: int(x == s), allowable_set))

# def batch_mols_frags(mol_pyg_list,frag_pyg_list,formula_peak_mzs_list,formula_peak_probs_list):

# 	batch_size = len(mol_pyg_list)
# 	mol_pyg = pyg.data.Batch.from_data_list(mol_pyg_list)
# 	frag_pyg = pyg.data.Batch.from_data_list(frag_pyg_list)
# 	assert mol_pyg.num_graphs == frag_pyg.num_graphs == batch_size
# 	assert all(torch.all(frag_pyg.node_feat_idxs[0] == frag_pyg.node_feat_idxs[i]) for i in range(batch_size))
# 	assert all(torch.all(frag_pyg.edge_feat_idxs[0] == frag_pyg.edge_feat_idxs[i]) for i in range(batch_size))
# 	mol_num_nodes = [g.num_nodes for g in mol_pyg_list]
# 	frag_num_nodes = [g.num_nodes for g in frag_pyg_list]
# 	mol_num_nodes = torch.cumsum(torch.tensor([0]+mol_num_nodes),dim=0)
# 	frag_num_nodes = torch.cumsum(torch.tensor([0]+frag_num_nodes),dim=0)
# 	frag_formula_peak_idxs = []
# 	frag_formula_peak_mzs = []
# 	frag_formula_peak_probs = []
# 	frag_formula_sizes = []
# 	frag_formula_peak_sizes = []
# 	for mzs, probs in zip(formula_peak_mzs_list,formula_peak_probs_list):
# 		# sparsify
# 		idx = torch.nonzero(probs)
# 		mzs = mzs[idx[:,0],idx[:,1]]
# 		probs = probs[idx[:,0],idx[:,1]]
# 		frag_formula_peak_idxs.append(idx[:,0])
# 		frag_formula_peak_mzs.append(mzs)
# 		frag_formula_peak_probs.append(probs)
# 		frag_formula_sizes.append(torch.unique(idx,sorted=True).shape[0])
# 		frag_formula_peak_sizes.append(idx.shape[0])
# 	frag_formula_peak_idxs = torch.cat(frag_formula_peak_idxs,dim=0)
# 	frag_formula_peak_mzs = torch.cat(frag_formula_peak_mzs,dim=0)
# 	frag_formula_peak_probs = torch.cat(frag_formula_peak_probs,dim=0)
# 	frag_formula_cumsizes = torch.cumsum(torch.tensor([0]+frag_formula_sizes),dim=0)
# 	frag_formula_sizes = torch.tensor(frag_formula_sizes)
# 	frag_formula_peak_sizes = torch.tensor(frag_formula_peak_sizes)	
# 	batched_mol_frag = {
# 		"mol_pyg": mol_pyg,
# 		"frag_pyg": frag_pyg,
# 		"mol_num_nodes": mol_num_nodes,
# 		"frag_num_nodes": frag_num_nodes,
# 		"frag_formula_peak_idxs": frag_formula_peak_idxs,
# 		"frag_formula_peak_mzs": frag_formula_peak_mzs,
# 		"frag_formula_peak_probs": frag_formula_peak_probs,
# 		"frag_formula_sizes": frag_formula_sizes,
# 		"frag_formula_cumsizes": frag_formula_cumsizes,
# 		"frag_formula_peak_sizes": frag_formula_peak_sizes,
# 	}
# 	return batched_mol_frag

# def get_frag_graph(dag_pyg,frag_node_feats,frag_edge_feats,edges,bigraph):

# 	device = dag_pyg.x.device
# 	# cast
# 	x = dag_pyg.x.long()
# 	edge_attr = dag_pyg.edge_attr.long()
# 	edge_index = dag_pyg.edge_index.long()
# 	node_feat_idxs = dag_pyg.node_feat_idxs.long()
# 	edge_feat_idxs = dag_pyg.edge_feat_idxs.long()
# 	num_nodes = dag_pyg.num_nodes
# 	# select node features
# 	_x = []
# 	_node_feat_idxs = [0]
# 	_node_feat_size = 0
# 	for feat, feat_idx in NODE_FEAT_TO_IDX.items():
# 		if feat in frag_node_feats:
# 			_x_cur = get_node_feats(x,node_feat_idxs[0],feat)
# 			_x.append(_x_cur)
# 			_node_feat_size += _x_cur.shape[1]
# 			# print(feat,feat_idx,_node_feat_size)
# 		_node_feat_idxs.append(_node_feat_size)
# 	_x = torch.cat(_x,dim=1)
# 	_node_feat_idxs = torch.tensor(_node_feat_idxs,device=device,dtype=torch.int64).reshape(1,-1)
# 	# select edge features
# 	_edge_index = edge_index.clone()
# 	_edge_attr = []
# 	_edge_feat_idxs = [0]
# 	_edge_feat_size = 0
# 	for feat, feat_idx in EDGE_FEAT_TO_IDX.items():
# 		if feat in frag_edge_feats:
# 			assert edges
# 			if feat == "complement":
# 				_edge_attr_cur = torch.zeros(edge_attr.shape[0],1,device=device,dtype=torch.int64)
# 			else:
# 				_edge_attr_cur = get_edge_feats(edge_attr,edge_feat_idxs[0],feat)
# 			_edge_attr.append(_edge_attr_cur)
# 			_edge_feat_size += _edge_attr_cur.shape[1]
# 			# print(feat,feat_idx,_edge_feat_size)
# 		_edge_feat_idxs.append(_edge_feat_size)
# 	if len(_edge_attr) == 0:
# 		_edge_attr = [torch.zeros(edge_attr.shape[0],1,device=device,dtype=torch.int64)]
# 	_edge_attr = torch.cat(_edge_attr,dim=1)
# 	_edge_feat_idxs = torch.tensor(_edge_feat_idxs,device=device,dtype=torch.int64).reshape(1,-1)
# 	# convert to undirected
# 	if bigraph:
# 		assert edges
# 		_edge_index_c = torch.stack([_edge_index[1],_edge_index[0]],dim=0)
# 		assert not torch.any(torch.all(_edge_index==_edge_index_c,dim=0),dim=0)
# 		_edge_attr_c = _edge_attr.clone()
# 		if "complement" in frag_edge_feats:
# 			_edge_attr_c[:,-1] = 1 - _edge_attr_c[:,-1]
# 		_edge_index = torch.cat([_edge_index,_edge_index_c],dim=1)
# 		_edge_attr = torch.cat([_edge_attr,_edge_attr_c],dim=0)
# 	if not edges:
# 		assert not bigraph
# 		_edge_index = _edge_index[:,:0]
# 		_edge_attr = _edge_attr[:0,:]
# 	# create pyg object
# 	dag_pyg = pyg.data.Data(
# 		x=_x,
# 		edge_index=_edge_index,
# 		edge_attr=_edge_attr,
# 		node_feat_idxs=_node_feat_idxs,
# 		edge_feat_idxs=_edge_feat_idxs
# 	)
# 	return dag_pyg

def random_walk_pe(g, k):
	"""Random Walk Positional Encoding, as introduced in
	`Graph Neural Networks with Learnable Structural and Positional Representations
	<https://arxiv.org/abs/2110.07875>`__

	This function computes the random walk positional encodings as landing probabilities
	from 1-step to k-step, starting from each node to itself.
	"""
	# sparse adjacency matrix
	A = scipy.sparse.csr_matrix(
		(
			torch.ones_like(g.edge_index[0]).numpy(),
			(
				g.edge_index[0].numpy(),
				g.edge_index[1].numpy()
			)
		)
	)
	RW = A / (A.sum(1).reshape(-1,1) + 1e-30)  # 1-step transition probability

	# Iterate for k steps
	PE = [RW.diagonal()]
	RW_power = RW.copy()
	for _ in range(k - 1):
		RW_power = RW_power @ RW
		PE.append(RW_power.diagonal())
	PE = np.stack(PE, axis=-1)
	PE = torch.as_tensor(PE,dtype=torch.float32)
	return PE


def get_fingerprints(mol, fp_types):

	fp_arrs = []
	for fp_type in sorted(fp_types):
		if fp_type == "morgan":
			fp = Chem.rdMolDescriptors.GetHashedMorganFingerprint(mol,3)
		elif fp_type == "maccs":
			fp = Chem.rdMolDescriptors.GetMACCSKeysFingerprint(mol)
		elif fp_type == "rdkit":
			fp = Chem.RDKFingerprint(mol)
		else:
			raise ValueError(f"Invalid fingerprint type: {fp_type}")
		fp_arr = np.zeros(1)
		ds.ConvertToNumpyArray(fp, fp_arr)
		fp_arrs.append(fp_arr)
	fp_arrs = np.concatenate(fp_arrs,axis=0)
	return fp_arrs
