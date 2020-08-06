import numpy as np
import scipy.spatial.distance as distance
from numpy import linalg as LA

def unique_threshold(x_unique):
    """

    :param x_unique:
    :return:
    """
    count = 0
    sum_distance = 0
    print("-------++++++++++++++---------------")
    for i in range(x_unique.shape[0]):
        for j in range(i + 1,x_unique.shape[0]):
            count += 1
            print(distance.correlation(x_unique[i,:],x_unique[j,:]))
            sum_distance += distance.correlation(x_unique[i,:],x_unique[j,:])

    avg_distance = sum_distance / count

    return  avg_distance

def detect_same_y_test(x_test, y_test, agv_distance_situ):
    """

    :param x_test:
    :param y_test:
    :param sum_situ:
    :return:
    """
    for i in range(x_test.shape[0]):
        for j in range(i+1, x_test.shape[0]):
            dist = distance.correlation(x_test[i,:], x_test[j,:])
            if dist > agv_distance_situ:
                print('val1: ',y_test[i],'  val2: ',y_test[j])
                print('diff = ',dist)


def train_test_observe(train_test_batch_situs):
    """

    :return:
    """
    print("##########################")
    for situ, data in train_test_batch_situs.items():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(' ',situ)
        y_train = data['y_train']
        y_test = data['y_test']
        x_train = data['x_train']
        x_test = data['x_test']

        y_unique_train = list(np.unique(y_train))

        sum_distance_situ = 0
        count = 0

        for y_unique in y_unique_train:
            indexes = np.where(y_train == y_unique)[0]
            if indexes.shape[0] > 1:
                count += 1
                x_unique = x_train[indexes, :]
                avg_distance = unique_threshold(x_unique)
                sum_distance_situ += avg_distance

        agv_distance_situ = sum_distance_situ / count
        print('sum_diff_situ: ', agv_distance_situ)
        detect_same_y_test(x_test, y_test, agv_distance_situ)


    assert 1 == 2
