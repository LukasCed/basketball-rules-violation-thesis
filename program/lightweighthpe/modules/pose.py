import cv2
import numpy as np

from modules.keypoints import BODY_PARTS_KPT_IDS, BODY_PARTS_PAF_IDS
from modules.one_euro_filter import OneEuroFilter
# https://github.com/2xic/openpose-pigs
# https://github.com/Daniil-Osokin/lightweight-human-pose-estimation.pytorch


class Pose:
    num_kpts = 18
    kpt_names = ['nose', 'neck',
                 'r_sho', 'r_elb', 'r_wri', 'l_sho', 'l_elb', 'l_wri',
                 'r_hip', 'r_knee', 'r_ank', 'l_hip', 'l_knee', 'l_ank',
                 'r_eye', 'l_eye',
                 'r_ear', 'l_ear']
                 # relevant (4,7) - hand   (2, 5) - shoe, 
    sigmas = np.array([.26, .79, .79, .72, .62, .79, .72, .62, 1.07, .87, .89, 1.07, .87, .89, .25, .25, .35, .35],
                      dtype=np.float32) / 10.0
    vars = (sigmas * 2) ** 2
    last_id = -1
    color = [0, 224, 255]

    def __init__(self, keypoints, confidence):
        super().__init__()
        self.keypoints = keypoints
        self.confidence = confidence
        self.bbox = Pose.get_bbox(self.keypoints)
        self.id = None
        self.filters = [[OneEuroFilter(), OneEuroFilter()] for _ in range(Pose.num_kpts)]
        self.prev_shoe_1 = None
        self.prev_shoe_2 = None

    @staticmethod
    def get_bbox(keypoints):
        found_keypoints = np.zeros((np.count_nonzero(keypoints[:, 0] != -1), 2), dtype=np.int32)
        found_kpt_id = 0
        for kpt_id in range(Pose.num_kpts):
            if keypoints[kpt_id, 0] == -1:
                continue
            found_keypoints[found_kpt_id] = keypoints[kpt_id]
            found_kpt_id += 1
        bbox = cv2.boundingRect(found_keypoints)
        return bbox

    def update_id(self, id=None):
        self.id = id
        if self.id is None:
            self.id = Pose.last_id + 1
            Pose.last_id += 1

    def draw(self, img):
        assert self.keypoints.shape == (Pose.num_kpts, 2)

        for part_id in range(len(BODY_PARTS_PAF_IDS) - 2):
            a_draw_color = Pose.color
            b_draw_color = Pose.color

            kpt_a_id = BODY_PARTS_KPT_IDS[part_id][0]
            kpt_b_id = BODY_PARTS_KPT_IDS[part_id][1]
            
            if kpt_a_id == 10 or kpt_a_id == 13:
                a_draw_color = [0, 0, 255]
                
            if kpt_b_id == 10 or kpt_b_id == 13:
                b_draw_color = [0, 0, 255]
                                   
            if kpt_a_id == 4 or kpt_a_id == 7:
                a_draw_color = [0, 255, 0]
                
            if kpt_b_id == 4 or kpt_b_id == 7:
                b_draw_color = [0, 255, 0]

            global_kpt_a_id = self.keypoints[kpt_a_id, 0]
            global_kpt_b_id = self.keypoints[kpt_b_id, 0]

            if global_kpt_a_id != -1:
                x_a, y_a = self.keypoints[kpt_a_id]
                cv2.circle(img, (int(x_a), int(y_a)), 10, a_draw_color, -1)

            if global_kpt_b_id != -1:
                x_b, y_b = self.keypoints[kpt_b_id]
                cv2.circle(img, (int(x_b), int(y_b)), 10, b_draw_color, -1)
                
            if global_kpt_a_id != -1 and global_kpt_b_id != -1:
                cv2.line(img, (int(x_a), int(y_a)), (int(x_b), int(y_b)), Pose.color, 2)
    # relevant (4,7) - hand other is shoe             
    def draw_only_relevant(self, img):
        global_kpt_a_id = self.keypoints[4, 0]
        global_kpt_b_id = self.keypoints[7, 0]
        global_kpt_c_id = self.keypoints[10, 0]
        global_kpt_d_id = self.keypoints[13, 0]
       
        if global_kpt_a_id != -1:
            x_a, y_a = self.keypoints[4]
            cv2.circle(img, (int(x_a), int(y_a)), 42, [0, 127, 0], -1)
            
        if global_kpt_b_id != -1:
            x_a, y_a = self.keypoints[7]
            cv2.circle(img, (int(x_a), int(y_a)), 39, [0, 255, 0], -1)
            
        if global_kpt_c_id != -1:
            x_a, y_a = self.keypoints[10]
            cv2.circle(img, (int(x_a), int(y_a)), 42, [0, 0, 127], -1)
            self.prev_shoe_1 = x_a, y_a
        elif self.prev_shoe_1 is not None:
            x_a, y_a = self.prev_shoe_1
            cv2.circle(img, (int(x_a), int(y_a)), 42, [0, 0, 127], -1)

        if global_kpt_d_id != -1:
            x_a, y_a = self.keypoints[13]
            cv2.circle(img, (int(x_a), int(y_a)), 39, [0, 0, 255], -1)
            self.prev_shoe_2 = x_a, y_a
        elif self.prev_shoe_2 is not None:
            x_a, y_a = self.prev_shoe_2
            cv2.circle(img, (int(x_a), int(y_a)), 39, [0, 0, 255], -1)
            


def get_similarity(a, b, threshold=0.5):
    num_similar_kpt = 0
    for kpt_id in range(Pose.num_kpts):
        if a.keypoints[kpt_id, 0] != -1 and b.keypoints[kpt_id, 0] != -1:
            distance = np.sum((a.keypoints[kpt_id] - b.keypoints[kpt_id]) ** 2)
            area = max(a.bbox[2] * a.bbox[3], b.bbox[2] * b.bbox[3])
            similarity = np.exp(-distance / (2 * (area + np.spacing(1)) * Pose.vars[kpt_id]))
            if similarity > threshold:
                num_similar_kpt += 1
    return num_similar_kpt


def track_poses(previous_poses, current_poses, threshold=3, smooth=False):
    """Propagate poses ids from previous frame results. Id is propagated,
    if there are at least `threshold` similar keypoints between pose from previous frame and current.
    If correspondence between pose on previous and current frame was established, pose keypoints are smoothed.

    :param previous_poses: poses from previous frame with ids
    :param current_poses: poses from current frame to assign ids
    :param threshold: minimal number of similar keypoints between poses
    :param smooth: smooth pose keypoints between frames
    :return: None
    """
    current_poses = sorted(current_poses, key=lambda pose: pose.confidence, reverse=True)  # match confident poses first
    mask = np.ones(len(previous_poses), dtype=np.int32)
    for current_pose in current_poses:
        best_matched_id = None
        best_matched_pose_id = None
        best_matched_iou = 0
        for id, previous_pose in enumerate(previous_poses):
            if not mask[id]:
                continue
            iou = get_similarity(current_pose, previous_pose)
            if iou > best_matched_iou:
                best_matched_iou = iou
                best_matched_pose_id = previous_pose.id
                best_matched_id = id
        if best_matched_iou >= threshold:
            mask[best_matched_id] = 0
        else:  # pose not similar to any previous
            best_matched_pose_id = None
        current_pose.update_id(best_matched_pose_id)

        if smooth:
            for kpt_id in range(Pose.num_kpts):
                if current_pose.keypoints[kpt_id, 0] == -1:
                    continue
                # reuse filter if previous pose has valid filter
                if (best_matched_pose_id is not None
                        and previous_poses[best_matched_id].keypoints[kpt_id, 0] != -1):
                    current_pose.filters[kpt_id] = previous_poses[best_matched_id].filters[kpt_id]
                current_pose.keypoints[kpt_id, 0] = current_pose.filters[kpt_id][0](current_pose.keypoints[kpt_id, 0])
                current_pose.keypoints[kpt_id, 1] = current_pose.filters[kpt_id][1](current_pose.keypoints[kpt_id, 1])
            current_pose.bbox = Pose.get_bbox(current_pose.keypoints)
