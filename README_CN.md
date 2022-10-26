<br/>

<div align="center">
    <img src="resources/xrmocap-logo.png" width="600"/>
</div>

<br/>

<div align="center">

[![Documentation](https://readthedocs.org/projects/xrmocap/badge/?version=latest)](https://xrmocap.readthedocs.io/en/latest/?badge=latest)
[![actions](https://github.com/openxrlab/xrmocap/workflows/build/badge.svg)](https://github.com/openxrlab/xrmocap/actions)
[![codecov](https://codecov.io/gh/openxrlab/xrmocap/branch/main/graph/badge.svg)](https://codecov.io/gh/openxrlab/xrmocap)
[![PyPI](https://img.shields.io/pypi/v/xrmocap)](https://pypi.org/project/xrmocap/)
[![Percentage of issues still open](https://isitmaintained.com/badge/open/openxrlab/xrmocap.svg)](https://github.com/openxrlab/xrmocap/issues)

</div>

## 简介

简体中文 | [English](README.md)

XRMoCap是一款基于PyTorch的多视角动作捕捉开源代码库，是 [OpenXRLab](https://openxrlab.org.cn/) 项目成员之一。

如果您对单视角动作捕捉感兴趣，请参考 [mmhuman3d](https://github.com/open-mmlab/mmhuman3d) 了解更多细节。

https://user-images.githubusercontent.com/26729379/187710195-ba4660ce-c736-4820-8450-104f82e5cc99.mp4

详情参见 [XRMoCap 简介](docs/zh_cn/tutorials/introduction.md)。


### 主要特征

- **支持流行的多目单人和多目多人动作捕捉方法**

  重新实现了从单人到多人的多视角动作捕捉 SOTA 方法，支持任意数目大于2的标定相机，并提供自动选择相机的有效策略。

- **支持基于关键点和参数化人体模型的多视角动捕算法**

  支持两种主流运动表示方法，即 3d 关键点和 SMPL(-X)，并提供它们之间的转换和优化的工具。

- **将基于优化和基于学习的方法集成在模块化框架中**

  整体框架进行模块化设计，将基于优化和基于学习的方法集成在一个框架中。用户可通过在配置文件选择不同的模块，轻松地创建指定的多视角动作捕捉管线。

## 最新进展

- 2022-10-14: XRMoCap [v0.6.0](https://github.com/openxrlab/xrmocap/releases/tag/v0.6.0) 已发布，主要更新包括:
  - 增加 [4D Association Graph](http://www.liuyebin.com/4dassociation/), 该算法的第一个Python实现
  - 增加自上而下的多目多人SMPL估计
  - 添加基于重投影误差的点选择器
- 2022-09-01: XRMoCap [v0.5.0](https://github.com/openxrlab/xrmocap/releases/tag/v0.5.0) 已发布，主要更新包括:
  - 支持 [HuMMan Mocap](https://caizhongang.github.io/projects/HuMMan/) 的多目单人SMPL估计
  - 复现 [MvP](https://arxiv.org/pdf/2111.04076.pdf), 一种基于深度学习的多目多人体三维姿态估计SOTA方法
  - 复现 [MVPose (single frame)](https://arxiv.org/abs/1901.04111) 和 [MVPose (temporal tracking and filtering)](https://ieeexplore.ieee.org/document/9492024), 两种基于优化的多目多人人体三维姿态估计方法
  - 支持 SMPLify, SMPLifyX, SMPLifyD 和 SMPLifyXD


## 基准

更多详情可见[测试基准](docs/en/benchmark.md)。

已支持的方法:

<details open>
<summary>(click to collapse)</summary>

- [x] [SMPLify](https://smplify.is.tue.mpg.de/) (ECCV'2016)
- [x] [SMPLify-X](https://smpl-x.is.tue.mpg.de/) (CVPR'2019)
- [x] [MVPose (Single frame)](https://zju3dv.github.io/mvpose/) (CVPR'2019)
- [x] [MVPose (Temporal tracking and filtering)](https://zju3dv.github.io/mvpose/) (T-PAMI'2021)
- [x] [Shape-aware 3D Pose Optimization](https://ait.ethz.ch/projects/2021/multi-human-pose/) (ICCV'2019)
- [x] [MvP](https://arxiv.org/pdf/2111.04076.pdf) (NeurIPS'2021)
- [x] [HuMMan MoCap](https://caizhongang.github.io/projects/HuMMan/) (ECCV'2022)

</details>

已支持的数据集:

<details open>
<summary>(click to collapse)</summary>

- [x] [Campus](https://campar.in.tum.de/Chair/MultiHumanPose) (CVPR'2014)
- [x] [Shelf](https://campar.in.tum.de/Chair/MultiHumanPose) (CVPR'2014)
- [x] [CMU Panoptic](http://domedb.perception.cs.cmu.edu/) (ICCV'2015)

</details>


## 快速入门

请参考[快速入门](docs/zh_cn/getting_started.md)文档学习 XRMoCap 的基本使用。

## 许可

该代码库采用 Apache-2.0 开源协议。此许可只适用于我们库中的代码，它们的依赖关系是独立的和单独授权的。我们要向所依赖的开源实现致敬。另外，请注意使用依赖项的内容可能会影响我们代码库的许可，请参见 [LICENSE](LICENSE) 查看完整的许可。

## 引用

如果您觉得 XRMoCap 对您的研究有所帮助，请考虑引用它：

```bibtex
@misc{xrmocap,
    title={OpenXRLab Multi-view Motion Capture Toolbox and Benchmark},
    author={XRMoCap Contributors},
    howpublished = {\url{https://github.com/openxrlab/xrmocap}},
    year={2022}
}
```

## 参与贡献

我们感谢所有为改进 XRMoCap 做出贡献的人，请参考 [CONTRIBUTING](.github/CONTRIBUTING.md) 了解更多细节。

## 致谢

XRMoCap 是一个由学术界和工业界的研究人员和工程师共同贡献的开源项目。我们感谢所有为该项目提供算法复现和新功能支持的贡献者，以及提供宝贵反馈的用户。我们希望该工具箱和基准测试能够为社区提供一个灵活的代码工具，供用户复现现有方法和开发自己的新模型，从而不断为开源社区提供贡献。

## OpenXRLab 中的项目

- [XRPrimer](https://github.com/openxrlab/xrprimer): 用于 XR 相关算法的 OpenXRLab 基础库。
- [XRSLAM](https://github.com/openxrlab/xrslam): OpenXRLab 视觉惯性 SLAM 工具箱和测试基准。
- [XRSfM](https://github.com/openxrlab/xrsfm): OpenXRLab 运动结构工具箱和测试基准。
- [XRLocalization](https://github.com/openxrlab/xrlocalization): OpenXRLab 视觉定位工具箱和测试基准。
- [XRMoCap](https://github.com/openxrlab/xrmocap): OpenXRLab 多目动作捕捉工具箱和测试基准。
- [XRMoGen](https://github.com/openxrlab/xrmogen): OpenXRLab 人体运动生成工具箱和测试基准。
- [XRNeRF](https://github.com/openxrlab/xrnerf): OpenXRLab 神经辐射场 (NeRF) 工具箱和测试基准。
