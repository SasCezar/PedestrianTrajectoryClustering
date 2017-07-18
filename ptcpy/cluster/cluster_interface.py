from abc import ABCMeta, abstractmethod


class ClusterInterface(metaclass=ABCMeta):
    """
    Interface covering basic clustering functionality.
    """

    @abstractmethod
    def cluster(self, vectors):
        """
        Assigns the vectors to clusters, learning the clustering parameters
        from the data. Returns a cluster identifier for each vector.
        :param vectors:
        :return:
        """

    @abstractmethod
    def classify(self, token):
        """
        Classifies the token into a cluster, setting the token's CLUSTER
        parameter to that cluster identifier.
        :param token:
        :return:
        """
