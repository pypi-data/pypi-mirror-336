import dnaweaver as dw
import time
import dnachisel as dnachisel 
from sciutil import SciUtil
from Bio.Seq import Seq
from difflib import SequenceMatcher
import primer3
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
import pandas as pd
import math
from dnachisel import *

u = SciUtil()

from primer3 import calc_hairpin, calc_homodimer


from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqFeature import SeqFeature, FeatureLocation

def insert_sequence_with_translation(input_file, output_file, insert_position, new_sequence, translation_label, reverse=False):
    """
    Insert a new sequence at a specific position in a GenBank file, add a translation annotation,
    and adjust existing annotations to avoid overlap.

    Args:
        input_file (str): Path to the original GenBank file.
        output_file (str): Path to save the modified GenBank file.
        insert_position (int): Position to insert the new sequence (0-based).
        new_sequence (str): The DNA sequence to insert.
        translation_label (str): Label for the translation feature.
        reverse (bool): Whether the feature should be on the reverse strand.
    """
    # Read the original GenBank file
    record = SeqIO.read(input_file, "genbank")
    
    # Insert the new sequence at the specified position
    if reverse:
        new_sequence = str(Seq(new_sequence).reverse_complement())  # Reverse complement the sequence if needed
    record.seq = record.seq[:insert_position] + Seq(new_sequence) + record.seq[insert_position:]
    
    # Adjust existing annotations to avoid overlap
    inserted_length = len(new_sequence)
    for feature in record.features:
        if feature.location.start >= insert_position:
            feature.location = FeatureLocation(
                feature.location.start + inserted_length,
                feature.location.end + inserted_length,
                strand=feature.location.strand
            )
    
    # Create the feature label
    strand_label = " (reverse)" if reverse else " (forward)"
    full_label = translation_label + strand_label
    
    # Add a feature for the inserted sequence
    start = insert_position
    end = insert_position + len(new_sequence)
    feature = SeqFeature(
        location=FeatureLocation(start, end, strand=-1 if reverse else 1),
        type="CDS",  # CDS type for coding sequences
        qualifiers={
            "label": full_label,
            "translation": Seq(new_sequence).translate(table=11)  # Translation for the sequence
        }
    )
    record.features.append(feature)
    # Save the modified GenBank file
    if output_file:
        SeqIO.write(record, output_file, "genbank")
        print(f"Updated GenBank file saved as {output_file}")
    
    return record

def insert_features_from_oligos(record, seq_id, seq, strand, tm, output_file):
    """
    Insert features into a GenBank file based on oligo_df.

    Args:
        genbank_file (str): Path to the original GenBank file.
        output_file (str): Path to save the updated GenBank file.
        oligo_df (pd.DataFrame): DataFrame with oligo information. 
                                 Expected columns: ['id', 'oligo_id', 'oligo_sequence', 'oligo_length', ...].
    """
    # Iterate through the oligo DataFrame to add features
    start = record.seq.find(seq.upper())
    if start == -1:
        print(f"Warning: Oligo sequence {seq_id} not found in the GenBank sequence.")
    
    end = start + len(seq)
    feature = SeqFeature(
        location=FeatureLocation(start, end, strand=strand),
        type="misc_feature",
        qualifiers={
            "label": f"{seq_id} {'(reverse)' if strand == -1 else '(forward)'}",
            "note": f"Length: {len(seq)}, TM: {tm}"
        }
    )
    record.features.append(feature)
    
    # Save the updated GenBank file
    if output_file:
        SeqIO.write(record, output_file, "genbank")
        print(f"Updated GenBank file saved as {output_file}")
    return record
    
def check_secondary_structure(sequence, temp=55):
    """
    Check secondary structures like hairpins and homodimers in a given primer sequence.
    
    Args:
        sequence (str): The DNA sequence of the primer to analyze.
        
    Returns:
        dict: Results for hairpin and homodimer properties.
    """
    try:
        # Check for hairpin structure
        hairpin_result = calc_hairpin(sequence, temp_c=temp)
        hairpin_info = {
            "hairpin_found": hairpin_result.structure_found,
            "hairpin_tm": hairpin_result.tm,
            "hairpin_dg": hairpin_result.dg/1000,
            "hairpin_dh": hairpin_result.dh/1000,
            "hairpin_ds": hairpin_result.ds,
        }

        # Check for homodimer structure
        homodimer_result = calc_homodimer(sequence, temp_c=temp)
        homodimer_info = {
            "homodimer_found": homodimer_result.structure_found,
            "homodimer_tm": homodimer_result.tm,
            "homodimer_dg": homodimer_result.dg/1000,
            "homodimer_dh": homodimer_result.dh/1000,
            "homodimer_ds": homodimer_result.ds,
        }
    except Exception as e:
        u.warn_p([f"Warning: issue with secondary structure check. ", sequence, e])
        hairpin_info = {"hairpin_found": False, "hairpin_tm": None, "hairpin_dg": None, "hairpin_dh": None, "hairpin_ds": None}
        homodimer_info = {"homodimer_found": False, "homodimer_tm": None, "homodimer_dg": None, "homodimer_dh": None, "homodimer_ds": None}
    # Combine results
    return {"hairpin": hairpin_info, "homodimer": homodimer_info}

def build_oligos(seq_id: str, sequence: str, output_directory: str, min_gc=0.3, max_gc=0.7, min_tm=55, max_tm=70, min_segment_length=40, max_segment_length=100, max_length=1500):
    """ Use DNAweaver to build oligos """
    # Here we use a comercial supplier but don't actually care. 
    cheap_dna_offer = dw.CommercialDnaOffer(
        name="CheapDNA.",
        sequence_constraints=[
            dw.NoPatternConstraint(enzyme="BsaI"),
            dw.SequenceLengthConstraint(max_length=4000),
            dw.GcContentConstraint(min_gc=min_gc, max_gc=max_gc)
        ],
        pricing=dw.PerBasepairPricing(0.10),
    )

    oligo_dna_offer = dw.CommercialDnaOffer(
        name="OliGoo",
        sequence_constraints=[
            dw.GcContentConstraint(min_gc=min_gc, max_gc=max_gc),
            dw.SequenceLengthConstraint(max_length=4000),
        ],
        pricing=dw.PerBasepairPricing(0.07),
        memoize=True
    )

    oligo_assembly_station = dw.DnaAssemblyStation(
        name="Oligo Assembly Station",
        assembly_method=dw.OligoAssemblyMethod(
            overhang_selector=dw.TmSegmentSelector(
                min_size=15, max_size=25, min_tm=min_tm, max_tm=max_tm
            ),
            min_segment_length=min_segment_length,
            max_segment_length=max_segment_length,
            sequence_constraints=[dw.SequenceLengthConstraint(max_length=4000)],
            duration=8,
            cost=30,
        ),
        supplier=oligo_dna_offer,
        coarse_grain=20,
        a_star_factor="auto",
        memoize=True,
    )

    assembly_station = dw.DnaAssemblyStation(
        name="Gibson Assembly Station",
        assembly_method=dw.GibsonAssemblyMethod(
            overhang_selector=dw.TmSegmentSelector(min_tm=min_tm, max_tm=max_tm),
            min_segment_length=min_segment_length,
            max_segment_length=max_segment_length + 20, # add a bit of a buffer
        ),
        supplier=[cheap_dna_offer, oligo_assembly_station],
        logger="bar",
        coarse_grain=100,
        fine_grain=10,
        a_star_factor="auto",
    )
    
    print("Looking for the best assembly plan...")
    t0 = time.time()
    quote = assembly_station.get_quote(sequence, with_assembly_plan=True)
    assembly_plan_report = quote.to_assembly_plan_report()
    assembly_plan_report.write_full_report(f"{output_directory}/oligo_assembly_plan_{seq_id}.zip")
    original_sequence = assembly_plan_report.plan.sequence
    # Then get the sequence 
    rows = []
    for oligo in assembly_plan_report.plan.assembly_plan:
        # If this was chosen then choose it
        if oligo.accepted:
            rows.append([oligo.id, oligo.sequence, original_sequence])
    return rows

def get_oligos(df, protein_column, id_column, output_directory, forward_primer: str, reverse_primer: str, sequence_end: str, min_overlap=10, min_gc=0.3, 
               max_gc=0.7, min_tm=55, max_tm=70, min_segment_length=90, max_segment_length=130, max_length=1500, genbank_file=None,
               insert_position=0, simple=False, codon_optimize=True):
    """ Get the oligos for a dataframe:
    sequence_end is the end of the sequence i.e. TAA, TGA, etc or a histag 
    """
    rows = []   
    for seq_id, protein_sequence in df[[id_column, protein_column]].values:
        # Add on the primers that the user has provided
        if codon_optimize:
            optimzed_sequence = codon_optimize(protein_sequence, min_gc, max_gc) + sequence_end
        else:
            optimzed_sequence = protein_sequence + sequence_end
            u.dp([f"Added sequence end with HIS and stop to: {seq_id}, {sequence_end}"])

        if genbank_file:
            # Add in the optimzed sequence
            translation_label = f"Insert_{seq_id}"
            reverse = False  # Set to True for reverse feature, False for forward
            record = insert_sequence_with_translation(genbank_file, None, insert_position, optimzed_sequence, translation_label, reverse)
            
        if optimzed_sequence[:3] != "ATG":
            u.dp([f"Warning: {seq_id} does not start with a methionine. ", optimzed_sequence[:3]])
            if 'ATG' not in forward_primer:
                u.warn_p([f"Warning: {seq_id} does not start with a methionine. AND you don't have a methonine in your primer!!", forward_primer])
                print("We expect the primer to be in 5 to 3 prime direction.")
        # ALso check the end and or the reverse primer check for the three ones
        if optimzed_sequence[-3:] != "TAA" and optimzed_sequence[-3:] != "TGA" and optimzed_sequence[-3:] != "TAG":
            u.dp([f"Warning: {seq_id} does not end with a stop codon. ", optimzed_sequence[-3:]])
            if 'TAA' not in reverse_primer and "TGA" not in reverse_primer and "TAG" not in reverse_primer:
                u.warn_p([f"Warning: {seq_id} does not end with a stop codon. AND you don't have a stop codon in your primer!!", reverse_primer])
                print("We expect the primer to be in 5 to 3 prime direction.")
        codon_optimized_sequence = forward_primer + optimzed_sequence + reverse_primer
        #try:
        # Check now some simple things like that there is 
        if simple:
            oligos = build_simple_oligos(seq_id, codon_optimized_sequence, min_segment_length, max_segment_length)
        else:
            oligos = build_oligos(seq_id, codon_optimized_sequence, output_directory, min_gc, max_gc, min_tm, max_tm, min_segment_length, max_segment_length, max_length)
        # except Exception as e:
        #     u.warn_p([f"Warning: {seq_id} did not have any oligos built. ", e])
        #     oligos = []
        prev_oligo = None
        # If a genbank file was provided also just add in the new sequnece
        if len(oligos) > 0:
            for i, oligo in enumerate(oligos):
                seq = oligo[1]
                # CHeck that there is an overlap with the previous sequence and that it is not too short
                # Also make sure we swap the directions of the oligos so they automatically anneal
                # Also assert that the start is a methionine (and if not warn it... )
                primer_overlap = None
                primer_tm = None
                primer_len = None
                homodimer_tm = None
                hairpin_tm = None
                if prev_oligo:
                    # Get the overlap with the previous sequence
                    match = SequenceMatcher(None, prev_oligo, seq).find_longest_match()
                    primer_overlap = prev_oligo[match.a:match.a + match.size]
                    # Analyze the primer sequence
                    results = check_secondary_structure(primer_overlap)
                    homodimer_tm = results['homodimer']['homodimer_dg']
                    hairpin_tm = results['hairpin']['hairpin_dg']
                    primer_tm = primer3.bindings.calcTm(primer_overlap)
                    primer_len = len(primer_overlap)

                prev_oligo = seq
                orig_seq = seq
                strand = 1
                if i % 2 == 0:
                    seq = str(Seq(seq).reverse_complement())
                    strand = -1
                oligo_tm = primer3.bindings.calcTm(seq)
                if genbank_file:
                    insert_features_from_oligos(record, f"{seq_id}_oligo_{i}", orig_seq, strand, oligo_tm, None)
                rows.append([seq_id, oligo[0], seq, len(seq), oligo_tm, primer_overlap, primer_tm, primer_len, homodimer_tm, hairpin_tm, oligo[2]])
            if genbank_file:
                output_file = genbank_file.replace('.', f'_{seq_id}.')
                record.name = seq_id
                SeqIO.write(record, f'{output_directory}/{output_file}', "genbank")
        else:
            u.warn_p([f"Warning: {seq_id} did not have any oligos built. ", optimzed_sequence])
            rows.append([seq_id, None, optimzed_sequence, len(optimzed_sequence), None, None, None, None, None, None, None])
        
    oligo_df = pd.DataFrame(rows, columns=["id", "oligo_id", "oligo_sequence", "oligo_length", "oligo_tm", "primer_overlap_with_previous", "overlap_tm_5prime", "overlap_length", 
                                            "overlap_homodimer_dg", "overlap_hairpin_dg", "original_sequence"])
    
        
    return oligo_df




def build_simple_oligos(seq_id: str, sequence: str, min_segment_length=90, max_segment_length=130, overlap_len=18):
    # Basically get the splits size
    seq_len = len(sequence)
    num_splits = int(math.ceil(seq_len / min_segment_length))
    # Make sure it is even
    if num_splits % 2 != 0:
        num_splits += 1
    remainder = seq_len % num_splits
    # Check if there is a remainder, if so we need to add one to the splits and then share the new remainder 
    print(num_splits, remainder)        
    prev_overlap = ''
    # Now we want to go through the new part length and while remainder is greater then 0 we distribute this across the splits
    max_part_len = math.floor(seq_len/num_splits)
    split_counts = {}
    for i in range(0, num_splits + 1):
        split_counts[i] = max_part_len
    # Now distribute the remainder
    split_count = 0
    print(max_part_len, num_splits, seq_len, max_part_len * num_splits)
    for i in range(0, remainder + 1):
        split_counts[split_count] += 1
        split_count += 1
        # Iterate through this again
        if split_count == num_splits + 1:
            split_count = 0
    prev_cut = 0
    rows = []
    finished = False
    for i in split_counts:
        part_len = split_counts[i]
        cut = prev_cut + part_len
        oligo = sequence[prev_cut:cut]
        # Calculate the tm and we'll check that we get the "best" one i.e. closest to 62 deg
        # Get the overlap with the previous sequence
        best_oligo = oligo
        best_tm_diff = 10000
        best_cut = cut
        part_len_diff = 0
        best_pl = 0
        optimal_temp = 62
        for pl in range(10, 0, -1):
            for j in range(0, max_segment_length - min_segment_length):
                cut = prev_cut + part_len + pl + j
                oligo = sequence[prev_cut:cut]
                primer_overlap = oligo[-1 * (overlap_len + pl):]
                # Analyze the primer sequence
                primer_tm = (primer3.bindings.calcTm(primer_overlap) + primer3.bindings.calcTm(str(Seq(primer_overlap).reverse_complement())))/2
                results = check_secondary_structure(primer_overlap)
                # Want to have the opp a high homodimer TM
                homodimer_tm = -1 * results['homodimer']['homodimer_dg']
                # Get the reverse comp overlap as well
                if (abs(primer_tm - optimal_temp) + homodimer_tm) < best_tm_diff:
                    best_tm_diff = abs(primer_tm - optimal_temp) + homodimer_tm
                    best_oligo = oligo
                    best_cut = cut
                    part_len_diff = j + pl
                    best_pl = pl
        # check the left over size
        if len(sequence[best_cut:]) < overlap_len:
            # Add on the last bit and just have a longer final oligo
            rows.append([f'{seq_id}_{i}', best_oligo + sequence[best_cut:], sequence, prev_cut, best_cut + len(sequence[best_cut:]), part_len + part_len_diff])
            print('CHECK!')
            finished = True
            break
        rows.append([f'{seq_id}_{i}', best_oligo, sequence, prev_cut, best_cut, part_len + part_len_diff])
        prev_cut = best_cut - overlap_len - best_pl
    # Add in the last one
    oligo = sequence[prev_cut:]
    if not finished:
        part_len = len(oligo)
        cut = len(sequence)
        if len(oligo) < 18:
            u.warn_p(["Last oligo very short,.... check this!", f'{seq_id}_{i}', oligo, sequence, prev_cut, cut, part_len])
        print(prev_cut, part_len, len(sequence), oligo)
        rows.append([f'{seq_id}_{i}', oligo, sequence, prev_cut, cut, part_len])
    return rows


def codon_optimize(protein_sequence: str, min_gc=0.3, max_gc=0.7):
    """ Codon optimize the protein sequence using DNA chisel: https://github.com/Edinburgh-Genome-Foundry/DnaChisel"""
    seq = dnachisel.reverse_translate(protein_sequence)
    problem = dnachisel.DnaOptimizationProblem(
        sequence=seq,
        constraints=[
            AvoidPattern("BsaI_site"),
            EnforceGCContent(mini=min_gc, maxi=max_gc, window=50),
            EnforceTranslation(location=(0, len(seq))), 
            AvoidStopCodons(
                location=(0, len(seq)-3)) # Let there be stop codons in the last bit
        ],
        objectives=[CodonOptimize(species='e_coli', location=(0, len(seq)))]
    )
    # SOLVE THE CONSTRAINTS, OPTIMIZE WITH RESPECT TO THE OBJECTIVE
    problem.resolve_constraints()
    problem.optimize()

    # PRINT SUMMARIES TO CHECK THAT CONSTRAINTS PASS
    print(problem.constraints_text_summary())
    print(problem.objectives_text_summary())

    # GET THE FINAL SEQUENCE (AS STRING OR ANNOTATED BIOPYTHON RECORDS)
    final_sequence = problem.sequence  # string
    final_record = problem.to_record(with_sequence_edits=True)
    print(protein_sequence)
    print(final_sequence)
    return final_sequence

