import pandas as pd
import numpy as np
from collections import Counter
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
def calculate_base_composition(sequence):
    counts = Counter(sequence)
    total = len(sequence)
    return counts['T'] / total * 100, counts['C'] / total * 100, counts['A'] / total * 100, counts['G'] / total * 100, \
           (counts['A'] + counts['T']) / total * 100, (counts['G'] + counts['C']) / total * 100, total

def calculate_position_base_composition(sequence):
    pos_counts = {1: Counter(), 2: Counter(), 3: Counter()}
    for i, base in enumerate(sequence):
        pos = (i % 3) + 1
        pos_counts[pos][base] += 1

    total_pos = {pos: sum(pos_counts[pos].values()) for pos in pos_counts}
    return (
        pos_counts[1]['T'] / total_pos[1] * 100, pos_counts[1]['C'] / total_pos[1] * 100, pos_counts[1]['A'] / total_pos[1] * 100, pos_counts[1]['G'] / total_pos[1] * 100, total_pos[1],
        pos_counts[2]['T'] / total_pos[2] * 100, pos_counts[2]['C'] / total_pos[2] * 100, pos_counts[2]['A'] / total_pos[2] * 100, pos_counts[2]['G'] / total_pos[2] * 100, total_pos[2],
        pos_counts[3]['T'] / total_pos[3] * 100, pos_counts[3]['C'] / total_pos[3] * 100, pos_counts[3]['A'] / total_pos[3] * 100, pos_counts[3]['G'] / total_pos[3] * 100, total_pos[3]
    )
def features(input_fasta_path, output_excel_path):
    data = []
    for record in SeqIO.parse(input_fasta_path, "fasta"):
        seq_str = str(record.seq)
        t, c, a, g, at_content, gc_content, total = calculate_base_composition(seq_str)
        t1, c1, a1, g1, total1, t2, c2, a2, g2, total2, t3, c3, a3, g3, total3 = calculate_position_base_composition(seq_str)
        features = {
            'Sequence ID': record.id,
            'Length': total,
            'T%': t, 'C%': c, 'A%': a, 'G%': g, 'AT%': at_content, 'GC%': gc_content,
            'T-1': t1, 'C-1': c1, 'A-1': a1, 'G-1': g1, 'Pos #1': total1,
            'T-2': t2, 'C-2': c2, 'A-2': a2, 'G-2': g2, 'Pos #2': total2,
            'T-3': t3, 'C-3': c3, 'A-3': a3, 'G-3': g3, 'Pos #3': total3,
        }
        data.append(features)

    df = pd.DataFrame(data)
    df.to_excel(output_excel_path, index=False)



def calculate_rscu(seq):
    codon_table = {
        'F': ['TTT', 'TTC'], 'L': ['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'], 'I': ['ATT', 'ATC', 'ATA'],
        'M': ['ATG'], 'V': ['GTT', 'GTC', 'GTA', 'GTG'], 'S': ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'],
        'P': ['CCT', 'CCC', 'CCA', 'CCG'], 'T': ['ACT', 'ACC', 'ACA', 'ACG'], 'A': ['GCT', 'GCC', 'GCA', 'GCG'],
        'Y': ['TAT', 'TAC'], 'H': ['CAT', 'CAC'], 'Q': ['CAA', 'CAG'], 'N': ['AAT', 'AAC'], 'K': ['AAA', 'AAG'],
        'D': ['GAT', 'GAC'], 'E': ['GAA', 'GAG'], 'C': ['TGT', 'TGC'], 'W': ['TGG'],
        'R': ['CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'], 'G': ['GGT', 'GGC', 'GGA', 'GGG']
    }

    codon_counts = Counter(seq[i:i + 3] for i in range(0, len(seq) - 2, 3))

    rscu_values = {}
    codon_counts_dict = {}
    for aa, codons in codon_table.items():
        total = sum(codon_counts[codon] for codon in codons)
        n_codons = len(codons)
        for codon in codons:
            observed = codon_counts[codon]
            expected = total / n_codons if n_codons else 0
            rscu = observed / expected if expected else 0
            rscu_values[codon] = rscu
            codon_counts_dict[codon] = observed

    return rscu_values, codon_counts_dict


c2aa = {
    'TGT': 'Cys', 'TGC': 'Cys', 'GAT': 'Asp', 'GAC': 'Asp', 'TCT': 'Ser', 'TCG': 'Ser', 'TCA': 'Ser', 'TCC': 'Ser',
    'AGC': 'Ser', 'AGT': 'Ser',
    'CAA': 'Gln', 'CAG': 'Gln', 'ATG': 'Met', 'AAC': 'Asn', 'AAT': 'Asn', 'CCT': 'Pro', 'CCG': 'Pro', 'CCA': 'Pro',
    'CCC': 'Pro', 'AAG': 'Lys',
    'AAA': 'Lys', 'ACC': 'Thr', 'ACA': 'Thr', 'ACG': 'Thr', 'ACT': 'Thr', 'TTT': 'Phe', 'TTC': 'Phe', 'GCA': 'Ala',
    'GCC': 'Ala', 'GCG': 'Ala',
    'GCT': 'Ala', 'GGT': 'Gly', 'GGG': 'Gly', 'GGA': 'Gly', 'GGC': 'Gly', 'ATC': 'Ile', 'ATA': 'Ile', 'ATT': 'Ile',
    'TTA': 'Leu', 'TTG': 'Leu',
    'CTC': 'Leu', 'CTT': 'Leu', 'CTG': 'Leu', 'CTA': 'Leu', 'CAT': 'His', 'CAC': 'His', 'CGA': 'Arg', 'CGC': 'Arg',
    'CGG': 'Arg', 'CGT': 'Arg',
    'AGG': 'Arg', 'AGA': 'Arg', 'TGG': 'Trp', 'GTA': 'Val', 'GTC': 'Val', 'GTG': 'Val', 'GTT': 'Val', 'GAG': 'Glu',
    'GAA': 'Glu', 'TAT': 'Tyr', 'TAC': 'Tyr'
}


def calculate_third_position_frequencies(seq):
    third_position_counts = Counter()
    total_third_positions = 0

    codons = [seq[i:i + 3] for i in range(0, len(seq) - 2, 3)]
    third_nucleotides = [codon[2] for codon in codons if len(codon) == 3]
    third_position_counts.update(third_nucleotides)
    total_third_positions += len(third_nucleotides)

    T3s = third_position_counts['T'] / total_third_positions if total_third_positions else 0
    C3s = third_position_counts['C'] / total_third_positions if total_third_positions else 0
    A3s = third_position_counts['A'] / total_third_positions if total_third_positions else 0
    G3s = third_position_counts['G'] / total_third_positions if total_third_positions else 0
    GC3s = (third_position_counts['G'] + third_position_counts[
        'C']) / total_third_positions if total_third_positions else 0

    return T3s, C3s, A3s, G3s, GC3s


def calculate_codon_frequency(gene_seq):
    # 计算基因中每个密码子的出现次数
    codon_counts = Counter(gene_seq[i:i + 3] for i in range(0, len(gene_seq), 3))
    total_codons = sum(codon_counts.values())

    # 计算每个密码子的使用频率
    codon_freq = {codon: count / total_codons for codon, count in codon_counts.items()}
    return codon_freq


def calculate_cai(gene_codon_freq, ref_codon_freq):
    # 计算每个密码子的相对适应性值
    cai_values = {codon: gene_freq / ref_codon_freq.get(codon, 1) for codon, gene_freq in gene_codon_freq.items()}

    # 取几何平均值作为 CAI
    cai = np.prod(list(cai_values.values())) ** (1 / len(cai_values))
    return cai


def calculate_cbi(gene_codon_freq):
    # Calculate the standard deviation of codon usage frequency
    codon_freq_values = np.array(list(gene_codon_freq.values()))
    cbi = np.std(codon_freq_values)
    return cbi


def calculate_fop(gene_codon_freq, ref_codon_freq):
    # Calculate the total frequency of optimal codon usage in the gene
    fop = sum(gene_freq for codon, gene_freq in gene_codon_freq.items() if ref_codon_freq.get(codon, 0) == 1)
    return fop


def calculate_nc(gene_codon_freq):
    # Calculate the uniformity of codon usage, i.e., the number of codons
    nc = len(gene_codon_freq)
    return nc
def calculate_L_sym(seq):
    codon_table = {
        'F': ['TTT', 'TTC'], 'L': ['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'], 'I': ['ATT', 'ATC', 'ATA'],
        'M': ['ATG'], 'V': ['GTT', 'GTC', 'GTA', 'GTG'], 'S': ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'],
        'P': ['CCT', 'CCC', 'CCA', 'CCG'], 'T': ['ACT', 'ACC', 'ACA', 'ACG'], 'A': ['GCT', 'GCC', 'GCA', 'GCG'],
        'Y': ['TAT', 'TAC'], 'H': ['CAT', 'CAC'], 'Q': ['CAA', 'CAG'], 'N': ['AAT', 'AAC'], 'K': ['AAA', 'AAG'],
        'D': ['GAT', 'GAC'], 'E': ['GAA', 'GAG'], 'C': ['TGT', 'TGC'], 'W': ['TGG'],
        'R': ['CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'], 'G': ['GGT', 'GGC', 'GGA', 'GGG']
        }
    return sum(seq.count(codon) for codon_list in codon_table.values() for codon in codon_list)

def calculate_L_aa(seq):
    codon_table = {
        'F': ['TTT', 'TTC'], 'L': ['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'], 'I': ['ATT', 'ATC', 'ATA'],
        'M': ['ATG'], 'V': ['GTT', 'GTC', 'GTA', 'GTG'], 'S': ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'],
        'P': ['CCT', 'CCC', 'CCA', 'CCG'], 'T': ['ACT', 'ACC', 'ACA', 'ACG'], 'A': ['GCT', 'GCC', 'GCA', 'GCG'],
        'Y': ['TAT', 'TAC'], 'H': ['CAT', 'CAC'], 'Q': ['CAA', 'CAG'], 'N': ['AAT', 'AAC'], 'K': ['AAA', 'AAG'],
        'D': ['GAT', 'GAC'], 'E': ['GAA', 'GAG'], 'C': ['TGT', 'TGC'], 'W': ['TGG'],
        'R': ['CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'], 'G': ['GGT', 'GGC', 'GGA', 'GGG']
    }
    return len(set(aa for codon_list in codon_table.values() for codon in codon_list for aa, codons in codon_table.items() if codon in codons))

def calculate_gravy(seq):
    protein_analysis = ProteinAnalysis(seq)
    return protein_analysis.gravy()

def calculate_aromo(seq):
    protein_analysis = ProteinAnalysis(seq)
    return protein_analysis.aromaticity()
def rscu(input_fasta_path, output_excel_path):
    seq_records = list(SeqIO.parse(input_fasta_path, 'fasta'))

    rscu_data = []
    summary_data = []

    for rec in seq_records:
        seq = str(rec.seq)
        rscu_values, codon_counts = calculate_rscu(seq)
        T3s, C3s, A3s, G3s, GC3s = calculate_third_position_frequencies(seq)

        for codon, value in rscu_values.items():
            aa = c2aa.get(codon)
            if aa is not None:
                count = codon_counts.get(codon, 0)
                rscu_data.append({
                    'Sequence ID': rec.id,
                    'Codon': codon,
                    'Amino Acid': aa,
                    'RSCU': round(value, 3),
                    'Count': count
                })

        summary_data.append({
            'Sequence ID': rec.id,
            'T3s': T3s,
            'C3s': C3s,
            'A3s': A3s,
            'G3s': G3s,
            'GC3s': GC3s,
            'CAI': calculate_cai(calculate_codon_frequency(seq), reference_codon_freq),
            'CBI': calculate_cbi(calculate_codon_frequency(seq)),
            'Fop': calculate_fop(calculate_codon_frequency(seq), reference_codon_freq),
            'Nc': calculate_nc(calculate_codon_frequency(seq)),
            'L_sym': calculate_L_sym(seq),
            'L_aa': calculate_L_aa(seq),
            'Gravy': calculate_gravy(seq),
            'Aromo': calculate_aromo(seq)
        })

    df_rscu = pd.DataFrame(rscu_data)
    df_summary = pd.DataFrame(summary_data)

    with pd.ExcelWriter(output_excel_path) as writer:
        df_rscu.to_excel(writer, sheet_name='RSCU', index=False)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)


# Example usage
input_fasta_path = 'barcodes_input.fasta'  # Replace with your input FASTA file path
output_excel_path = 'output.xlsx'  # Replace with your output Excel file path

reference_codon_freq = {
    'TTT': 0.5, 'TTC': 0.5, 'TTA': 0.5, 'TTG': 0.5, 'CTT': 0.5, 'CTC': 0.5, 'CTA': 0.5, 'CTG': 0.5,
    'ATT': 0.5, 'ATC': 0.5, 'ATA': 0.5, 'ATG': 1.0, 'GTT': 0.5, 'GTC': 0.5, 'GTA': 0.5, 'GTG': 0.5,
    'TCT': 0.5, 'TCC': 0.5, 'TCA': 0.5, 'TCG': 0.5, 'AGT': 0.5, 'AGC': 0.5, 'CCT': 0.5, 'CCC': 0.5,
    'CCA': 0.5, 'CCG': 0.5, 'ACT': 0.5, 'ACC': 0.5, 'ACA': 0.5, 'ACG': 0.5, 'GCT': 0.5, 'GCC': 0.5,
    'GCA': 0.5, 'GCG': 0.5, 'TAT': 0.5, 'TAC': 0.5, 'TAA': 0.5, 'TAG': 0.5, 'CAT': 0.5, 'CAC': 0.5,
    'CAA': 0.5, 'CAG': 0.5, 'AAT': 0.5, 'AAC': 0.5, 'AAA': 0.5, 'AAG': 0.5, 'GAT': 0.5, 'GAC': 0.5,
    'GAA': 0.5, 'GAG': 0.5, 'TGT': 0.5, 'TGC': 0.5, 'TGA': 0.5, 'TGG': 1.0, 'CGT': 0.5, 'CGC': 0.5,
    'CGA': 0.5, 'CGG': 0.5, 'AGA': 0.5, 'AGG': 0.5, 'GGT': 0.5, 'GGC': 0.5, 'GGA': 0.5, 'GGG': 0.5
}

# # 基本特征
# extract_features(input_fasta_path, output_excel_path)
# #RSCI值计算
# extract_rscu(input_fasta_path, output_excel_path)
#
