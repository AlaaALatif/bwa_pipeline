import glob
import shutil
import argparse
from path import Path


def rename_picard_fastq(fastq_filepaths: list, lane: str, destination_folder: str):
    for fp in fastq_filepaths:
        s_id = fp.split('/')[-1].split('.')[0]
        _rnd = fp.split('/')[-1].split('.')[1]
        if len(_rnd)==1:
            rnd = f"R{fp.split('/')[-1].split('.')[1]}"
        else:
            rnd = fp.split('/')[-1].split('.')[1].replace('barcode_', 'I')
        new_filename = f'{s_id}_S0_{lane}_{rnd}_001.fastq.gz'
        new_fp = f'{destination_folder}/{new_filename}'
        shutil.move(fp, new_fp)
#         print(new_fp)
    return 0


if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', "--out-dir", action='store_false', 
                        help="Output directory containing Picard's fastq files")
    args = parser.parse_args()

    # whether or not to include bam files in the release
    out_dir = args.out_dir
    if not Path.isdir(out_dir):
        raise ValueError("The user-specified output directory (arg --out-dir) does not Exist. Operations aborted.")
    l1_fastq_fps = glob.glob(f'{out_dir}/lane_1_tmp/*.fastq.gz')
    if len(l1_fastq_fps)==0:
        raise ValueError("The user-specified output directory (arg --out-dir) does not contain FASTQ files for lane 1. Operations aborted.")
    rename_picard_fastq(l1_fastq_fps, lane='L001', destination_folder=f'{out_dir}/all_fastqs')
    print(f"Lane 1 FASTQ files renamed and stored in all_fastqs folder")
    l2_fastq_fps = glob.glob(f'{out_dir}/lane_2_tmp/*.fastq.gz')
    if len(l2_fastq_fps)==0:
        raise ValueError("The user-specified output directory (arg --out-dir) does not contain FASTQ files for lane 2. Operations aborted.")
    rename_picard_fastq(l2_fastq_fps, lane='L002', destination_folder=f'{out_dir}/all_fastqs')
    print(f"Lane 2 FASTQ files renamed and stored in all_fastqs folder")