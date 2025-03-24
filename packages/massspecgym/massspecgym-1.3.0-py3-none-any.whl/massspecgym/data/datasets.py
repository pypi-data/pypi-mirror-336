import pandas as pd
import json
import os
import typing as T
import numpy as np
import torch
import matchms
from pathlib import Path
from torch.utils.data.dataset import Dataset
from torch.utils.data.dataloader import default_collate
from torch_geometric.data import Data, Batch
from matchms.importing import load_from_mgf

import massspecgym.utils as utils
from massspecgym.data.transforms import SpecTransform, MolTransform, MolToInChIKey, MetaTransform
from massspecgym.simulation_utils.misc_utils import flatten_lol


class MassSpecDataset(Dataset):
    """
    Dataset containing mass spectra and their corresponding molecular structures. This class is
    responsible for loading the data from disk and applying transformation steps to the spectra and
    molecules.
    """

    def __init__(
        self,
        spec_transform: T.Optional[T.Union[SpecTransform, T.Dict[str, SpecTransform]]] = None,
        mol_transform: T.Optional[T.Union[MolTransform, T.Dict[str, MolTransform]]] = None,
        pth: T.Optional[Path] = None,
        return_mol_freq: bool = True,
        return_identifier: bool = True,
        identifiers_subset: T.Optional[T.List[str]] = None,
        dtype: T.Type = torch.float32
    ):
        """
        Args:
            pth (Optional[Path], optional): Path to the .tsv or .mgf file containing the mass spectra.
                Default is None, in which case the MassSpecGym dataset is downloaded from HuggingFace Hub.
        """
        self.pth = pth
        self.spec_transform = spec_transform
        self.mol_transform = mol_transform
        self.return_mol_freq = return_mol_freq
        self.return_identifier = return_identifier
        self.identifiers_subset = identifiers_subset
        self.dtype = dtype
        self.load_data()
        self.compute_mol_freq()

    def load_data(self):

        if self.pth is None:
            self.pth = utils.hugging_face_download("MassSpecGym.tsv")

        if isinstance(self.pth, str):
            self.pth = Path(self.pth)

        if self.pth.suffix == ".tsv":
            self.metadata = pd.read_csv(self.pth, sep="\t")
            self.spectra = self.metadata.apply(
                lambda row: matchms.Spectrum(
                    mz=np.array([float(m) for m in row["mzs"].split(",")]),
                    intensities=np.array(
                        [float(i) for i in row["intensities"].split(",")]
                    ),
                    metadata={"precursor_mz": row["precursor_mz"]},
                ),
                axis=1,
            )
            self.metadata = self.metadata.drop(columns=["mzs", "intensities"])
        elif self.pth.suffix == ".mgf":
            self.spectra = pd.Series(list(load_from_mgf(str(self.pth))))
            self.metadata = pd.DataFrame([s.metadata for s in self.spectra])
        else:
            raise ValueError(f"{self.pth.suffix} file format not supported.")
        
        if self.identifiers_subset is not None:
            self.metadata = self.metadata[self.metadata["identifier"].isin(self.identifiers_subset)]
            self.spectra = self.spectra[self.metadata.index].reset_index(drop=True)
            self.metadata = self.metadata.reset_index(drop=True)

    def compute_mol_freq(self):
        if self.return_mol_freq:
            if "inchikey" not in self.metadata.columns:
                self.metadata["inchikey"] = self.metadata["smiles"].apply(utils.smiles_to_inchi_key)
            self.metadata["mol_freq"] = self.metadata.groupby("inchikey")["inchikey"].transform("count")

    def __len__(self) -> int:
        return len(self.spectra)

    def __getitem__(
        self, i: int, transform_spec: bool = True, transform_mol: bool = True
    ) -> dict:
        spec = self.spectra[i]
        metadata = self.metadata.iloc[i]
        mol = metadata["smiles"]

        # Apply all transformations to the spectrum
        item = {}
        if transform_spec and self.spec_transform:
            if isinstance(self.spec_transform, dict):
                for key, transform in self.spec_transform.items():
                    item[key] = transform(spec) if transform is not None else spec
            else:
                item["spec"] = self.spec_transform(spec)
        else:
            item["spec"] = spec

        # Apply all transformations to the molecule
        if transform_mol and self.mol_transform:
            if isinstance(self.mol_transform, dict):
                for key, transform in self.mol_transform.items():
                    item[key] = transform(mol) if transform is not None else mol
            else:
                item["mol"] = self.mol_transform(mol)
        else:
            item["mol"] = mol

        # Add other metadata to the item
        item.update({
            k: metadata[k] for k in ["precursor_mz", "adduct"]
        })

        if self.return_mol_freq:
            item["mol_freq"] = metadata["mol_freq"]

        if self.return_identifier:
            item["identifier"] = metadata["identifier"]

        # TODO: this should be refactored
        for k, v in item.items():
            if not isinstance(v, str):
                item[k] = torch.as_tensor(v, dtype=self.dtype)

        return item

    @staticmethod
    def collate_fn(batch: T.Iterable[dict]) -> dict:
        """
        Custom collate function to handle the outputs of __getitem__.
        """
        return default_collate(batch)


class RetrievalDataset(MassSpecDataset):
    """
    Dataset containing mass spectra and their corresponding molecular structures, with additional
    candidates of molecules for retrieval based on spectral similarity.
    """

    def __init__(
        self,
        mol_label_transform: MolTransform = MolToInChIKey(),
        candidates_pth: T.Optional[T.Union[Path, str]] = None,
        **kwargs,
    ):
        """
        Args:
            mol_label_transform (MolTransform, optional): Transformation to apply to the candidate molecules.
                Defaults to `MolToInChIKey()`.
            candidates_pth (Optional[Union[Path, str]], optional): Path to the .json file containing the candidates for
                retrieval. Defaults to None, in which case the candidates for standard `molecular retrieval` challenge
                are downloaded from HuggingFace Hub. If set to `bonus`, the candidates based on molecular formulas
                for the `bonus chemical formulae challenge` are downloaded instead.
        """
        # note: __init__ calls load_data, these variables are required for load_data to work properly
        self.mol_label_transform = mol_label_transform
        self.candidates_pth = candidates_pth
        super().__init__(**kwargs)

    def load_data(self):

        super().load_data()

        # Download candidates from HuggigFace Hub if not a path to exisiting file is passed
        if self.candidates_pth is None:
            self.candidates_pth = utils.hugging_face_download(
                "molecules/MassSpecGym_retrieval_candidates_mass.json"
            )
        elif self.candidates_pth == 'bonus':
            self.candidates_pth = utils.hugging_face_download(
                "molecules/MassSpecGym_retrieval_candidates_formula.json"
            )
        elif isinstance(self.candidates_pth, str):
            if Path(self.candidates_pth).is_file():
                self.candidates_pth = Path(self.candidates_pth)
            else:
                self.candidates_pth = utils.hugging_face_download(self.candidates_pth)

        # Read candidates_pth from json to dict: SMILES -> respective candidate SMILES
        with open(self.candidates_pth, "r") as file:
            self.candidates = json.load(file)

    def __getitem__(self, i) -> dict:
        item = super().__getitem__(i, transform_mol=False)

        # Save the original SMILES representation of the query molecule (for evaluation)
        item["smiles"] = item["mol"]

        # Get candidates
        if item["mol"] not in self.candidates:
            raise ValueError(f'No candidates for the query molecule {item["mol"]}.')
        item["candidates"] = self.candidates[item["mol"]]

        # Save the original SMILES representations of the canidates (for evaluation)
        item["candidates_smiles"] = item["candidates"]

        # Create neg/pos label mask by matching the query molecule with the candidates
        item_label = self.mol_label_transform(item["mol"])
        item["labels"] = [
            self.mol_label_transform(c) == item_label for c in item["candidates"]
        ]

        if not any(item["labels"]):
            raise ValueError(
                f'Query molecule {item["mol"]} not found in the candidates list.'
            )

        # TODO: it should be refactored this way to a dict in the MassSpecDataset constructor
        #       we don't refactor it now to avoid breaking changes
        if not isinstance(self.mol_transform, dict):
            mol_transform = {"mol": self.mol_transform}
        else:
            mol_transform = self.mol_transform

        # Transform the query and candidate molecules
        for key, transform in mol_transform.items():
            item[key] = transform(item["mol"]) if transform is not None else item["mol"]
            item["candidates_"+key] = [transform(c) if transform is not None else c for c in item["candidates"]]
            if isinstance(item[key], np.ndarray):
                item[key] = torch.as_tensor(item[key], dtype=self.dtype)
                item["candidates_"+key] = torch.as_tensor(np.stack(item["candidates_"+key]), dtype=self.dtype)
        del item["candidates"]

        return item

    @staticmethod
    def _collate_fn_variable_size(batch: T.Iterable[dict], key: str) -> T.Union[torch.Tensor, list]:

        # Flatten the list of lists
        if isinstance(batch[0][key], list):
            collated_item = sum([item[key] for item in batch], start=[])

            # Convert to tensor if it's not a list of strings
            if not isinstance(batch[0][key][0], str):
                if isinstance(batch[0][key][0], Data):
                    # PyG Data object
                    collated_item = Batch.from_data_list(collated_item)
                else:
                    # Standard torch tensor
                    collated_item = torch.as_tensor(collated_item)
        
        # Concatenate the tensors
        elif isinstance(batch[0][key], torch.Tensor):
            collated_item = torch.cat([item[key] for item in batch], dim=0)
        
        # Raise an error if the type is not supported
        else:
            raise ValueError(f"Unsupported type: {type(batch[0][key])}")
        
        return collated_item


    @staticmethod
    def collate_fn(batch: T.Iterable[dict]) -> dict:
        # Standard collate for everything except candidates and their labels (which may have different length per sample)
        collated_batch = {}
        for k in batch[0].keys():
            if k.startswith("candidates") or k == "labels":
                # Handle candidates and labels of variable size per sample
                collated_batch[k] = RetrievalDataset._collate_fn_variable_size(batch, k)
            else:
                # Standard torch or PyG collate for everything else
                if isinstance(batch[0][k], Data):
                    collated_batch[k] = Batch.from_data_list([item[k] for item in batch])
                else:
                    collated_batch[k] = default_collate([item[k] for item in batch])

        # Store the batch pointer reflecting the number of candidates per sample
        collated_batch["batch_ptr"] = torch.as_tensor(
            [len(item["candidates_smiles"]) for item in batch]
        )

        return collated_batch


class SimulationDataset(MassSpecDataset):

    def __init__(
        self,
        spec_transform: SpecTransform,
        mol_transform: MolTransform,
        meta_transform: MetaTransform,
        meta_keys: T.List[str],
        pth: T.Optional[Path] = None,
        return_mol_freq: bool = True,
        return_identifier: bool = True,
        dtype: T.Type = torch.float32
    ): 
        
        # note: __init__ calls load_data, these variables are required for load_data to work properly
        self.meta_transform = meta_transform
        self.meta_keys = meta_keys
        super().__init__(
            spec_transform=spec_transform,
            mol_transform=mol_transform,
            pth=pth,
            return_mol_freq=return_mol_freq,
            return_identifier=return_identifier,
            dtype=dtype
        )

    def load_data(self):

        # set self.pth correctly
        # download if necessary
        if self.pth is None:
            self.pth = utils.hugging_face_download(
                "MassSpecGym.tsv"
            )
        else: 
            assert isinstance(self.pth, str)
            if not os.path.isfile(self.pth):
                self.pth = utils.hugging_face_download(self.pth)

        # will never download here
        super().load_data()

        # remove any spectra not included in the simulation challenge
        sim_mask = self.metadata["simulation_challenge"]
        sim_metadata = self.metadata[sim_mask].copy(deep=True)
        # verify all datapoints are not missing CE information and are [M+H]+
        assert (sim_metadata["adduct"]=="[M+H]+").all()
        assert (~sim_metadata["collision_energy"].isna()).all()
        # mz checks
        assert (sim_metadata["precursor_mz"] <= self.spec_transform.mz_to).all()
        # do the filtering
        self.spectra = self.spectra[sim_mask]
        self.metadata = sim_metadata.reset_index(drop=True) 

    def _get_spec_feats(self, i):

        spectrum = self.spectra.iloc[i]
        spec_feats = self.spec_transform(spectrum)
        return spec_feats

    def _get_mol_feats(self, i):

        metadata = self.metadata.iloc[i]
        mol_feats = self.mol_transform(metadata["smiles"])
        return mol_feats

    def _get_meta_feats(self, i):

        metadata = self.metadata.iloc[i]
        meta_feats = self.meta_transform({k: metadata[k] for k in self.meta_keys})
        return meta_feats

    def _get_other_feats(self, i):

        metadata = self.metadata.iloc[i]
        other_feats = {}
        other_feats["smiles"] = metadata["smiles"]
        if self.return_mol_freq:
            other_feats["mol_freq"] = torch.tensor(metadata["mol_freq"])
        if self.return_identifier:
            other_feats["identifier"] = metadata["identifier"]
        return other_feats

    def __getitem__(self, i) -> dict:
        item = {}
        item.update(self._get_spec_feats(i))
        item.update(self._get_mol_feats(i))
        item.update(self._get_meta_feats(i))
        item.update(self._get_other_feats(i))
        return item
    
    def get_collate_data(self, batch_data: dict) -> dict:

        collate_data = {}
        # handle spectrum
        collate_data.update(self.spec_transform.collate_fn(batch_data))
        # handle molecule
        collate_data.update(self.mol_transform.collate_fn(batch_data))
        # handle metadata
        collate_data.update(self.meta_transform.collate_fn(batch_data))
        # handle other stuff
        if "smiles" in batch_data:
            collate_data["smiles"] = batch_data["smiles"].copy()
        if "mol_freq" in batch_data:
            collate_data["mol_freq"] = torch.stack(batch_data["mol_freq"],dim=0)
        if "identifier" in batch_data:
            collate_data["identifier"] = batch_data["identifier"].copy()
        return collate_data

    def collate_fn(self, data_list: T.List[dict]) -> dict:

        keys = list(data_list[0].keys())
        collate_data = {}
        batch_data = {key: [] for key in keys}
        for data in data_list:
            for key in keys:
                batch_data[key].append(data[key])
        collate_data = self.get_collate_data(batch_data)
        return collate_data

        
class RetrievalSimulationDataset(SimulationDataset):

    def __init__(
        self,
        mol_label_transform: MolTransform = MolToInChIKey(),
        candidates_pth: T.Optional[T.Union[Path, str]] = None,

        **kwargs,
    ):
        # note: __init__ calls load_data, these variables are required for load_data to work properly
        self.mol_label_transform = mol_label_transform
        self.candidates_pth = candidates_pth
        super().__init__(**kwargs)

    def load_data(self):

        super().load_data()

        # Download candidates from HuggigFace Hub
        if self.candidates_pth is None:
            self.candidates_pth = utils.hugging_face_download(
                "molecules/MassSpecGym_retrieval_candidates_mass.json"
            )
        else: 
            assert isinstance(self.candidates_pth, str)
            if not os.path.isfile(self.candidates_pth):
                self.candidates_pth = utils.hugging_face_download(self.candidates_pth)

        # Read candidates_pth from json to dict: SMILES -> respective candidate SMILES
        with open(self.candidates_pth, "r") as file:
            self.candidates = json.load(file)

        # check that everything has candidates
        smileses = self.metadata["smiles"]
        candidates_mask = []
        for smiles in smileses:
            candidates_mask.append(smiles in self.candidates)
        candidates_mask = np.array(candidates_mask)
        assert candidates_mask.all()

    def __getitem__(self, i):

        item = super().__getitem__(i)
        smiles = item["smiles"]
        assert isinstance(smiles, str)

        # Get candidates
        if smiles not in self.candidates:
            raise ValueError(f'No candidates for the query molecule {smiles}.')
        candidates_smiles = self.candidates[smiles]

        # # Save the original SMILES representations of the canidates (for evaluation)
        # item["candidates_smiles"] = candidates_smiles

        # Create neg/pos label mask by matching the query molecule with the candidates
        item_label = self.mol_label_transform(smiles)
        candidates_labels = [
            self.mol_label_transform(c) == item_label for c in candidates_smiles
        ]
        if not any(candidates_labels):
            raise ValueError(
                f'Query molecule {smiles} not found in the candidates list.'
            )
        # item["candidates_labels"] = torch.tensor(candidates_labels)

        candidates_mol_feats, candidates_mask = [], []
        for c in candidates_smiles:
            try:
                candidates_mol_feats.append(self.mol_transform(c))
                candidates_mask.append(True)
            except IndexError as e:
                print(f"> error processing candidate {c} for query {smiles}")
                candidates_mol_feats.append(None)
                candidates_mask.append(False)
        
        candidates_smiles = [candidates_smiles[i] for i in range(len(candidates_smiles)) if candidates_mask[i]]
        candidates_labels = [candidates_labels[i] for i in range(len(candidates_labels)) if candidates_mask[i]]
        candidates_mol_feats = [candidates_mol_feats[i] for i in range(len(candidates_mol_feats)) if candidates_mask[i]]

        # filter based on mask
        item["candidates_smiles"] = candidates_smiles
        item["candidates_labels"] = torch.tensor(candidates_labels)
        item["candidates_mol_feats"] = candidates_mol_feats

        return item

    def collate_fn(self, data_list: T.List[dict]) -> dict:

        keys = list(data_list[0].keys())
        collate_data = {}
        batch_data = {key: [] for key in keys}
        for data in data_list:
            for key in keys:
                batch_data[key].append(data[key])
        collate_data = super().get_collate_data(batch_data)
        # transform candidates mols
        c_collate_data = {}
        c_mol_feats = flatten_lol(batch_data["candidates_mol_feats"])
        c_mol_keys = list(c_mol_feats[0].keys())
        c_mol_batch_data = {key: [] for key in c_mol_keys}
        for c_mol_feats in c_mol_feats:
            for key in c_mol_keys:
                c_mol_batch_data[key].append(c_mol_feats[key])
        c_mol_collate_data = self.mol_transform.collate_fn(c_mol_batch_data)
        # c_meta_feats = batch_data["candidates_meta_feats"]
        # c_meta_keys = list(c_meta_feats[0].keys())
        # c_meta_batch_data = 
        # package it
        prefix = "" # "candidates_"
        for key in c_mol_keys:
            c_collate_data[prefix+key] = c_mol_collate_data[key]
        c_collate_data[prefix+"smiles"] = flatten_lol(batch_data["candidates_smiles"])
        c_collate_data[prefix+"batch_ptr"] = torch.tensor([len(item) for item in batch_data["candidates_smiles"]])
        c_collate_data[prefix+"labels"] = torch.cat(batch_data["candidates_labels"],dim=0)
        # copy relevant keys
        collate_data["candidates_data"] = c_collate_data
        return collate_data


# TODO: Dataset for unlabeled spectra.


import h5py
from tqdm import tqdm
from torch_geometric.data import InMemoryDataset, download_url
from torch_geometric.data import Batch

class MoleculeDataset(InMemoryDataset):
    def __init__(
            self,
            root: str,
            pre_transform: MolTransform,
            pre_filter: T.Callable = lambda x: x is not None,
            url: str = "https://huggingface.co/datasets/roman-bushuiev/MassSpecGym/resolve/main/data/molecules/MassSpecGym_molecules_MCES2_disjoint_with_test_fold_4M.tsv",
            mol_col: str = "smiles",
            verbose: bool = True
        ):
        """
        Args:
            root (str): Root directory where the dataset should be saved.
            pre_transform (MolTransform): Pre-transformation to apply to the molecules.
            pre_filter (Callable, optional): Pre-filter to apply to the pre-transformed molecules. Defaults to lambda x: x is not None.
            url (str, optional): URL to download the .tsv dataset from. Defaults to "https://huggingface.co/datasets/roman-bushuiev/MassSpecGym/resolve/main/data/molecules/MassSpecGym_molecules_MCES2_disjoint_with_test_fold_4M.tsv".
            mol_col (str, optional): Column name of the molecules in the dataset. Defaults to "smiles".
            verbose (bool, optional): Whether to print verbose output. Defaults to True.

        TODO: splits
        """
        self.url = url
        self.mol_col = mol_col
        self.verbose = verbose
        self.file_name = Path(url).name
        super().__init__(root, None, pre_transform, pre_filter)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return [self.file_name]

    @property
    def processed_file_names(self):
        return [Path(self.file_name).with_suffix(".pt")]

    def download(self):
        download_url(self.url, self.raw_dir)

    def process(self):
        # Read data
        df = pd.read_csv(self.raw_paths[0], sep="\t")
        
        # Process all SMILES strings
        smiles_list = df[self.mol_col].tolist()
        data_list = []
        
        # Process each SMILES string
        for smiles in tqdm(smiles_list, desc="Processing molecules"):
            # Pre-transform
            if self.pre_transform is not None:
                data = self.pre_transform(smiles)
            else:
                data = smiles

            # Pre-filter
            if self.pre_filter is not None:
                if not self.pre_filter(data):
                    continue
                    
            data_list.append(data)

        # Collate all molecules into single batch
        if self.verbose:
            print('Collating...')
        processed_data = Batch.from_data_list(data_list)
        del data_list

        if self.verbose:
            print(f'Total processed molecules: {len(processed_data.x):,}')
            print(f'Saving to {h5_path}...')
        
        h5_path = str(Path(self.processed_paths[0]).with_suffix('.hdf5'))
        with h5py.File(h5_path, 'w') as f:
            # Save all attributes with compression
            for key in processed_data.keys():  # ['x', 'edge_index', 'edge_attr', 'batch', 'ptr']
                data = processed_data[key]
                if torch.is_tensor(data) and data is not None:
                    f.create_dataset(key, data=data.numpy(), compression='gzip', compression_opts=5)

        # Store final result 
        self.save(processed_data, self.processed_paths[0])
