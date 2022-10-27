# 自上而下的多目多人 SMPL 估计

- [概述](#概述)
- [参数说明](#参数说明)
- [运行](#运行)
  - [步骤0: 估计 2d 感知数据](#步骤0-估计-2d-感知数据)
  - [步骤1: 建立跨视角的人体 2d 关键点联系](#步骤1-建立跨视角的人体-2d-关键点联系)
  - [步骤2: 估计 3d 关键点](#步骤2-估计-3d-关键点)
  - [步骤3: 估计 SMPL](#步骤3-估计-smpl)
- [例子](#例子)

## 概述

以多目 RGB 序列和相机参数作为输入，调用 `run()` 函数可以输出图像中人体的 3d 关键点和 SMPL 参数。

## 参数说明

- **output_dir**:
`output_dir` 是保存输出文件的路径，输出文件包括 3d 关键点、SMPLData 和视频。

- **estimator_config**:
`estimator_config` 是 `MultiViewMultiPersonTopDownEstimator` 配置文件的路径, 其中 `bbox_detector`、`kps2d_estimator`、`associator`、`triangulator` 和 `smplify` 是必须的参数。另外，`point_selectors` 是定义在`xrmocap/ops/triangulation/point_selection` 中选择器配置的列表。 `kps3d_optimizers` 是定义在 `xrmocap/transform/keypoints3d/optim` 中优化器配置的列表。当进行估计时，请设置 `load_batch_size` 为一个合理的值以防计算机内存不足。有关更多细节，请参见[配置文件](../../../configs/modules/core/estimation/mview_mperson_topdown_estimator.py)和[代码](../../../xrmocap/core/estimation/mview_mperson_topdown_estimator.py)中的说明。

- **image_and_camera_param**:
`image_and_camera_param` 是一个包含图像路径和对应相机参数的文本文件。第0行是第一个视角的图像路径，第1行是对应相机参数的路径。第2行是第二个视角的图像路径，第3行是对应相机参数的路径，依此类推。
```text
xrmocap_data/Shelf_50/Shelf/Camera0/
xrmocap_data/Shelf_50/xrmocap_meta_testset_small/scene_0/camera_parameters/fisheye_param_00.json
xrmocap_data/Shelf_50/Shelf/Camera1/
xrmocap_data/Shelf_50/xrmocap_meta_testset_small/scene_0/camera_parameters/fisheye_param_01.json
```

- **start_frame**:
`start_frame` 是起始帧的索引。

- **end_frame**:
`end_frame` 是终止帧的索引。

- **enable_log_file**:
默认情况下，enable_log_file 为 False，该工具只将日志打印到控制台。添加 `--enable_log_file` 使其为 True，可将日志写入名为 ` {smc_file_name}_{time_str}.txt` 的文件里。

- **disable_visualization**:
默认情况下，disable_visualization 为 False，该工具能可视化 3d 关键点和 SMPLData。

## 运行

在 `run()` 函数内部有三个主要步骤，每个步骤的详细信息如下：

### 步骤0: 估计 2d 感知数据

执行自上而下的 2d 关键点估计。使用 `bbox_detector` 检测 bbox2d，使用 `kps2d_estimator` 检测每个 bbox2d 中的人体 2d 关键点。用户可通过修改配置文件来选择不同的 2d 感知模型及权重。

### 步骤1: 建立跨视角的人体 2d 关键点联系
在不同视角中，通过在 `associator` 中添加时域跟踪及滤波算法，得到 2d 关键点的匹配结果。有关 `associator` 的推荐配置，您可查看 [README](../../../configs/mvpose_tracking/README.md)。

### 步骤2: 估计 3d 关键点

我们将 3d 关键点估计分为三个子步骤：点选择、三角化和优化。除三角化外，其他步骤可在配置文件中设置 `None` 来跳过。另外，我们在 `point_selectors` 中使用级联的点选择器来选择多视角中更准确 2d 关键点。在三角化之后，我们使用 `kps3d_optimizer` 来优化 3d 关键点的位置。

### 步骤3: 估计 SMPL

从 3d 关键点估计 SMPL 参数，关于 SMPL 拟合的配置信息，请参考 [smplify 文档](../../../docs/en/model/smplify.md)。

## 例子

```python
python tools/mview_mperson_topdown_estimator.py \
      --image_and_camera_param 'data/image_and_camera_param.txt' \
      --start_frame 0 \
      --end_frame 10 \
      --enable_log_file
```
