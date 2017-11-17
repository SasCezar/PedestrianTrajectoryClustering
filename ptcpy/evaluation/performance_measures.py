import numpy as np
from sklearn.metrics import adjusted_rand_score, precision_recall_fscore_support


def get_intersection_matrix(clustered_pedestrians, ground_truth):
    clusters_number = len(set(clustered_pedestrians.values()))
    ground_clusters_number = len(set(ground_truth.values()))
    size = max(clusters_number, ground_clusters_number)

    clusters_members = {}
    for pedestrian_id in clustered_pedestrians:
        cluster_number = clustered_pedestrians[pedestrian_id]
        clusters_members[cluster_number] = clusters_members[cluster_number] + [
            pedestrian_id] if cluster_number in clusters_members else [pedestrian_id]

    ground_clusters_members = {}
    for pedestrian_id in ground_truth:
        cluster_number = ground_truth[pedestrian_id]
        ground_clusters_members[cluster_number] = ground_clusters_members[cluster_number] + [
            pedestrian_id] if cluster_number in ground_clusters_members else [pedestrian_id]

    intersection_count = np.zeros(shape=(ground_clusters_number, clusters_number))

    for ground_key in ground_clusters_members:
        for cluster_key in clusters_members:
            a = ground_clusters_members[ground_key]
            b = clusters_members[cluster_key]
            intersection = list(set(a) & set(b))
            intersection_count[ground_key, cluster_key] = len(intersection)

    return intersection_count


def equivalence_classes(confusion_matrix):
    return np.argmax(confusion_matrix, axis=0)


def get_performance_measures(clustered_pedestrian, ground_truth):
    intersection = get_intersection_matrix(clustered_pedestrian, ground_truth)
    equivalences = equivalence_classes(intersection)

    sorted_pedestrian = sorted(clustered_pedestrian.items(), key=lambda x: x[0])
    predicted = [value for key, value in sorted_pedestrian]
    sorted_gt = sorted(ground_truth.items(), key=lambda x: x[0])
    gt = [(lambda x: list(equivalences).index(x) if x in equivalences else x)(value) for key, value in sorted_gt]

    precision, recall, f1, support = precision_recall_fscore_support(gt, predicted, average='micro')

    return precision, recall, f1, support


def rand_score_measure(clustered_pedestrian, ground_truth):
    predicted_label = []
    true_label = []
    for user_id in ground_truth:
        predicted_label += [clustered_pedestrian[user_id]]
        true_label += [ground_truth[user_id]]

    score = adjusted_rand_score(true_label, predicted_label)

    return score
