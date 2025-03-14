import argparse
import pickle

import numpy as np
import torch
from sklearn.mixture import GaussianMixture

from multimodal_gnn.utils import load_model

torch.set_float32_matmul_precision("medium")


def get_items_embedding(model, item_ids: torch.tensor):
    return model.model.embedding(item_ids)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--run-id",
    required=True,
    help="Run id of model on which to base lableling",
)
parser.add_argument(
    "--tagnn",
    action="store_true",
    help="Run id of model on which to base lableling",
)

parser.add_argument(
    "--no-clusters",
    type=int,
    default=16,
    help="Number of clusters in GMM",
)
parser.add_argument(
    "--n-init",
    type=int,
    default=2,
    help="Number of times to recalculate EM for GMM",
)
parser.add_argument(
    "--init-params",
    type=str,
    default="k-means++",
    help="Algorithm with which to init means of gausoids",
)
parser.add_argument(
    "--covariance-type",
    type=str,
    default="full",
    help="Bonds on covariance matrix of every gaussoid. Lookup sklearn docs.",
)
parser.add_argument(
    "--tol",
    type=float,
    default=1e-3,
    help="The convergence threshold.",
)


def main(flags_str=""):
    if flags_str:
        parser_opt = parser.parse_args(flags_str.split())
    else:
        parser_opt = parser.parse_args()

    model, opt = load_model(parser_opt.run_id, parser_opt.tagnn)

    if opt.dataset == "amazon_cd":
        n_node = 157661 + 1
    elif opt.dataset == "amzaon_Baby_Products":
        n_node = 89555 + 1
    elif opt.dataset == "amzaon_Musical_Instruments":
        n_node = 68465 + 1
    elif opt.dataset == "diginetica":
        n_node = 43098
    elif opt.dataset == "yoochoose1_64" or opt.dataset == "yoochoose1_4":
        n_node = 37484
    elif opt.dataset == "otto-recsys":
        n_node = 19679 + 1
    else:
        n_node = 310

    items_embeddings = (
        get_items_embedding(model, torch.arange(n_node, device=model.device))
        .cpu()
        .detach()
        .numpy()
    )
    del model

    gm = GaussianMixture(
        n_components=parser_opt.no_clusters,
        n_init=parser_opt.n_init,
        init_params=parser_opt.init_params,
        weights_init=np.ones(parser_opt.no_clusters) / parser_opt.no_clusters,
        verbose=1,
        covariance_type=parser_opt.covariance_type,
        tol=parser_opt.tol,
    )
    item_labels = gm.fit_predict(items_embeddings)
    print(np.unique(item_labels, return_counts=True))
    with open(
        f"../datasets/{opt.dataset}/item_labels_gmm_{gm.n_components}_{parser_opt.init_params}_{parser_opt.covariance_type}_{parser_opt.tol}_{opt.hiddenSize}_{parser_opt.run_id.split('-')[-1]}.txt",
        "wb",
    ) as f:
        pickle.dump(item_labels, f)
    with open(
        f"../datasets/{opt.dataset}/cluster_centers_gmm_{gm.n_components}_{parser_opt.init_params}_{parser_opt.covariance_type}_{parser_opt.tol}_{opt.hiddenSize}_{parser_opt.run_id.split('-')[-1]}.txt",
        "wb",
    ) as f:
        pickle.dump(gm.means_, f)
    with open(
        f"../datasets/{opt.dataset}/gmm_model_{gm.n_components}_{parser_opt.init_params}_{parser_opt.covariance_type}_{parser_opt.tol}_{opt.hiddenSize}_{parser_opt.run_id.split('-')[-1]}.txt",
        "wb",
    ) as f:
        pickle.dump(gm, f)


if __name__ == "__main__":
    main()
