# MVPose (Temporal tracking and filtering)

- [Introduction](#introduction)
- [Prepare models and datasets](#prepare-models-and-datasets)
- [Results](#results)

## Introduction

We provide the config files for MVPose (Temporal tracking and filtering): [Fast and robust multi-person 3d pose estimation and tracking from multiple views](https://zju3dv.github.io/mvpose/).

```BibTeX
@article{dong2021fast,
  title={Fast and robust multi-person 3d pose estimation and tracking from multiple views},
  author={Dong, Junting and Fang, Qi and Jiang, Wen and Yang, Yurou and Huang, Qixing and Bao, Hujun and Zhou, Xiaowei},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence},
  year={2021},
  publisher={IEEE}
}
```

## Prepare models and datasets

- **Prepare models**:

```
sh scripts/download_weight.sh
```
You can find `resnet50_reid_camstyle.pth.tar` in `weight` file.

- **Prepare the datasets**:

Convert original dataset to our unified meta-data, with data converters controlled by configs,
you can find more details in [dataset_preparation.md](../../docs/en/dataset_preparation.md).

The final file structure would be like:

```text
xrmocap
├── xrmocap
├── docs
├── tools
├── configs
└── weight
    └── resnet50_reid_camstyle.pth.tar
└── xrmocap_data
    ├── Shelf
        ├── Camera0
        ├── ...
        ├── Camera4
        ├── xrmocap_meta_testset_fasterrcnn
        └── xrmocap_meta_testset
    ├── CampusSeq1
    └── panoptic
        ├── xrmocap_meta_ian5
            ├── hd_00_03
            ├── ...
            ├── hd_00_23
            ├── camera_parameters
            ├── keypoints3d_GT.npz
            └── perception_2d.npz
        ├── xrmocap_meta_pizza1
        ├── xrmocap_meta_band4
        └── xrmocap_meta_haggling1
```

## Results

We evaluate MVPose (Temporal tracking and filtering) on 3 popular benchmarks, report the Percentage of Correct Parts (PCP) on Shelf/Campus/CMU-Panoptic datasets.

You can find the recommended configs in `configs/mvpose_tracking/*/eval_keypoints3d.py`, where `interval` is the global matching interval, that is, the maximum number of frames for Kalman filtering. If the interval is set too large, the accuracy of the estimation will be degraded, so we recommen within 50 frames. `__bbox_thr__` is the threshold of bbox2d, you can set a high threshold to ignore incorrect 2D perception data, and we recommen setting it to 0.8~0.9. `best_distance` is the threshold at which the current-frame keypoints2d successfully matches the last-frame keypoints2d, for the different dataset, it needs to be adjusted. `n_cam_min` is the amount of views required for triangulation, which defaults to 2.

### Campus

The 2D perception data we use is generated by fasterrcnn, and you can download it from [here](/docs/en/dataset_preparation.md#download-converted-meta-data). What's more, we set `__bbox_thr__=0.9`, `n_cam_min=2` and `interval=10`.

| Config | Actor 0 | Actor 1 | Actor 2 | Average | Download |
|:------:|:-------:|:--------:|:------:|:-------:|:--------:|
| [eval_keypoints3d.py](./campus_config/eval_keypoints3d.py) | 94.79 | 88.46 | 98.38 | 93.88 | [log](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/logs/MVPoseTracking/campus.zip) |


### Shelf

The 2D perception data we use is generated by fasterrcnn, and you can download it from [here](/docs/en/dataset_preparation.md#download-converted-meta-data). What's more, we set `__bbox_thr__=0.9`, `n_cam_min=3` and `interval=5`.

| Config | Actor 0 | Actor 1 | Actor 2 | Average | Download |
|:------:|:-------:|:--------:|:------:|:-------:|:--------:|
| [eval_keypoints3d.py](./shelf_config/eval_keypoints3d.py) | 98.28 | 95.41 | 97.83 | 97.17 | [log](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/logs/MVPoseTracking/shelf.zip) |


### CMU Panoptic

The 2D perception data we use is generated by mmpose, and you can download it from [here](/docs/en/dataset_preparation.md#download-converted-meta-data). The selection principle of the camera is to cover as much information as possible about the human body, so we selected cameras 3, 6, 12, 13 and 23.

The CMU Panoptic dataset contains four sequences that share the same [config file](panoptic_config/eval_keypoints3d.py). For different sequences, you need to change the `__meta_path__`. What's more, we set `__bbox_thr__=0.85`, `n_cam_min=2` and `interval=10`.

- **160906_band4**

| Config | Actor 0 | Actor 1 | Actor 2 | Average | Download |
|:-------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| [eval_keypoints3d.py](./panoptic_config/eval_keypoints3d.py)  | 98.39 | 98.04 | 95.51 | 97.31 | [log](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/logs/MVPoseTracking/panoptic.zip) |

- **160906_ian5**

| Config | Actor 0 | Actor 1 | Average | Download |
|:-------:|:--------:|:--------:|:--------:|:--------:|
| [eval_keypoints3d.py](./panoptic_config/eval_keypoints3d.py) | 97.52 | 71.12 | 84.32 | [log](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/logs/MVPoseTracking/panoptic.zip) |

- **160906_pizza1**

| Config | Actor 0 | Actor 1 | Actor 2 | Actor 3 | Actor 4 | Actor 5 | Actor 6 | Average | Download |
|:-------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| [eval_keypoints3d.py](./panoptic_config/eval_keypoints3d.py) | 99.44 | 95.05 | 93.85 | 96.07 | 95.76 | 81.96 | 97.15 | 94.18 | [log](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/logs/MVPoseTracking/panoptic.zip) |

- **160422_haggling1**

| Config | Actor 0 | Actor 1 | Actor 2 | Actor 3 | Actor 4 | Actor 5 | Actor 6 | Actor 7 | Actor 8 | Actor 9 | Actor 10 | Actor 11 | Actor 12 | Actor 13 | Actor 14 | Actor 15 | Actor 16 | Actor 17 | Average | Download |
|:-------:|:--------:|:--------:|:--------:|:--------:|:--------:|:-------:|:--------:|:--------:|:--------:|:--------:|:--------:|:-------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| [eval_keypoints3d.py](./panoptic_config/eval_keypoints3d.py) | 98.61 | 98.39 | 96.40 | 99.46 | 97.10 | 94.71 | 97.91 | 82.21 | 98.19 | 91.32 | 98.76 | 97.37 | 96.37 | 95.01 | 97.13 | 90.54 | 98.70 | 93.67 | 95.66 | [log](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/logs/MVPoseTracking/panoptic.zip) |