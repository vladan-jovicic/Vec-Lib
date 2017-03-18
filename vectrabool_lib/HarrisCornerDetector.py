import cv2
import sys
import numpy as np



class HarrisCornerDetector:
    def __init__(self, points, cl_threshold=1.5, corner_threshold=0.45, block_size=2, kernel_size=7, kfree=0.01):
        self.points = points
        self.corner_threshold = corner_threshold
        self.cluster_threshold = cl_threshold
        self.block_size, self.kernel_size, self.kfree = block_size, kernel_size, kfree

    def get_corners(self):
        """
        :return: the set of indices of corners
        """
        # compute minimum/maximum by x and y
        max_x, max_y = -1, -1  # np.max(self.points, axis=0)
        min_y = min_x = np.max(self.points)
        for point in self.points:
            # print(point[0], point[1])
            max_x = max(max_x, point[0])
            max_y = max(max_y, point[1])
            min_x = min(min_x, point[0])
            min_y = min(min_y, point[1])
        # convert to int
        max_x, max_y, min_x, min_y = int(max_x), int(max_y), int(min_x), int(min_y)
        # create black image with white line
        image = np.zeros((max_y + 10, max_x + 10), dtype=np.uint8)
        for i in range(1, len(self.points)):
            start_point = (int(self.points[i-1][0]), int(self.points[i-1][1]))
            end_point = (int(self.points[i][0]), int(self.points[i][1]))
            cv2.line(image, start_point, end_point, 155, 1)  # bilo 200

        dst = cv2.cornerHarris(image, self.block_size, self.kernel_size, self.kfree)
        dst = cv2.dilate(dst, None)
        corners_in_image = np.argwhere(dst > self.corner_threshold * dst.max())  # coordinates with respect to image

        # all possible corners are in the array: extract the best ones
        clusters = []
        for i in range(len(corners_in_image)):
            curr_point = np.array(corners_in_image[i])
            found, cl_idx = False, -1
            for curr_idx, cluster in enumerate(clusters):
                dist = min([np.linalg.norm(curr_point - np.array(corners_in_image[j])) for j in cluster])  # ovdje je greska
                if dist < self.cluster_threshold:
                    found, cl_idx = True, curr_idx
                    break

            # if cluster is found
            if found:
                # the ith point belongs to this cluster
                clusters[cl_idx].append(i)
            else:  # if the cluster is not found
                clusters.append([i])

        # everything is alright
        corresponding_clusters = []
        for cluster in clusters:  # fix one cluster and compute points corresponding to that cluster
            curr_cluster = []
            for idx, point in enumerate(self.points):  # check all points that are close to the fixed cluster
                # compute the distance between point and the cluster, corresponding to the coord system
                dist = min([np.linalg.norm(np.array([int(point[1]), int(point[0])]) - np.array(corners_in_image[i])) for i in cluster])
                if dist < self.cluster_threshold:
                    curr_cluster.append(idx)
            corresponding_clusters.append(curr_cluster)

        # each corresponding cluster represents one corner
        # pick the best one
        corners = []
        # maybe to try one that is surrounded with
        # the one that have the most
        for cluster in corresponding_clusters:
            if len(cluster) == 0:
                continue
            if 1 <= len(cluster) <= 2:  # improve also this
                corners.append(cluster[0])
            best_idx, best_dist = -1, 0
            for i in range(1, len(cluster)-1):
                pt1 = np.array(self.points[i-1])
                pt2 = np.array(self.points[i+1])
                pt3 = np.array(self.points[i])
                dist = np.linalg.norm(np.cross(pt2 - pt1, pt1 - pt3))/np.linalg.norm(pt2 - pt1)
                best_idx, best_dist = (i, dist) if dist > best_dist else (best_idx, best_dist)
            corners.append(cluster[best_idx])

        tmp_corners = sorted(corners)
        if len(corners) == 0:
            return corners
        corners = [tmp_corners[0]]
        for i in range(1, len(tmp_corners)):
            if tmp_corners[i]-corners[-1] > 2:
                corners.append(tmp_corners[i])
        return tmp_corners
