import random
import numpy as np


def train_test_split(regression_features, gt_expo_scores, train_ratio):
    """Split data into train and test set for a given situation

    :param: regression_features : dict
        indiviual user and its feature
            {user1: [feature1,...], ...}

    :param: gt_expo_scores : dict
        user and its ground truth crowd-sourcing user exposure scores
            {user1: avg_score, ...}
    Returns
    -------
        situ_data : dict

            with following fields

                X_train, X_test : numpy array
                    (N, #features)

                Y_train, Y_test : numpy array
                    (N, )
    """
    nb_users = len(list(gt_expo_scores.keys()))
    nb_user_not_consistent = 0
    X = []
    Y = []
    for user, score in gt_expo_scores.items():
        if user in regression_features:
            Y.append(score)
            X.append(regression_features[user])
        else:
            nb_user_not_consistent += 1

    X = np.asarray(X)
    Y = np.asarray(Y)

    indexes = np.linspace(0, nb_users-nb_user_not_consistent -1, nb_users - nb_user_not_consistent, dtype=np.int32)
    random.shuffle(indexes)

    train_index = indexes[:int(nb_users*train_ratio)]
    test_index = indexes[int(nb_users*train_ratio):]

    situ_data = {'x_train': X[train_index, :], 'y_train': Y[train_index],
                 'x_test': X[test_index, :], 'y_test': Y[test_index]}

    print('     nb of users: ', nb_users - nb_user_not_consistent)
    print('     train profiles:',train_index.shape[0])

    return situ_data


def train_test_split_situ(regress_feature_situs, gt_user_expo_situs, train_ratio = 0.8):
    """Train test split by situation

    :param: regress_feature_situs: dict
        user regression features in each situation
        {situ1: {user1: [feature1,...], ...}, ...}

    :param: gt_user_expo_situs: dict
        users and its ground truth crowd-sourcing user exposure scores in each situation
            {situ1: {user1: avg_score, ...}, ...}

    Returns
    -------
        train_test_situs: dict
            train and test data in each situation
                {situ1: {'x_train': ,'y_train': ,'x_test': ,'y_test': }, ...}
    """
    train_test_situs = {}

    for situ, gt_expo_user_scores in gt_user_expo_situs.items():
        print('  ',situ)
        train_test_situs[situ] = train_test_split(regress_feature_situs[situ],gt_expo_user_scores, train_ratio)

    return train_test_situs