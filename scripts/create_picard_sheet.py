import argparse
import pandas as pd
from path import Path



def create_picard_sheet(sample_sheet_df: pd.DataFrame, out_fp: str, is_test: bool=False):
    samples_df = (sample_sheet_df[['Sample_ID', 'index', 'index2']]
                    .rename(columns={'Sample_ID': 'OUTPUT_PREFIX',
                                     'index': 'BARCODE_1',
                                     'index2': 'BARCODE_2'}))
    if is_test:
        search_ids = ['SEARCH-8686',
              'SEARCH-8702',
              'SEARCH-8708',
              'SEARCH-8720',
              'SEARCH-8722',
              'SEARCH-8732',
              'SEARCH-8749',
              'SEARCH-8770',
             ]
        samples_df = samples_df.loc[samples_df['OUTPUT_PREFIX'].isin(search_ids)]
    samples_df.to_csv(out_fp, sep='\t', index=False)
    return 0


def create_picard_barcodes(sample_sheet_df: pd.DataFrame, out_fp: str, is_test: bool=False):
    barcodes_df = (sample_sheet_df[['Sample_ID', 'index', 'index2']]
                    .rename(columns={'Sample_ID': 'barcode_name',
                                     'index': 'barcode_sequence_1',
                                     'index2': 'barcode_sequence_2'}))
    if is_test:
        search_ids = ['SEARCH-8686',
              'SEARCH-8702',
              'SEARCH-8708',
              'SEARCH-8720',
              'SEARCH-8722',
              'SEARCH-8732',
              'SEARCH-8749',
              'SEARCH-8770',
             ]
        barcodes_df = barcodes_df.loc[barcodes_df['barcode_name'].isin(search_ids)]
    barcodes_df.to_csv(out_fp, sep='\t', index=False)
    return 0



if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', "--sample-sheet", type=str, 
                        help="Filepath to original sample sheet (TSV)")
    parser.add_argument('-o', "--out-dir", type=str, 
                        help="Output directory containing Picard's fastq files")
    parser.add_argument('-t', "--test", type=bool, 
                        help="FLAG for whether the execution is for testing purposes")
    args = parser.parse_args()

    sample_sheet_fp = Path(args.sample_sheet)
    out_dir = Path(args.out_dir)
    is_test = args.test
    if not Path.isdir(out_dir):
        raise ValueError("The user-specified output directory (arg --out-dir) does not Exist. Operations aborted.")
    if not Path.isfile(sample_sheet_fp):
        raise ValueError("The user-specified sample sheet (arg --sample-sheet) does not Exist. Operations aborted.")
    sample_sheet_df = pd.read_csv(sample_sheet_fp, skiprows=19)
    create_picard_sheet(sample_sheet_df.copy(), out_fp=f'{out_dir}/picard_experiment_sheet.tsv', is_test=is_test)
    create_picard_barcodes(sample_sheet_df.copy(), out_fp=f'{out_dir}/picard_experiment_barcodes.tsv', is_test=is_test)