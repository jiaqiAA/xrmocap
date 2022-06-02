import numpy as np
import torch
from abc import ABCMeta
from mmcv.cnn.resnet import ResNet
from torch.autograd import Variable
from torch.nn import functional as F
from typing import Optional, Union

from .base_architecture import BaseArchitecture


def pairwise_affinity(query_features):
    m = query_features.size(0)

    dist = torch.pow(query_features, 2).sum(
        dim=1, keepdim=True).expand(m, m) + torch.pow(query_features, 2).sum(
            dim=1, keepdim=True).expand(m, m).t()
    dist.addmm_(query_features, query_features.t(), beta=1, alpha=-2)
    normalized_affinity = -(dist - dist.mean()) / dist.std()
    affinity = torch.sigmoid(normalized_affinity * torch.tensor(5.))
    return affinity


def reranking(query_features, k1=20, k2=6, lamda_value=0.3):
    feat = torch.cat((query_features, query_features))
    query_num, all_num = query_features.size(0), feat.size(0)
    feat = feat.view(all_num, -1)

    dist = torch.pow(feat, 2).sum(dim=1, keepdim=True).expand(all_num, all_num)
    dist = dist + dist.t()
    dist.addmm_(1, -2, feat, feat.t())

    original_dist = dist.numpy()
    all_num = original_dist.shape[0]
    original_dist = np.transpose(original_dist / np.max(original_dist, axis=0))
    V = np.zeros_like(original_dist).astype(np.float16)
    initial_rank = np.argsort(original_dist).astype(np.int32)

    for i in range(all_num):
        # k-reciprocal neighbors
        forward_k_neigh_index = initial_rank[i, :k1 + 1]
        backward_k_neigh_index = initial_rank[forward_k_neigh_index, :k1 + 1]
        fi = np.where(backward_k_neigh_index == i)[0]
        k_reciprocal_index = forward_k_neigh_index[fi]
        k_reciprocal_expansion_index = k_reciprocal_index
        for j in range(len(k_reciprocal_index)):
            candidate = k_reciprocal_index[j]
            candidate_forward_k_neigh_index = initial_rank[
                candidate, :int(np.around(k1 / 2)) + 1]
            candidate_backward_k_neigh_index = initial_rank[
                candidate_forward_k_neigh_index, :int(np.around(k1 / 2)) + 1]
            fi_candidate = np.where(
                candidate_backward_k_neigh_index == candidate)[0]
            candidate_k_reciprocal_index = \
                candidate_forward_k_neigh_index[fi_candidate]
            if len(
                    np.intersect1d(candidate_k_reciprocal_index,
                                   k_reciprocal_index)
            ) > 2 / 3 * len(candidate_k_reciprocal_index):
                k_reciprocal_expansion_index = np.append(
                    k_reciprocal_expansion_index, candidate_k_reciprocal_index)

        k_reciprocal_expansion_index = np.unique(k_reciprocal_expansion_index)
        weight = np.exp(-original_dist[i, k_reciprocal_expansion_index])
        V[i, k_reciprocal_expansion_index] = weight / np.sum(weight)
    original_dist = original_dist[:query_num, ]
    if k2 != 1:
        V_query_expansion = np.zeros_like(V, dtype=np.float16)
        for i in range(all_num):
            V_query_expansion[i, :] = \
                np.mean(V[initial_rank[i, :k2], :], axis=0)
        V = V_query_expansion
    invIndex = []
    for i in range(all_num):
        invIndex.append(np.where(V[:, i] != 0)[0])

    jaccard_dist = np.zeros_like(original_dist, dtype=np.float16)

    for i in range(query_num):
        temp_min = np.zeros(shape=[1, all_num], dtype=np.float16)
        indNonZero = np.where(V[i, :] != 0)[0]
        indImages = []
        indImages = [invIndex[ind] for ind in indNonZero]
        for j in range(len(indNonZero)):
            temp_min[0, indImages[j]] = temp_min[0, indImages[j]] + \
                np.minimum(V[i, indNonZero[j]], V[indImages[j], indNonZero[j]])
        jaccard_dist[i] = 1 - temp_min / (2 - temp_min)

    final_dist = jaccard_dist * (1 - lamda_value) + original_dist * lamda_value
    final_dist = final_dist[:query_num, query_num:]
    return final_dist


class AppearanceAffinityEstimator(BaseArchitecture, metaclass=ABCMeta):
    """AppearanceAffinityEstimator Architecture."""

    def __init__(self, init_cfg: Optional[Union[list, dict, None]] = None):
        super(AppearanceAffinityEstimator, self).__init__(init_cfg)
        self.backbone = ResNet(depth=50, out_indices=[3])

    def extract_features(self, image_tensor):
        image_tensor = Variable(image_tensor)
        outputs = self.forward_test(image_tensor)
        features = outputs.data
        return features

    def get_affinity(self,
                     image_tensor: torch.Tensor,
                     rerank=False) -> torch.Tensor:
        """Compute affinity matrix.

        Args:
            image_tensor (torch.Tensor)
            rerank (bool, optional): Defaults to False.

        Returns:
            torch.Tensor: affinity
        """
        query_features = self.extract_features(image_tensor)
        if rerank:
            affinity = reranking(query_features)
        else:
            affinity = pairwise_affinity(query_features)
        return affinity

    def forward_train(self, **kwargs):
        """Forward function for general training.

        For 3d pose estimation, we do not use this interface.
        """
        raise NotImplementedError('This interface should not be used in '
                                  'current training schedule. Please use '
                                  '`train_step` for training.')

    def forward_test(self, x: torch.Tensor, **kwargs):
        assert len(kwargs) == 0
        for _, module in self.backbone._modules.items():
            x = module(x)

        # if self.cut_at_pooling:
        #     return x

        x = F.avg_pool2d(x, x.size()[2:])
        x = x.view(x.size(0), -1)

        x = F.normalize(x)
        return x