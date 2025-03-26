import os
import argparse
import pandas as pd


rm_low_abd_otu_usage = '''
=================== rm_low_abd_otu example commands ===================

BioSAK rm_low_abd_otu -i otu_table.txt -o otu_table_0.001.txt -c 0.001

=======================================================================
'''


def rm_low_abd_otu(args):

    table_in            = args['i']
    value_cutoff        = args['c']
    decimal_round_at    = args['d']
    table_out           = args['o']

    df_in           = pd.read_csv(table_in, sep='\t', header=0, index_col=0)
    df_pct          = df_in.div(df_in.sum(axis=0), axis=1)
    df_pct          = df_pct.round(decimal_round_at)
    df_pct_filtered = df_pct.where(df_pct >= value_cutoff, other=0)
    df_pct_no_zero  = df_pct_filtered[df_pct_filtered.sum(axis=1) != 0]
    df_pct_no_zero.to_csv(table_out, sep='\t')


if __name__ == '__main__':

    blast_parser = argparse.ArgumentParser()
    blast_parser.add_argument('-i', required=True,                              help='input otu count table')
    blast_parser.add_argument('-c', required=False, default=0.001,type=float,   help='relative abundance cutoff, default is 0.001')
    blast_parser.add_argument('-o', required=True,                              help='output otu count table')
    args = vars(blast_parser.parse_args())
    rm_low_abd_otu(args)


'''

otu_table_txt           = '/Users/songweizhi/Desktop/SMP/02_Usearch_BLCA_GTDB/s07_AllSamples_unoise_otu_table_nonEU.txt'
abundance_cutoff        = 0.01
decimal_round_at        = 4
otu_table_txt_filtered  = '/Users/songweizhi/Desktop/SMP/02_Usearch_BLCA_GTDB/s07_AllSamples_unoise_otu_table_nonEU_0.0001.txt'

'''
