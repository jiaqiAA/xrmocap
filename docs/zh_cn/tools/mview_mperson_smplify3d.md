# 多目多人 SMPLify3D 工具

- [概述](#概述)
- [参数说明](#参数说明)
- [例子](#例子)

## 概述

该工具可以从 3d 关键点生成多人 SMPLData。

## 参数说明

- **estimator_config**:
`estimator_config` 是 `MultiPersonSMPLEstimator` 配置文件的路径。 更多细节可查看 `MultiPersonSMPLEstimator` 的文档和[代码](../../../xrmocap/core/estimation/mperson_smpl_estimator.py)。

- **start_frame**:
`start_frame` 是起始帧的索引。

- **end_frame**:
`end_frame` 是终止帧的索引。

- **bbox_thr**:
`bbox_thr` 是 bbox2d 的阈值, 其大小应该与在得到 3d 关键点时的阈值一致。

- **keypoints3d_path**:
`keypoints3d_path` 是存储 3d 关键点文件的路径。

- **matched_kps2d_idx**:
`matched_kps2d_idx` 多视角 2d 关键点匹配结果, 生成于此[代码](../../../tools/mview_mperson_evaluation.py)。

- **image_and_camera_param**:
`image_and_camera_param` 是一个包含图像路径和对应相机参数的文本文件。第0行是第一个视角的图像路径，第1行是对应相机参数的路径。第2行是第二个视角的图像路径，第3行是对应相机参数的路径，依此类推。

- **perception2d_path**:
`perception2d_path` 是存储 2d 感知数据的路径。

- **output_dir**:
`output_dir` 是保存输出文件的路径，输出文件包括 SMPLData 和视频。

- **visualize**:
默认情况下，visualize 为 False。添加 `--visualize` 使其为 True，将可视化 SMPLData。

- **enable_log_file**：
默认情况下，enable_log_file 为 False，该工具只将日志打印到控制台。添加 `--enable_log_file` 使其为 True，可将日志写入名为 ` {smc_file_name}_{time_str}.txt` 的文件。


## 例子

```python
python tools/mview_mperson_smplify3d.py \
      --estimator_config 'configs/modules/core/estimation/mperson_smpl_estimator.py' \
      --start_frame 300 \
      --end_frame 600 \
      --keypoints3d_path 'output/mvpose_tracking/shelf/scene0_pred_keypoints3d.npz' \
      --matched_kps2d_idx 'output/mvpose_tracking/shelf/scene0_matched_kps2d_idx.npy' \
      --image_and_camera_param 'xrmocap_data/Shelf/image_and_camera_param.txt' \
      --perception2d_path 'xrmocap_data/Shelf/xrmocap_meta_test/scene_0/perception_2d.npz' \
      --output_dir 'output/mvpose_tracking/shelf/smpl' \
      --visualize \
      --enable_log_file
```
