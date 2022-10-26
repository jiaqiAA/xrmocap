# 简介

本文件将介绍 XRmoCap 的框架设计和文件结构。


## 框架

### 基于优化方法的框架

[多目单人框架]

重建管线首先进行手动相机估计并逐帧检测2d关键点。然后应用三角化和光束法平差 (Bundle adjustment) 优化相机参数和3d关键点。最后，利用3d关键点拟合得到SMPL模型，进而得到由关节角和根轨迹表示的运动序列。

[多目多人框架]

对于多目多人重建问题，主要有两个挑战。一是建立不同视角间人（或关键点）的对应关系，二是解决人与人之间的遮挡问题。为此，添加了两个模块，分别是匹配模块和跟踪模块。

### 基于学习方法的框架

describe the component of each module (as in the paper)

how to incorporate optimization and learning-based methods into one framework



## 文件结构

```text
.
├── Dockerfile                   # Dockerfile for quick start
├── README.md                    # README
├── README_CN.md                 # README in Chinese
├── configs                      # Recommended configuration files for tools and modules
├── docs                         # docs
├── requirements                 # pypi requirements
├── scripts                      # scripts for downloading data, training and evaluation
├── tests                        # unit tests
├── tools                        # utility tools
└── xrmocap
    ├── core
    │   ├── estimation           # multi-view single-person or multi-pserson SMPL estimator
    │   ├── evaluation           # evluation on datasets
    │   ├── hook                 # hooks to registry
    │   ├── train                # end-to-end model trainer
    │   └── visualization        # visualization functions for data structures
    ├── data
    │   ├── data_converter       # modules for dataset converting into XRMoCap annotation
    │   ├── data_visualization   # modules for dataset visualization
    │   ├── dataloader           # implementation of torch.utils.data.Dataloader
    │   └── dataset              # implementation of torch.utils.data.Dataset
    ├── data_structure           # data structure for single-person SMPL(X/XD), multi-person keypoints etc.
    ├── human_perception         # modules for human perception
    ├── io                       # functions for Input/Output
    ├── model                    # neural network modules
    │   ├── architecture         # high-level models for a specific task
    │   ├── body_model           # re-implementation of SMPL(X) body models
    │   ├── loss                 # loss functions
    │   ├── mvp                  # models for MVP
    │   └── registrant           # re-implementation of SMPLify(X)
    ├── ops                      # operators for multi-view MoCap
    │   ├── projection           # modules for projecting 3D points to 2D points
    │   ├── top_down_association # multi-view human association and tracking on top-down-detection data
    │   └── triangulation        # modules for triangulating 2D points to 3D points
    │       └── point_selection  # modules for selecting good 2D points before triangulation
    ├── transform                # functions and classes for data transform, e.g., bbox, image, keypoints3d
    ├── utils                    # utility functions for camera, geomotry computation and others
    └── version.py               # digital version of XRMocap

```


Usage of each module/folder
