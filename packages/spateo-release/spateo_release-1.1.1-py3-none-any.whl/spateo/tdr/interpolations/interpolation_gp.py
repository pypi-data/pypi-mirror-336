from typing import Optional, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import gpytorch
import numpy as np
import ot
import pandas as pd
import torch
from anndata import AnnData
from gpytorch.likelihoods import GaussianLikelihood
from numpy import ndarray
from scipy.sparse import issparse

from ...alignment.methods import _chunk, _unsqueeze
from ...logging import logger_manager as lm
from .interpolation_gaussianprocess import Approx_GPModel, Exact_GPModel, gp_train


class Imputation_GPR:
    def __init__(
        self,
        source_adata: AnnData,
        target_points: Optional[ndarray] = None,
        keys: Union[str, list] = None,
        spatial_key: str = "spatial",
        layer: str = "X",
        device: str = "cpu",
        method: Literal["SVGP", "ExactGP"] = "SVGP",
        batch_size: int = 1024,
        shuffle: bool = True,
        inducing_num: int = 512,
        normalize_spatial: bool = True,
    ):

        self.keys = keys
        # Source data
        source_adata = source_adata.copy()
        source_adata.X = source_adata.X if layer == "X" else source_adata.layers[layer]

        source_spatial_data = source_adata.obsm[spatial_key]

        info_data = np.ones(shape=(source_spatial_data.shape[0], 1))
        assert keys != None, "`keys` cannot be None."
        keys = [keys] if isinstance(keys, str) else keys
        obs_keys = [key for key in keys if key in source_adata.obs.keys()]
        if len(obs_keys) != 0:
            obs_data = np.asarray(source_adata.obs[obs_keys].values)
            info_data = np.c_[info_data, obs_data]
        var_keys = [key for key in keys if key in source_adata.var_names.tolist()]
        if len(var_keys) != 0:
            var_data = source_adata[:, var_keys].X
            if issparse(var_data):
                var_data = var_data.toarray()
            info_data = np.c_[info_data, var_data]
        info_data = info_data[:, 1:]

        self.device = f"cuda:{device}" if torch.cuda.is_available() and device != "cpu" else "cpu"
        torch.device(self.device)

        self.train_x = torch.from_numpy(source_spatial_data).float()
        self.train_y = torch.from_numpy(info_data).float()
        if self.device == "cpu":
            self.train_x = self.train_x.cpu()
            self.train_y = self.train_y.cpu()
        else:
            self.train_x = self.train_x.cuda()
            self.train_y = self.train_y.cuda()
        self.train_y = self.train_y.squeeze()

        self.nx = ot.backend.get_backend(self.train_x, self.train_y)
        self.normalize_spatial = normalize_spatial
        if self.normalize_spatial:
            self.train_x = self.normalize_coords(self.train_x)

        self.N = self.train_x.shape[0]
        # create training dataloader
        self.method = method
        from torch.utils.data import DataLoader, TensorDataset

        if method == "SVGP":
            train_dataset = TensorDataset(self.train_x, self.train_y)
            self.train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)
            inducing_idx = (
                np.random.choice(self.train_x.shape[0], inducing_num)
                if self.train_x.shape[0] > inducing_num
                else np.arange(self.train_x.shape[0])
            )
            self.inducing_points = self.train_x[inducing_idx, :].clone()
        else:
            train_loader = {"train_x": self.train_x, "train_y": self.train_y}
            # TO-DO: add a dict that contains all the train_x and train_y
            # pass

        self.PCA_reduction = False
        self.info_keys = {"obs_keys": obs_keys, "var_keys": var_keys}

        # Target data
        self.target_points = torch.from_numpy(target_points).float()
        self.target_points = self.target_points.cpu() if self.device == "cpu" else self.target_points.cuda()

    def normalize_coords(self, data: Union[np.ndarray, torch.Tensor], given_normalize: bool = False):
        if not given_normalize:
            self.mean_data = self.nx.mean(data, axis=0)[None, :]
        data = data - self.mean_data
        if not given_normalize:
            self.variance = self.nx.sqrt(self.nx.sum(data**2) / data.shape[0])
        data = data / self.variance
        return data

    def inference(
        self,
        training_iter: int = 50,
        verbose: bool = True,
    ):
        self.likelihood = GaussianLikelihood()
        if self.method == "SVGP":
            self.GPR_model = Approx_GPModel(inducing_points=self.inducing_points)
        elif self.method == "ExactGP":
            self.GPR_models = [
                Exact_GPModel(self.train_x, self.train_y[:, i], self.likelihoods[i])
                for i in range(self.train_y.shape[1])
            ]
        # if to convert to GPU
        if self.device != "cpu":
            self.GPR_model = self.GPR_model.cuda()
            self.likelihood = self.likelihood.cuda()

        # Start training to find optimal model hyperparameters
        gp_train(
            model=self.GPR_model,
            likelihood=self.likelihood,
            train_loader=self.train_loader,
            train_epochs=training_iter,
            method=self.method,
            N=self.N,
            device=self.device,
            verbose=verbose,
            keys=self.keys,
        )

        self.GPR_model.eval()
        self.likelihood.eval()

    def interpolate(
        self,
        use_chunk: bool = False,
        chunk_num: int = 20,
    ):
        # Get into evaluation (predictive posterior) mode
        self.GPR_model.eval()
        self.likelihood.eval()

        target_points = self.target_points
        if self.normalize_spatial:
            target_points = self.normalize_coords(target_points, given_normalize=True)

        if use_chunk:
            target_points_s = _chunk(self.nx, target_points, chunk_num, 0)
            arr = []
            with torch.no_grad(), gpytorch.settings.fast_pred_var():
                for target_points_ss in target_points_s:
                    predictions = self.likelihood(self.GPR_model(target_points_ss)).mean
                    arr.append(predictions)
                quary_target = self.nx.concatenate(arr, axis=0)
        else:
            with torch.no_grad(), gpytorch.settings.fast_pred_var():
                predictions = self.likelihood(self.GPR_model(target_points))
                quary_target = predictions.mean

        quary_target = np.asarray(quary_target.cpu()) if self.device != "cpu" else np.asarray(quary_target)
        return quary_target


def gp_interpolation(
    source_adata: AnnData,
    target_points: Optional[ndarray] = None,
    keys: Union[str, list] = None,
    spatial_key: str = "spatial",
    layer: str = "X",
    training_iter: int = 50,
    device: str = "cpu",
    method: Literal["SVGP", "ExactGP"] = "SVGP",
    batch_size: int = 1024,
    shuffle: bool = True,
    inducing_num: int = 512,
    verbose: bool = True,
) -> AnnData:
    """
    Learn a continuous mapping from space to gene expression pattern with the Gaussian Process method.

    Args:
        source_adata: AnnData object that contains spatial (numpy.ndarray) in the `obsm` attribute.
        target_points: The spatial coordinates of new data point. If target_coords is None, generate new points based on grid_num.
        keys: Gene list or info list in the `obs` attribute whose interpolate expression across space needs to learned.
        spatial_key: The key in ``.obsm`` that corresponds to the spatial coordinate of each bucket.
        layer: If ``'X'``, uses ``.X``, otherwise uses the representation given by ``.layers[layer]``.
        training_iter:  Max number of iterations for training.
        device: Equipment used to run the program. You can also set the specified GPU for running. ``E.g.: '0'``.

    Returns:
        interp_adata: an anndata object that has interpolated expression.
    """
    assert keys != None, "`keys` cannot be None."
    keys = [keys] if isinstance(keys, str) else keys
    obs_keys = [key for key in keys if key in source_adata.obs.keys()]
    var_keys = [key for key in keys if key in source_adata.var_names.tolist()]
    info_keys = {"obs_keys": obs_keys, "var_keys": var_keys}
    print(info_keys)
    obs_data = []
    var_data = []
    if len(obs_keys) != 0:
        for key in obs_keys:
            GPR = Imputation_GPR(
                source_adata=source_adata,
                target_points=target_points,
                keys=[key],
                spatial_key=spatial_key,
                layer=layer,
                device=device,
                method=method,
                batch_size=batch_size,
                shuffle=shuffle,
                inducing_num=inducing_num,
            )
            GPR.inference(training_iter=training_iter, verbose=verbose)

            # Interpolation
            target_info_data = GPR.interpolate(use_chunk=True)
            obs_data.append(target_info_data[:, None])
    if len(var_keys) != 0:
        for key in var_keys:
            GPR = Imputation_GPR(
                source_adata=source_adata,
                target_points=target_points,
                keys=[key],
                spatial_key=spatial_key,
                layer=layer,
                device=device,
                method=method,
                batch_size=batch_size,
                shuffle=shuffle,
                inducing_num=inducing_num,
            )
            GPR.inference(training_iter=training_iter, verbose=verbose)

            # Interpolation
            target_info_data = GPR.interpolate(use_chunk=True)
            var_data.append(target_info_data[:, None])

    # Output interpolated anndata
    lm.main_info("Creating an adata object with the interpolated expression...")
    if len(obs_keys) != 0:
        obs_data = np.concatenate(obs_data, axis=1)
        obs_data = pd.DataFrame(obs_data, columns=obs_keys)
    if len(var_keys) != 0:
        X = np.concatenate(var_data, axis=1)
        var_data = pd.DataFrame(index=var_keys)

    interp_adata = AnnData(
        X=X if len(var_keys) != 0 else None,
        obs=obs_data if len(obs_keys) != 0 else None,
        obsm={spatial_key: np.asarray(target_points)},
        var=var_data if len(var_keys) != 0 else None,
    )

    lm.main_finish_progress(progress_name="GaussianProcessInterpolation")
    return interp_adata
