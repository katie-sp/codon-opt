import pickle
species_list = ['Homo sapiens', 'Cricetulus griseus', 'Mus musculus']

codon_table = {
        'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
        'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',                
        'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
        'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
        'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
        'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
        'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
        'UUC':'F', 'UUU':'F', 'UUA':'L', 'UUG':'L',
        'UAC':'Y', 'UAU':'Y', 'UAA':'_', 'UAG':'_',
        'UGC':'C', 'UGU':'C', 'UGA':'_', 'UGG':'W',
    }

#codon_table_T = {key.replace('U','T') :codon_table_U[key] for key in codon_table_U.keys()}

codon_usage = pickle.load(open('./codon_freqs.pkl', 'rb'))

def check_seq(seq):
    ''' Checks if a seq (string) is a DNA sequence '''
    seq_set = set(seq)
    dna_set = set(['A', 'G', 'C', 'U', 'T'])
    try:
        assert len(seq) > 0
    except:
        return('Please enter a sequence.')
    try:
        assert seq_set.issubset(dna_set)
    except:
        return('Please ensure your sequence only contains DNA one-letter bases (A, G, C, T, U) and no spaces or other characters.')
    try:
        assert ('T' not in seq_set or 'U' not in seq_set)
    except:
        return('Please ensure your sequence does not contain both T and U bases.')
    try:
        assert len(seq) % 3 == 0 
    except:
        return('Your sequence length is not divisible by 3, so it cannot be read as codons.')
# take input
def opt(species, seq):
    seq = seq.upper()
    T = 'T' in seq # check if using T's or U's
    if check_seq(seq) is not None:
        return(check_seq(seq))
    seq = seq.replace('T', 'U')  # since the codon chart and frequencies only use U from what i could easily get online

    # convert input into codons
    codons = []
    for i in range(0, len(seq), 3):
        codons.append(seq[i:i+3])

    # identify rare codons
    rare_codons = []
    for i in range(len(codons)):
        if codon_usage[species][codons[i]] <= 10:
            aa = codon_table[codons[i]]
            possible_codons = [i for i in codon_table.keys() if codon_table[i] == aa]
            codon_usage_subtable = {k:codon_usage[species][k] for k in codon_usage[species].keys() if k in possible_codons}
            best_codon = max(codon_usage_subtable, key=codon_usage_subtable.get)
            if best_codon != codons[i]:
                rare_codons.append((i, codons[i], codon_usage[species][codons[i]]))
            
    rare_codons_optimized = []
            
    # print out list of rare codons 
    output = {'changes':''}
    if len(rare_codons) == 0:
        output['changes'] = 'No rare codons detected.'
    else:
        output['changes'] = 'The following changes were made:<br>'
        for rare in rare_codons:
            aa = codon_table[rare[1]]
            possible_codons = [i for i in codon_table.keys() if codon_table[i] == aa]
            codon_usage_subtable = {k:codon_usage[species][k] for k in codon_usage[species].keys() if k in possible_codons}
            best_codon = max(codon_usage_subtable, key=codon_usage_subtable.get)
            best_freq = codon_usage[species][best_codon]
            output['changes'] += f"Codon number {rare[0] + 1} ({rare[1].replace('U', 'T') if T else rare[1]}) has a frequency of {rare[2]} per thousand codons. We recommend changing to {best_codon.replace('U', 'T') if T else best_codon}, which has a frequency of {best_freq} per thousand codons.<br>"
            rare_codons_optimized.append(best_codon)
    final_changes = ''
    for i in range(len(codons)):
        if codons[i] in list(i[1] for i in rare_codons):
            final_changes += rare_codons_optimized.pop(0).replace('U', 'T') if T else rare_codons_optimized.pop(0)
        else:
            final_changes += codons[i].replace('U', 'T') if T else codons[i]
            
    # print out optimized version of initial sequence
    output['final'] = f'Click here to copy the final optimized sequence to your clipboard:<br>{final_changes}'
    output['final_seq'] = final_changes
    return output

if __name__ == "__main__": 
    seq = 'AGTACT'
    species = 'Homo sapiens'
    print(opt(species, seq))
    

