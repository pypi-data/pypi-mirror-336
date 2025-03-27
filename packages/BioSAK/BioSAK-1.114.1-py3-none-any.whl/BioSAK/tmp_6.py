import os

seq_id_txt  = '/Users/songweizhi/Desktop/s06_AllSamples_unoise_nc_vs_nt_formatted2_uniq.txt'
op_dir      = '/Users/songweizhi/Desktop/seq_tax_dir'
cmd_txt     = '/Users/songweizhi/Desktop/esearch_cmds.txt'

cmd_txt_handle = open(cmd_txt, 'w')
for each_id in open(seq_id_txt):
    seq_id = each_id.strip()
    esearch_cmd = 'esearch -db nucleotide -query %s | efetch -format docsum | xtract -pattern DocumentSummary -element TaxId > %s.txt' % (seq_id, seq_id)
    cmd_txt_handle.write(esearch_cmd + '\n')
cmd_txt_handle.close()
