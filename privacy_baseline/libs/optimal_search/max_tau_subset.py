
import numpy as np
from correlation import corr


def select_subset(detectors, tau_fix):
    """
    Select a subset whose detector taus are greater than tau_fix

    :param: detectors: dict
        {detector1: (tau_max1, threshold1, score1), ...}

    :param: tau_fix: float

    :return:
        tau_detectors: dict
            {detector1: (threshold1, score1), ...}

    """
    tau_detectors = {}
    for detector, tau_thres_score in detectors.items():
        if tau_thres_score[0] >= tau_fix:
            tau_detectors[detector] = (tau_thres_score[1], tau_thres_score[2])
    
    return tau_detectors


def tau_subset(users, gt_user_expo, detectors, corr_type):
    """
    Estimate the best correlation score for a subset tau_detectors

    :param: users
        users in a situation and its photos
            {user1: {photo1: {class1: [obj1, ...], ...}}, ...}, ...}
            
    :param gt_user_expo: dict
        user expo in a given situation
            {user1: avg_score, ...}
    
    :param: detectors: dict
        {detector1: (tau_max1, threshold1, score1), ...}
    
    :param corr_type: string

    :return:

    """
    tau_estimate_list = []
    tau_fixes = list(np.linespace(-1,1,201))
    
    for tau_fix in tau_fixes:
        tau_detectors = select_subset(detectors, tau_fix) #select subset
        tau_est = corr(users, gt_user_expo, tau_detectors, corr_type)
        tau_estimate_list.append(tau_est)

    tau_max = max(tau_estimate_list)

    return tau_max