import pandas as pd


def transpose_csv(file_in, file_out, sep_symbol, column_name_pos, row_name_pos):
    csv = pd.read_csv(file_in, sep=sep_symbol, header=column_name_pos, index_col=row_name_pos)
    df_csv = pd.DataFrame(data=csv)
    transposed_csv = df_csv.T
    transposed_csv.to_csv(file_out, sep=sep_symbol)


def rm_low_abd_otu():

    input_otu_table         = ''
    output_otu_table        = ''
    output_otu_table_tmp1   = ''
    output_otu_table_tmp2   = ''
    output_otu_table_tmp3   = ''
    abd_cutoff              = 0.01


    otu_table_txt =  '/Users/songweizhi/Desktop/SMP/02_Usearch_BLCA_GTDB_20250325/s07_AllSamples_unoise_otu_table.txt'
    otu_table_txt_t = '/Users/songweizhi/Desktop/SMP/02_Usearch_BLCA_GTDB_20250325/s07_AllSamples_unoise_otu_table_T.txt'
    otu_table_txt_t_filtered = '/Users/songweizhi/Desktop/SMP/02_Usearch_BLCA_GTDB_20250325/s07_AllSamples_unoise_otu_table_T_filtered.txt'
    otu_table_txt_filtered = '/Users/songweizhi/Desktop/SMP/02_Usearch_BLCA_GTDB_20250325/s07_AllSamples_unoise_otu_table_filtered.txt'

    transpose_csv(otu_table_txt, otu_table_txt_t, '\t', 0, 0)

    otu_table_txt_t_filtered_handle = open(otu_table_txt_t_filtered, 'w')
    line_index = 0
    for each_line in open(otu_table_txt_t):
        if line_index == 0:
            otu_table_txt_t_filtered_handle.write(each_line)
        else:
            each_line_split = each_line.strip().split('\t')
            sample_id = each_line_split[0]
            count_list = [int(i) for i in each_line_split[1:]]
            count_sum = sum(count_list)
            count_list_filtered = []
            for each_count in count_list:
                if (each_count/count_sum) >= abd_cutoff:
                    count_list_filtered.append(str(each_count))
                else:
                    count_list_filtered.append('0')
            otu_table_txt_t_filtered_handle.write('%s\t%s\n' % (sample_id, '\t'.join(count_list_filtered)))
        line_index += 1
    otu_table_txt_t_filtered_handle.close()

    transpose_csv(otu_table_txt_t_filtered, otu_table_txt_filtered, '\t', 0, 0)

rm_low_abd_otu()
