from exposure.photo import photo_exposure


def user_expo(photos, detectors, cfg):
    """Estimate user exposure

    :param photos: dict
        user photos and its detected objects
            {photo1: {class1: [obj1, ...], ...}}, ...}

    :param detectors: dict
         {detector: (threshold, object_score),...} for not inference_mode
        {detector1: object_score, ...} for inference_mode
    :param cfg:

    :return:
        user_score: float
    """

    user_score = 0
    cardinality = 0
    for photo, detected_objects in photos.items():

        photo_score, active_state = photo_exposure(detected_objects, detectors, cfg)
        user_score += photo_score

        if active_state:
            cardinality += 1

    if cardinality != 0:
        user_score = user_score / cardinality

    return user_score


def user_expo_situ(users, detectors, cfg):
    """

    :param users:
        users in a situation and its photos
            {user1: {photo1: {class1: [obj1, ...], ...}}, ...}, ...}

    :param detectors: dict
        {detector1: (threshold, object_score), ...}

    :param cfg:

    :return:
        community_expo: dict
            {user1: score, ...}

    """
    community_expo = {}
    for user, photos in users.items():
        community_expo[user] = user_expo(photos, detectors, cfg)

    return community_expo
