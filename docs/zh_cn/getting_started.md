# 快速入门

- [安装指引](#安装指引)
- [数据准备](#数据准备)
- [人体模型下载 (可选)](#人体模型下载-可选)
- [推理](#推理)
- [测评](#测评)
- [训练](#训练)
- [更多教程](#更多教程)

## 安装指引

请参阅[安装教程](./installation.md)。

## 数据准备

请参阅[数据说明](./dataset_preparation.md)。

## 人体模型下载 (可选)

本代码库可以输出人体的3d关键点和SMPL模型，若你需要得到SMPL模型，则需要准备如下模型，反之不需要。

- 我们使用v1.0.0版本的SMPL，请注册以获取下载文件的权限。
  - 从 [SMPL](https://smpl.is.tue.mpg.de/) 下载男性和女性的模型，从 [SMPLify](https://smplify.is.tue.mpg.de/) 下载中性的模型。
  - 所有的模型都需要重命名为 `SMPL_{GENDER}.pkl` 的形式，比如将 `basicModel_neutral_lbs_10_207_0_v1.0.0.pkl` 重命名为 `SMPL_NEUTRAL.pkl`。
- 从 [here](https://openmmlab-share.oss-cn-hangzhou.aliyuncs.com/mmhuman3d/models/smpl_mean_params.npz) 下载  `smpl_mean_params.npz` 文件。
- 从 smplify-x 下载 [gmm_08.zip](https://github.com/vchoutas/smplify-x/files/3295771/gmm_08.zip) 文件，或者从 openxrlab 下载 [gmm_08.pkl](https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/weight/gmm_08.pkl) 文件。

下载上述文件，并将它们按以下文件结构排列:

```text
xrmocap
├── xrmocap
├── docs
├── tests
├── tools
├── configs
└── xrmocap_data
    └── body_models
        ├── gmm_08.pkl
        ├── smpl_mean_params.npz
        └── smpl
            ├── SMPL_FEMALE.pkl
            ├── SMPL_MALE.pkl
            └── SMPL_NEUTRAL.pkl
```

## 推理

目前该框架支持基于优化和基于端到端学习的方法估计SMPL参数，使用我们提供了演示脚本，指定一些参数，您就可以得到多视角图像或视频中单人或多人的SMPL参数。

我们假定相机已标定，如果您想了解更多有关相机标定的知识，请参阅 [XRPrimer](https://github.com/openxrlab/xrprimer/blob/main/docs/en/tools/calibrate_multiple_cameras.md)。


### 模型下载

下载感知模型权重，包括检测、2d 姿态估计、跟踪和 CamStyle 模型权重。

```
sh scripts/download_weight.sh
```
您可以在 `weight` 文件夹下找到已下载的权重文件。

### 单人推理

目前，我们只提供基于优化方法的单人3d关键点和SMPL估计。

1. 下载人体模型，具体步骤请参阅[下载说明](#人体模型下载)。
2. Download a 7z file from [humman dataset](https://drive.google.com/drive/folders/17dinze70MWL5PmB9-Mw36zUjkrQvwb-J).
3. Extract the 7z file.

```bash
cd xrmocap_data/humman
7z x p000127_a000007.7z
```

3. Run [process_smc](./tools/process_smc.md) tool.

```bash
python tools/process_smc.py \
	--estimator_config configs/humman_mocap/mview_sperson_smpl_estimator.py \
	--smc_path xrmocap_data/humman/p000127_a000007.smc \
	--output_dir xrmocap_data/humman/p000127_a000007_output \
	--visualize
```


### 多人推理

您可以从 [here](https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/example_resources/Shelf_50.zip) 下载一个用于快速演示的小型测试数据集。它包含从 Shelf 数据集挑选的5个视角的50帧图像序列以及标定的相机参数。

#### 基于优化的方法

基于优化的方法使用匹配后多视角的2d关键点，借助三角化或其他方法可以生成3d关键点。以 [MVPose](../../configs/mvpose/) 为例，您可以通过以下步骤得到3d关键点。

1. 下载数据和人体模型

- 下载数据

```bash
mkdir xrmocap_data
wget https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/example_resources/Shelf_50.zip -P xrmocap_data
cd xrmocap_data/ && unzip -q Shelf_50.zip && rm Shelf_50.zip && cd ..
```
- 下载人体模型

此部分配置文件的 `smplify` 为非空, 并且您将获得SMPL模型参数。请下载人体模型，具体步骤可参阅[人体模型下载说明](#人体模型下载)。

2. 运行

```python
python tools/mview_mperson_topdown_estimator.py \
      --estimator_config 'configs/mvpose_tracking/mview_mperson_topdown_estimator.py' \
      --image_and_camera_param 'xrmocap_data/Shelf_50/image_and_camera_param.txt' \
      --start_frame 300 \
      --end_frame 350 \
      --output_dir 'output/estimation' \
      --enable_log_file
```
如果所有配置都没问题，您可以在`output_dir`文件夹看到输出结果。

#### 基于学习的方法

For learning-based methods, it resorts to an end-to-end learning scheme so as to require training before inference.
Taking Multi-view Pose Transformer ([MvP](../../configs/mvp/)) as an example, we can download pretrained MvP model and run it on Shelf_50 as:

1. Install `Deformable` package by running the script:
```
sh scripts/download_install_deformable.sh
```

2. Download data and pretrained model

```bash
# download data
mkdir -p xrmocap_data
wget https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/example_resources/Shelf_50.zip -P xrmocap_data
cd xrmocap_data/ && unzip -q Shelf_50.zip && rm Shelf_50.zip && cd ..

# download pretrained model
mkdir -p weight/mvp
wget https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/weight/mvp/xrmocap_mvp_shelf-22d1b5ed_20220831.pth -P weight/mvp
```

3. Run demo with Shelf_50

```bash
sh ./scripts/eval_mvp.sh 1 configs/mvp/shelf_config/mvp_shelf_50.py weight/mvp/xrmocap_mvp_shelf-22d1b5ed_20220831.pth
```

For detailed tutorials about dataset preparation, model weights and checkpoints download for learning-based methods, please refer to the [evaluation tutorial](./tools/eval_model.md).


## 测评

### 模型下载

下载感知模型权重，包括检测、2d 姿态估计、跟踪和 CamStyle 模型权重。

```
sh scripts/download_weight.sh
```

### 使用单卡或多卡GPU进行测评

#### 基于优化的方法

1. 下载数据和人体模型

- 下载 Shelf 数据集和 meta-data

```bash
# download Shelf dataset (16G)
mkdir xrmocap_data
wget https://www.campar.in.tum.de/public_datasets/2014_cvpr_belagiannis/Shelf.tar.bz2 -P xrmocap_data
cd xrmocap_data/ && tar -xf Shelf.tar.bz2 && rm Shelf.tar.bz2 && cd ..

# download meta-data
mkdir -p xrmocap_data/Shelf
wget https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/xrmocap_meta/Shelf/xrmocap_meta_testset_fasterrcnn.zip -P xrmocap_data/Shelf
cd xrmocap_data/Shelf && unzip xrmocap_meta_testset_fasterrcnn.zip && rm xrmocap_meta_testset_fasterrcnn.zip && cd ../..
```
- 下载人体模型

此部分配置文件的 `smplify` 为非空, 并且您将获得SMPL模型参数。请下载人体模型，具体步骤可参阅[人体模型下载说明](#人体模型下载)。


2. 运行

- 使用无跟踪方法在 Shelf 数据集上进行测评：

```bash
python tools/mview_mperson_evaluation.py \
      --enable_log_file \
      --evaluation_config configs/mvpose/shelf_config/eval_keypoints3d.py
```

- 使用跟踪方法在 Shelf 数据集上进行测评：

```bash
python tools/mview_mperson_evaluation.py \
      --enable_log_file \
      --evaluation_config configs/mvpose_tracking/shelf_config/eval_keypoints3d.py
```

有关数据准备和测评的更多细节可参阅 [MVPose evaluation](../../configs/mvpose/README.md) 或 [MVPose tracking evaluation](../../configs/mvpose_tracking/README.md)。

#### Learning-based methods

1. Download and install the `Deformable` package (Skip if you have done this step before)

Run the script:

```bash
sh scripts/download_install_deformable.sh
```

2. Download dataset and pretrained model, taking Shelf dataset as an example:

```bash
# download Shelf dataset (16G)
mkdir -p xrmocap_data
wget https://www.campar.in.tum.de/public_datasets/2014_cvpr_belagiannis/Shelf.tar.bz2 -P xrmocap_data
cd xrmocap_data/ && tar -xf Shelf.tar.bz2 && rm Shelf.tar.bz2 && cd ..

# download meta data
mkdir -p xrmocap_data
wget https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/xrmocap_meta/Shelf/xrmocap_meta_testset.zip -P xrmocap_data
cd xrmocap_data/ && unzip xrmocap_meta_testset.zip && rm xrmocap_meta_testset.zip && mv xrmocap_meta_testset ./Shelf && cd ..

# download pretrained model
mkdir -p weight/mvp
wget https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/weight/mvp/xrmocap_mvp_shelf-22d1b5ed_20220831.pth -P weight/mvp
```

3. Run the evaluation:

```bash
sh ./scripts/eval_mvp.sh 8 configs/mvp/shelf_config/mvp_shelf.py weight/mvp/xrmocap_mvp_shelf-22d1b5ed_20220831.pth
```

### Evaluate with slurm

If you can run XRMoCap on a cluster managed with [slurm](https://slurm.schedmd.com/), you can use the script `scripts/slurm_eval_mvp.sh`.


```bash
sh ./scripts/slurm_eval_mvp.sh ${PARTITION} 8 configs/mvp/shelf_config/mvp_shelf.py weight/mvp/xrmocap_mvp_shelf-22d1b5ed_20220831.pth
```

For learning-based methods, more details about dataset preparation, model weights and checkpoints download and evaluation can be found at [evaluation tutorial](./tools/eval_model.md).


## 训练

Training is only applicable to learning-based methods.

### Training with a single / multiple GPUs

To train the learning-based model, such as a MvP model, to prepare the datasets and pre-trained weights:

1. Download and install the `Deformable` package (Skip if you have done this step before)

Run the script:
```
sh scripts/download_install_deformable.sh
```
2. Download dataset and pretrained models, taking Shelf dataset as an example:

```bash
# download Shelf dataset (16G)
mkdir -p xrmocap_data
wget https://www.campar.in.tum.de/public_datasets/2014_cvpr_belagiannis/Shelf.tar.bz2 -P xrmocap_data
cd xrmocap_data/ && tar -xf Shelf.tar.bz2 && rm Shelf.tar.bz2 && cd ..

# download meta data
mkdir -p xrmocap_data
wget https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/xrmocap_meta/Shelf/xrmocap_meta_trainset_pesudo_gt.zip -P xrmocap_data
cd xrmocap_data/ && unzip xrmocap_meta_trainset_pesudo_gt.zip && rm xrmocap_meta_trainset_pesudo_gt.zip && mv xrmocap_meta_trainset_pesudo_gt ./Shelf && cd ..

# download pretrained 5-view panoptic model to finetune with Shelf datasest
mkdir -p weight/mvp
wget https://openxrlab-share-mainland.oss-cn-hangzhou.aliyuncs.com/xrmocap/weight/mvp/xrmocap_mvp_panoptic_5view-1b673cdf_20220831.pth -P weight/mvp
```

3. Run the training:

```bash
sh ./scripts/train_mvp.sh 8 configs/mvp/campus_config/mvp_campus.py
```

### Training with Slurm

If you can run XRMoCap on a cluster managed with [slurm](https://slurm.schedmd.com/), you can use the script `scripts/slurm_train_mvp.sh`.


```shell
sh ./scripts/slurm_train_mvp.sh ${PARTITION} 8 configs/mvp/shelf_config/mvp_shelf.py
```

For learning-based methods, more details about dataset preparation, model weights and checkpoints download and training can be found at [training tutorial](./tools/train_model.md)


## 更多教程

- [Introduction](./tutorials/introduction.md)
- [Config](./tutorials/config.md)
- [New dataset](./tutorials/new_dataset.md)
- [New module](./tutorials/new_module.md)
