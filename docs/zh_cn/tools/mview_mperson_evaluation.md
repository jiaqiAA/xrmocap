# 多目多人评估

- [概述](#概述)
- [参数说明](#参数说明)
- [例子](#例子)

## 概述

在Campus、Shelf和CMU-Panoptic数据集上，该工具将校准的相机参数、RGB序列、2d感知数据和来自“MviewMpersonDataset”的3d真值作为输入，生成多目多人3d关键点，并进行评估。

## 参数说明

- **enable_log_file**:
默认情况下，enable_log_file为False，该工具只将日志打印到控制台。添加`--enable_log_file`使其为True，可将日志写入名为` {smc_file_name}_{time_str}.txt`的文件里。

- **evaluation_config**:
`evaluation_config` 是 `TopDownAssociationEvaluation` 配置文件的路径。 要了解更多细节，请参阅`TopDownAssociationEvaluation`的文档和[code](../../../xrmocap/core/evaluation/top_down_association_evaluation.py)中的说明。

此外，您可以在`configs/mvpose/*/eval_keypoints3d.py` 或 `configs/mvpose_tracking/*/eval_keypoints3d.py`中找到我们准备好的配置文件。

## 例子

在Shelf数据集上，不使用跟踪算法评估的例子：

```python
python tools/mview_mperson_evaluation.py \
      --enable_log_file \
      --evaluation_config configs/mvpose/shelf_config/eval_keypoints3d.py
```

在Shelf数据集上，使用跟踪算法评估的例子：

```python
python tools/mview_mperson_evaluation.py \
      --enable_log_file \
      --evaluation_config configs/mvpose_tracking/shelf_config/eval_keypoints3d.py
```
