import numpy as np
import matplotlib.pyplot as plt

def agg_features(com_features):
    """Aggregate exposure features of all images
        in the community.

    :param: com_features : dict
        photos and it features
           {user1: {photo1: [transformed features], ...}, ...}

    Returns
    -------
        transformed_features : list
            [ [user1's photo1's transformed features], ...]

    """
    features = []

    for user, user_features in com_features.items():
        for photo, photo_features in user_features.items():
            features.append(photo_features)
            #features.append([abs(feature) for feature in (photo_features)])

    features = np.asarray(features)

    return features


def train_clusteror(situ_name, model, com_features, cfg):
    """
    Train clusteror on all images of the community, which will be used
    further to cluster each user's image.

    Parameters
    ----------
    model: object
        clusteror modeling

    com_features : dict
        community exposure features
        dict of all users in a given situation with their clusteror features
            {user1: {photo1:[transformed features], ...}, ...}

    """
    aggfeatures_ = agg_features(com_features)

    if cfg.CLUSTEROR.TYPE == 'K_MEANS':
        model.fit(aggfeatures_)
        centers = model.cluster_centers_
        labels = model.labels_

    elif cfg.CLUSTEROR.TYPE == 'GM':
        model.fit(aggfeatures_)
        centers = model.means_
        labels = model.predict(aggfeatures_)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(aggfeatures_[:,0], aggfeatures_[:,1], c=labels, s=2)
    for i, j in centers:
        ax.scatter(i, j, s=50, c='red', marker='+')
    ax.set_xlabel('object-ness')
    ax.set_ylabel('expo_score')

    fig.savefig('vis_obj_'+situ_name+'.jpg')

    return model