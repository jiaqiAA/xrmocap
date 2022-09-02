# Dataset preparation

- [Overview](#overview)
- [Supported datasets](#supported-datasets)
- [Download converted meta-data](#download-converted-meta-data)
- [Convert a dataset manually](#convert-a-dataset-manually)
- [Validate converted meta-data by visualization](#validate-converted-meta-data-by-visualization)

### Overview

Our data pipeline converts original dataset to our unified meta-data, with data converters controlled by configs.

### Supported datasets

| Dataset name | Dataset page                                               | Download                                                     |
| ------------ | ---------------------------------------------------------- | ------------------------------------------------------------ |
| Campus       | [Home page](https://campar.in.tum.de/Chair/MultiHumanPose) | [CampusSeq1.tar.bz2](https://www.campar.in.tum.de/public_datasets/2014_cvpr_belagiannis/CampusSeq1.tar.bz2) |
| Shelf        | [Home page](https://campar.in.tum.de/Chair/MultiHumanPose) | [Shelf.tar.bz2](https://www.campar.in.tum.de/public_datasets/2014_cvpr_belagiannis/Shelf.tar.bz2) |
| CMU Panoptic | [Home page](http://domedb.perception.cs.cmu.edu/)          | By [official script](https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox/blob/master/scripts/getData.sh) |

### Download converted meta-data

Considering that it takes long to run a converter if perception2d is checked, we have done it for you. Our perception 2D is generated by mmtrack and mmpose, defined in coco_wholebody by default. You can download compressed zip file for converted meta-data below.

For where to put the downloaded meta-data, check [xrmocap dataset structure](tutorials/new_dataset.md#file-tree-of-our-unified-format) for details.

| Dataset name | meta name          | Download link                                                | Notes                                                        |
| ------------ | ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Campus       | testset            | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Campus/xrmocap_meta_testset.zip) |                                                              |
| Campus       | testset_fasterrcnn | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Campus/xrmocap_meta_testset_fasterrcnn.zip) | Bbox 2D is generated by [mmdet Faster R-CNN](https://github.com/open-mmlab/mmdetection/tree/master/configs/faster_rcnn). |
| ..Campus     | testset_mvpose2d   | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Campus/xrmocap_meta_testset_mvpose2d.zip) | Perception 2D is generated by [MVPose](https://github.com/zju3dv/mvpose#accelerate-the-evaluation), defined in coco convention. |
| Campus       | trainset           | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Campus/xrmocap_meta_trainset.zip) |                                                              |
| Campus       | trainset_pesudo_gt | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Campus/xrmocap_meta_trainset_pesudo_gt.zip) | Ground-truth keypoints3d is generated by [MvP](https://github.com/sail-sg/mvp#22-shelfcampus), defined in campus convention. |
| Shelf        | testset            | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Shelf/xrmocap_meta_testset.zip) |                                                              |
| Shelf        | testset_fasterrcnn | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Shelf/xrmocap_meta_testset_fasterrcnn.zip) | Bbox 2D is generated by [mmdet Faster R-CNN](https://github.com/open-mmlab/mmdetection/tree/master/configs/faster_rcnn). |
| Shelf        | testset_mvpose2d   | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Shelf/xrmocap_meta_testset_mvpose2d.zip) | Perception 2D is generated by [MVPose](https://github.com/zju3dv/mvpose#accelerate-the-evaluation), defined in coco. There's only data for the first three people in ground truth keypoints3d . |
| Shelf        | trainset           | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Shelf/xrmocap_meta_trainset.zip) |                                                              |
| Shelf        | trainset_pesudo_gt | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Shelf/xrmocap_meta_trainset_pesudo_gt.zip) | Ground-truth keypoints3d is generated by [MvP](https://github.com/sail-sg/mvp#22-shelfcampus), defined in campus convention. |
| CMU Panoptic | 160906_band4       | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Panoptic/xrmocap_meta_band4.zip) | Only five views are selected: 03, 06, 12, 13, 23             |
| CMU Panoptic | 160422_haggling1   | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Panoptic/xrmocap_meta_haggling1.zip) | Only five views are selected: 03, 06, 12, 13, 23             |
| CMU Panoptic | 160906_ian5        | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Panoptic/xrmocap_meta_ian5.zip) | Only five views are selected: 03, 06, 12, 13, 23             |
| CMU Panoptic | 160906_pizza1      | [download](https://openxrlab-share.oss-cn-hongkong.aliyuncs.com/xrmocap/xrmocap_meta/Panoptic/xrmocap_meta_pizza1.zip) | Only five views are selected: 03, 06, 12, 13, 23             |

For CMU panoptic meta-data, frames extracted from videos have been removed before uploading. One has to convert panoptic data locally with `bbox_detector = None` and `kps2d_estimator = None`  first, and then copy download data into the converted meta-data directory.

### Convert a dataset manually

Use our prepare_dataset tool to convert a dataset. See the [tool tutorial](./tool/prepare_dataset.md) for details.

### Validate converted meta-data by visualization

Use our visualize_dataset tool to visualize meta-data. See the [tool tutorial](./tool/visualize_dataset.md) for details.

For CMU panoptic meta-data, the multi-view all-in-one video is too large to load, please set `vis_aio_video = False`  to avoid OOM.