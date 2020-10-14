"""
This file generates .slurm files to fine-tune models

Usage:

    python gen_slurm.py -f fine_tune_bank.slurm -p gpu-test -n node21 -e 1 -s BANK -d MOBI
"""
import argparse


def argument_parser():
    """
    Create a parser with some common arguments.

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="fine_tune_bank.slurm", help="saved slurm file name")
    parser.add_argument("-p", "--partition", required= True, help= "partition of node")
    parser.add_argument("-n", "--node", default="", required=True, help="node where to train models")
    parser.add_argument("-e", "--exclusive", required=True, help="1 to turn on the exclusive mode")
    parser.add_argument("-s", "--situation", required=True, help="IT, ACCOM, BANK, WAIT")
    parser.add_argument("-d", "--detector", required=True, help="MOBI, FRCNN")

    return parser

def main():
    """

    Returns
    -------

    """

    EPSs = [0.05, 0.1, 0.15, 0.2]
    KEEPs = [0.8, 0.85, 0.9, 0.95, 1.0]
    FEATURE_TYPEs = ['VOTE', 'ORG']
    args = argument_parser().parse_args()
    writer = open(args.file,'w')
    writer.write('#!/bin/bash\n# SBATCH -N 1\n#SBATCH -n 1\n')
    writer.write('#SBATCH --partition %s\n#SBATCH -w %s\n'%(args.partition, args.node))

    if args.exclusive == '1':
        writer.write('#SBATCH --exclusive\n')
    writer.write('#SBATCH -J FT\n')

    writer.write('# SBATCH --output=%s\n'%(args.file.replace('slurm','out')))
    writer.write('# SBATCH --error=%s\n'%(args.file.replace('slurm', 'errs')))
    writer.write('\n')

    common_part = 'python3 ft0_user_selector.py --config_file ../configs/'
    save_model = args.file.split('.slurm')[0]
    out_dir = args.file.split('.slurm')[0]
    counter = 0

    for eps in EPSs:
        for keep in KEEPs:
            for feature in FEATURE_TYPEs:
                if args.detector == 'MOBI':
                    model_part = common_part+'mobi_rf_kmeans.yaml --model_name '+save_model+'_'+str(counter)+'.pkl '+'--situation= '+args.situation
                elif args.detector == 'FRCNN':
                    model_part = common_part+'rcnn_rf_kmeans.yaml --model_name '+save_model+'_'+str(counter)+'.pkl '+'--situation= '+args.situation
                param_part = model_part+' --opts'+' USER_SELECTOR.EPS '+str(eps)+' USER_SELECTOR.KEEP '+str(keep)+' SOLVER.FEATURE_TYPE '+str(feature)+' OUTPUT.DIR '+out_dir
                writer.write(param_part+'\n')
                counter += 1

if __name__ == '__main__':
    main()