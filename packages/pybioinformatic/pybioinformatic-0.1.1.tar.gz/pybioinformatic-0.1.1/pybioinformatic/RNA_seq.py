"""
File: RNA_seq.py
Description: RNA-seq analysis module.
CreateDate: 2024/7/24
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import TextIOWrapper
from typing import Literal, Union
from os import makedirs
from os.path import abspath, exists
from shutil import which
from natsort import natsort_key
from tqdm import tqdm
from scipy.stats import pearsonr
from statsmodels.stats.multitest import multipletests
from pandas import DataFrame, Series, concat
from pybioinformatic.gtf import Gtf
from pybioinformatic.task_manager import TaskManager


def parse_sample_info(sample_info: TextIOWrapper) -> dict:
    d = {}  # {sample_name: [fastq_file1, fastq_file2], ...}
    for line in sample_info:
        split = line.strip().split('\t')
        d[split[0]] = split[1:4]
    return d


class MergeSamples:
    def __init__(self,
                 hisat2_bam: set,
                 stringtie_gtf: set):
        self.hisat2_bam = hisat2_bam
        self.stringtie_gtf = stringtie_gtf


class StrandSpecificRNASeqAnalyser:
    """
    \033[32m
    Strand-specific (dUTP constructed library) pair end transcriptome analyser.
    \033[0m
    \033[34m
    :param read1: Strand-specific pair end read1 fastq file.
    :param read2: Strand-specific pair end read2 fastq file.
    :param ref_genome: Reference genome fasta file.
    :param ref_gff: Reference genome gff file.
    :param output_path: Output path.
    :param num_threads: Number of threads.
    :param sample_name: Sample name.
    \033[0m
    """

    def __init__(self,
                 read1: str,
                 read2: str,
                 ref_genome: str,
                 ref_gff: str ,
                 output_path: str,
                 num_threads: int = 10,
                 sample_name: str = None):
        """
        :param read1: Strand-specific pair end read1 fastq file.
        :param read2: Strand-specific pair end read2 fastq file.
        :param ref_genome: Reference genome fasta file.
        :param ref_gff: Reference genome gff file.
        :param output_path: Output path.
        :param num_threads: Number of threads.
        :param sample_name: Sample name.
        """
        self.read1 = abspath(read1)
        self.read2 = abspath(read2)
        self.ref_genome = abspath(ref_genome)
        self.ref_gff = abspath(ref_gff)
        self.gff_to_gtf()
        self.num_threads = num_threads
        self.output_path = abspath(output_path)
        if sample_name is None:
            self.sample_name = self.read1.split('/')[-1].split('.')[0]
        else:
            self.sample_name = sample_name

    def gff_to_gtf(self,
                   gffread_exe: str = 'gffread'):
        gffread_exe = which(gffread_exe)
        gtf = '.'.join(self.ref_gff.split('.')[:-1]) + '.gtf'
        cmd = f"{gffread_exe} {self.ref_gff} -T -o {gtf}"
        self.ref_gtf = gtf
        return cmd

    @staticmethod
    def __other_options(options_dict: dict, command: str):
        for option, value in options_dict.items():
            if len(option) == 1:
                command += f'-{option} {value} '
            else:
                command += f'--{option} {value} '
        return command

    def run_fastp(self,
                  q_value: int = 20,
                  fastp_exe: str = 'fastp',
                  **kwargs) -> str:
        """
        \n\nRaw reads quality control.
        \n\033[1m:param:\033[0m
        fastp_exe: fastp executable file path. (type=str)
        q_value: Minimum quality value of base. (type=int, default=20)
        kwargs: Other options of fastp.
        \n\033[1m:return:\033[0m
        Fastp command. (type=str)
        """
        fastp_exe = which(fastp_exe)  # Get fastp executable file absolute path.
        out_path = f'{self.output_path}/01.QC/{self.sample_name}'
        makedirs(out_path, exist_ok=True)
        if self.read2:
            cmd = f"{fastp_exe} " \
                  f"-w {self.num_threads} " \
                  f"-q {q_value} " \
                  f"-i {self.read1} " \
                  f"-I {self.read2} " \
                  f"-o {out_path}/{self.sample_name}_R_clean.fq.gz " \
                  f"-O {out_path}/{self.sample_name}_F_clean.fq.gz " \
                  f"-j {out_path}/{self.sample_name}.fastp.json " \
                  f"-h {out_path}/{self.sample_name}.fastp.html "
            self.clean1 = f'{out_path}/{self.sample_name}_R_clean.fq.gz'
            self.clean2 = f'{out_path}/{self.sample_name}_F_clean.fq.gz'
        else:
            cmd = f"{fastp_exe} -w {self.num_threads} -q {q_value} -i {self.read1} -o {out_path}/{self.sample_name}_clean.fq.gz "
            self.clean1 = f'{out_path}/{self.sample_name}_clean.fq.gz'
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd

    def run_hisat2(self,
                   build_index: bool = False,
                   hisat2_exe: str = 'hisat2',
                   samtools_exe: str = 'samtools',
                   storer: MergeSamples = None,
                   **kwargs):
        cmd = ''
        hisat2_exe = which(hisat2_exe)
        samtools_exe = which(samtools_exe)
        out_path = f'{self.output_path}/02.mapping/{self.sample_name}'
        makedirs(out_path, exist_ok=True)
        if build_index:
            cmd += f"{hisat2_exe}-build -x {self.ref_genome} {self.ref_genome}\n"
        cmd += f"{hisat2_exe} " \
               f"--rna-strandness RF " \
               f"-p {self.num_threads} " \
               f"-x {self.ref_genome} " \
               f"-1 {self.clean1} " \
               f"-2 {self.clean2} " \
               f"--summary-file {out_path}/{self.sample_name}.ht2.log | " \
               f"{samtools_exe} sort " \
               f"-@ {self.num_threads} " \
               f"-T {self.sample_name} - > {out_path}/{self.sample_name}.ht2.sort.bam "
        self.sort_bam = f'{out_path}/{self.sample_name}.ht2.sort.bam'
        if storer:
            storer.hisat2_bam.add(f'{out_path}/{self.sample_name}.ht2.sort.bam')
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd

    def run_stringtie(self,
                      stringtie_exec: str = 'stringtie',
                      storer: MergeSamples = None,
                      **kwargs):
        stringtie_exec = which(stringtie_exec)
        out_path = f'{self.output_path}/03.assembly/{self.sample_name}'
        makedirs(out_path, exist_ok=True)
        cmd = f"{stringtie_exec} " \
              f"--rf " \
              f"-p {self.num_threads} " \
              f"-l {self.sample_name} " \
              f"-A {out_path}/{self.sample_name}_gene_abundance.st.xls " \
              f"-o {out_path}/{self.sample_name}.st.gtf " \
              f"{self.sort_bam} "
        if storer:
            storer.stringtie_gtf.add(f'{out_path}/{self.sample_name}.st.gtf')
        if self.ref_gff:
            cmd += f"-G {self.ref_gff} "
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd

    def run_stringtie_merge(self,
                            gtf_list: list,
                            m: int = 200,
                            c: float = 1.0,
                            F: float = 0.5,
                            g: int = 500,
                            stringtie_exec: str = 'stringtie',
                            **kwargs):
        stringtie_exec = which(stringtie_exec)
        out_path = f'{self.output_path}/03.assembly'
        makedirs(out_path, exist_ok=True)
        gtf_list.sort(key=natsort_key)
        gtf_files = ' '.join(gtf_list)
        cmd = f"{stringtie_exec} --merge " \
              f" -p {self.num_threads} " \
              f"-m {m} -c {c} -F {F} -g {g} " \
              f"-o {out_path}/All.stringtie.gtf " \
              f"{gtf_files} "
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd

    def run_cuffcompare(self,
                        cuffcompare_exe: str = 'cuffcompare',
                        gffread_exe: str = 'gffread_exe'):
        cuffcompare_exe = which(cuffcompare_exe)
        gffread_exe = which(gffread_exe)
        out_path = f'{self.output_path}/03.assembly'
        makedirs(out_path, exist_ok=True)
        gff_to_gtf = self.gff_to_gtf(gffread_exe=gffread_exe)
        mv = f"mv $PWD/cuffcompare.* {out_path}/"
        extract_gtf = fr'''awk -F'\t' '$3~/[uxijo]/' {out_path}/cuffcompare.All.stringtie.gtf.tmap | cut -f 5 | grep -Fwf - {out_path}/cuffcompare.combined.gtf | awk -F'\t' '$7 != "."' > {out_path}/novel_transcript.gtf'''
        extract_novel_transcript_seq = (
            f"{gffread_exe} -g {self.ref_genome} -w {out_path}/novel_transcript.fa {out_path}/novel_transcript.gtf\n"
            f"{gffread_exe} -g {self.ref_genome} -y {out_path}/novel_transcript_pep.fa {out_path}/novel_transcript.gtf"
        )
        merge_gtf = f"cat {self.ref_gtf} {out_path}/novel_transcript.gtf > {out_path}/All.gtf"
        cmd = (f"{gff_to_gtf}\n"
               f"{cuffcompare_exe} -r {self.ref_gtf} -R -o cuffcompare {out_path}/All.stringtie.gtf\n{mv}\n"
               f"{extract_gtf}\n"
               f"{extract_novel_transcript_seq}\n"
               f"{merge_gtf}")
        self.ref_gtf = f'{out_path}/All.gtf'
        return cmd

    def run_featureCounts(self,
                          bam_list: list,
                          anno_file: Literal['gff', 'gtf'] = 'gtf',
                          feature_type: str = 'exon',
                          count_unit: str = 'transcript_id',
                          featureCounts_exec: str = 'featureCounts',
                          **kwargs):
        featureCounts_exec = which(featureCounts_exec)
        anno_file = self.ref_gtf if anno_file == 'gtf' else self.ref_gff
        out_path = f'{self.output_path}/04.expression'
        makedirs(out_path, exist_ok=True)
        bam_list.sort(key=natsort_key)
        bam_files = ' '.join(bam_list)
        cmd = f"{featureCounts_exec} " \
              f"-t {feature_type} " \
              f"-g {count_unit} " \
              f"-fMO -p --countReadPairs " \
              f"-s 2 " \
              f"-T {self.num_threads} " \
              f"-a {anno_file} " \
              f"-o {out_path}/featureCounts.xls " \
              f"{bam_files} " \
              f"2> {out_path}/featureCounts.log "
        if kwargs:
            cmd = self.__other_options(options_dict=kwargs, command=cmd)
        return cmd


class LncRNAPredictor:
    def __init__(self,
                 nucl_fasta_file: str,
                 num_thread: int,
                 output_path: str,
                 module: Literal['ve', 'pl'],
                 pep_fasta_file: str = None):
        self.nucl = abspath(nucl_fasta_file)
        self.pep = abspath(pep_fasta_file) if pep_fasta_file else None
        self.output_path = abspath(output_path)
        self.num_thread = num_thread
        self.module = module

    def run_CNCI(self, CNCI_exec: str = 'CNCI.py'):
        CNCI = which(CNCI_exec)
        cmd = f'{CNCI} -p {self.num_thread} -m {self.module} -f {self.nucl} -o {self.output_path}/CNCI'
        return cmd

    def run_CPC2(self, CPC2_exec: str = 'CPC2.py', ):
        CPC2 = which(CPC2_exec)
        makedirs(f'{self.output_path}/CPC2', exist_ok=True)
        cmd = f'{CPC2} -i {self.nucl} --ORF TRUE -o {self.output_path}/CPC2/CPC2'
        return cmd

    def run_PLEK(self, PLEK_exec: str = 'PLEK'):
        makedirs(f'{self.output_path}/PLEK', exist_ok=True)
        cmd = f'{PLEK_exec} -thread {self.num_thread} -fasta {self.nucl} -out {self.output_path}/PLEK/PLEK.xls'
        return cmd

    def run_PfamScan(self,
                     PfamDatabase: str,
                     PfamScan_exec: str = 'pfam_scan.pl'):
        PfamScan = which(PfamScan_exec)
        cmd = (f'{PfamScan} '
               f'-fasta {self.pep} '
               f'-dir {PfamDatabase} '
               f'-outfile {self.output_path}/PfamScan/pfamscan_out.txt')
        return cmd

    def merge_results(self,
                      CNCI_results: str = None,
                      CPC2_results: str = None,
                      PLEK_results: str = None,
                      PfamScan_results: str = None,
                      seqkit_exec: str = 'seqkit'):
        seqkit = which(seqkit_exec)
        CNCI_results = r'''awk -F'\t' '{if($2 == "noncoding"){print $1}}' %s | awk -F' ' '{print $1}' ''' % CNCI_results
        CPC2_results = r'''awk -F'\t' '{if($9 == "noncoding"){print $1}}' %s''' % CPC2_results
        PLEK_results = r'''awk -F'\t' '{if($1 == "Non-coding"){print $3}}' %s | sed 's/>//;s/ gene.*//' ''' % PLEK_results
        awk1 = r'''awk -F' ' '{if($1 == 3){print $2}}' '''
        awk2 = r'''awk -F' ' '{print $1}' %s''' % PfamScan_results
        seqkit_cmd1 = f'{seqkit} grep -f - {self.nucl}'
        seqkit_cmd2 = f'{seqkit} seq -m 200 -'
        cmd = f'cat <({CNCI_results}) <({CPC2_results}) <({PLEK_results}) | sort | uniq -c | {awk1} | grep -vFwf <({awk2}) - | {seqkit_cmd1} | {seqkit_cmd2} > {self.output_path}/lncRNA.fa'
        return cmd


class LncRNATargetPredictor:
    def __init__(self,
                 lncRNA_gtf_file: Union[str, TextIOWrapper] = None,
                 mRNA_gtf_file: Union[str, TextIOWrapper] = None,
                 distance: int = 100000,
                 lncRNA_exp_file: Union[str, TextIOWrapper] = None,
                 mRNA_exp_file: Union[str, TextIOWrapper] = None,
                 lncRNA_min_exp: float = 0.5,
                 mRNA_min_exp: float = 0.5,
                 r: float = 0.85,
                 FDR: float = 0.05,
                 q_value: float = 0.05,
                 num_processing: int = 1,
                 output_path: str = '.'):
        self.lncRNA_gtf = abspath(lncRNA_gtf_file)
        self.lncRNA_exp = abspath(lncRNA_exp_file)
        self.lncRNA_min_exp = lncRNA_min_exp
        self.mRNA_gtf = abspath(mRNA_gtf_file)
        self.mRNA_exp = abspath(mRNA_exp_file)
        self.mRNA_min_exp = mRNA_min_exp
        self.distance = distance
        self.r, self.FDR, self.q_value = r, FDR, q_value
        self.num_processing = num_processing
        self.output_path = abspath(output_path)

    @staticmethod
    def intersect(row: Series, mRNA: DataFrame, distance: int):
        lncRNA_chr = row['Chromosome']
        lncRNA_start, lncRNA_end = row['Start'], row['End']
        start = lncRNA_start - distance if lncRNA_start - distance > 0 else 1
        end = lncRNA_end + distance
        lncRNA_strand = row['Strand']
        candidate_mRNA = mRNA[
            (mRNA['Chromosome'] == lncRNA_chr) &
            (start <= mRNA['Start']) &
            (end >= mRNA['End'])
            ]
        candidate_mRNA['LncRNA_id'] = row.name
        candidate_mRNA['LncRNA_start'] = lncRNA_start
        candidate_mRNA['LncRNA_end'] = lncRNA_end
        candidate_mRNA['LncRNA_strand'] = lncRNA_strand
        return candidate_mRNA

    def co_location(self):
        with Gtf(self.lncRNA_gtf) as lncRNA_gtf, Gtf(self.mRNA_gtf) as mRNA_gtf:
            lncRNA_df = lncRNA_gtf.merge_by_transcript()
            mRNA_df = mRNA_gtf.merge_by_transcript()
            lncRNA_df.to_csv(f'{self.output_path}/lncRNA.bed', sep='\t')
            mRNA_df.to_csv(f'{self.output_path}/mRNA.bed', sep='\t')
            params = ((row[1], mRNA_df, self.distance) for row in lncRNA_df.iterrows())
            tkm = TaskManager(num_processing=self.num_processing, params=params)
            with tqdm(total=len(lncRNA_df), desc='Co-location predicting') as pbar:
                rets = tkm.parallel_run_func(func=self.intersect, call_back_func=lambda _: pbar.update())
            dfs = [ret.get() for ret in rets]
            lncRNA_mRNA_df = concat(dfs)
            lncRNA_mRNA_df.to_csv(f'{self.output_path}/co_loc.xls', sep='\t')

    @staticmethod
    def sub_process(x_name, x_data, y_name, y_data):
        r, p = pearsonr(x_data, y_data)
        return [x_name, y_name, r, p]

    def co_expression(self):
        lncRNA_exp_dict = {
            line.strip().split('\t')[0]: [float(i) for i in line.strip().split('\t')[1:]]
            for line in open(self.lncRNA_exp)
            if not line.startswith('Geneid') and line.strip() and
               all([float(i) >= self.lncRNA_min_exp for i in line.strip().split('\t')[1:]])
        }

        mRNA_exp_dict = {
            line.strip().split('\t')[0]: [float(i) for i in line.strip().split('\t')[1:]]
            for line in open(self.mRNA_exp)
            if not line.startswith('Geneid') and line.strip() and
               all([float(i) >= self.mRNA_min_exp for i in line.strip().split('\t')[1:]])
        }

        with tqdm(total=len(lncRNA_exp_dict) * len(mRNA_exp_dict), desc='Co-expression predicting') as pbar:
            params = ((k1, v1, k2, v2) for k1, v1 in lncRNA_exp_dict.items() for k2, v2 in mRNA_exp_dict.items())
            tkm = TaskManager(num_processing=self.num_processing, params=params)
            rets = tkm.parallel_run_func(func=self.sub_process, call_back_func=lambda _: pbar.update())

        data = [ret.get() for ret in rets]
        raw = DataFrame(data=data, columns=['lncRNA_id', 'mRNA_id', 'pcc', 'p_value'])
        raw.sort_values(by=['lncRNA_id', 'p_value'], inplace=True, ascending=[True, True])
        raw.to_csv(f'{self.output_path}/raw_co_exp.xls', sep='\t', index=False, float_format='%.12f', na_rep='NA')

        filter_df = raw[(raw['pcc'].abs() >= self.r) & (raw['p_value'] <= self.q_value)]
        filter_df['q_value'] = multipletests(pvals=filter_df['p_value'], alpha=self.FDR, method='fdr_bh')[1]
        filter_df = filter_df[filter_df['q_value'] <= self.q_value]
        filter_df.sort_values(by=['lncRNA_id', 'q_value'], inplace=True, ascending=[True, True])
        filter_df.to_csv(f'{self.output_path}/filter_co_exp.xls', sep='\t', index=False, float_format='%.12f', na_rep='NA')


class LncRNAClassification:
    def __init__(self, mRNA_gff_file: str, lncRNA_gtf_file: str, out_dir: str):
        self.mRNA_gff_file = abspath(mRNA_gff_file)
        self.mRNA_gtf_file = '.'.join(self.mRNA_gff_file.split('.')[:-1]) + '.gtf'
        self.lncRNA_gtf_file = abspath(lncRNA_gtf_file)
        out_dir = abspath(out_dir)
        makedirs(out_dir, exist_ok=True)
        self.gene_bed = f'{out_dir}/gene.bed'
        self.exon_bed = f'{out_dir}/exon.bed'
        self.intron_bed = f'{out_dir}/intron.bed'
        self.lncRNA_bed = f'{out_dir}/lncRNA.bed'
        self.sense = f'{out_dir}/sense.bed'
        self.antisense = f'{out_dir}/antisense.bed'
        self.intronic = f'{out_dir}/intronic.bed'
        self.intergenic = f'{out_dir}/intergenic.bed'

    def classification(self):
        bedtools = which('bedtools')
        gffread = which('gffread')
        gff2gtf = f'{gffread} {self.mRNA_gff_file} -T -o {self.mRNA_gtf_file}' if not exists(self.mRNA_gtf_file) else ''

        gene_bed = (r'''awk -F'\t' '{if($3 == "gene"){print $1,$4,$5,$9,$6,$7}}' OFS='\t' %s | sort -uV > %s''' %
                    (self.mRNA_gff_file, self.gene_bed))
        exon_bed = (r'''awk -F'\t' '{if($3 == "exon"){print $1,$4,$5,$9,$6,$7}}' OFS='\t' %s | sort -uV > %s''' %
                    (self.mRNA_gtf_file, self.exon_bed))
        intron_bed = f'{bedtools} subtract -a {self.gene_bed} -b {self.exon_bed} -s | sort -uV > {self.intron_bed}'
        lncRNA_bed = (r'''awk -F'\t' '{print $1,$4,$5,$9,$6,$7}' OFS='\t' %s | sort -uV > %s''' %
                      (self.lncRNA_gtf_file, self.lncRNA_bed))

        intronic = f'{bedtools} intersect -a {self.lncRNA_bed} -b {self.intron_bed} -s > {self.intronic}'

        sense = (
                r'''%s intersect -a <(awk '{if(match($0, /transcript_id "[a-zA-Z0-9]*.*[a-zA-Z0-9]*"/)) print substr($0, RSTART, RLENGTH)}' %s | sort -uV | grep -Fwvf - %s) -b %s -s > %s''' %
                (bedtools, self.intronic, self.lncRNA_bed, self.gene_bed, self.sense)
        )

        antisense = (
                r'''%s intersect -a <(cat %s %s | awk '{if(match($0, /transcript_id "[a-zA-Z0-9]*.*[a-zA-Z0-9]*"/)) print substr($0, RSTART, RLENGTH)}' | sort -uV | grep -Fwvf - %s) -b %s -S > %s''' %
                (bedtools, self.intronic, self.sense, self.lncRNA_bed, self.gene_bed, self.antisense)
        )

        intergenic = (
                r'''%s subtract -a <(cat %s %s %s | awk '{if(match($0, /transcript_id "[a-zA-Z0-9]*.*[a-zA-Z0-9]*"/)) print substr($0, RSTART, RLENGTH)}' | sort -uV | grep -Fwvf - %s) -b %s > %s''' %
                (bedtools, self.intronic, self.sense, self.antisense, self.lncRNA_bed, self.gene_bed, self.intergenic)
        )

        return '\n'.join([gff2gtf, gene_bed, exon_bed, intron_bed, lncRNA_bed, sense, antisense, intronic, intergenic])
