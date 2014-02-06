#! /usr/bin/env python

import logging, logging.config

from pbhla import __LOG__
from pbhla.references.data import get_exon_reference, get_genomic_reference, get_cDNA_reference
from pbhla.external.utils import (align_best_reference, 
                                  full_align_best_reference)
from pbhla.external.align_by_identity import align_by_identity
from pbhla.sequences.orientation import orient_sequences
from pbhla.sequences.input import get_input_file
from pbhla.alleles.extract import extract_alleles
from pbhla.cdna.extract_cDNA import extract_cDNA
from pbhla.typing.summarize import summarize_typing

GROUPINGS = ['locus', 'allele', 'both', 'all']
GROUPING = 'both'

logging.config.fileConfig( __LOG__ )
log = logging.getLogger()

def type_sequences( input, grouping=GROUPING,
                           exon_fofn=None,
                           genomic_reference=None,
                           cDNA_reference=None):
    """
    Pick the top Amplicon Analysis consensus seqs from a Fasta by Nreads
    """

    # First, get any references not specified by the user
    exon_fofn = exon_fofn or get_exon_reference()
    genomic_reference = genomic_reference or get_genomic_reference()
    cDNA_reference = cDNA_reference or get_cDNA_reference()

    # Second, get the input file if a directory was specified
    sequence_file = get_input_file( input )

    # Finally, run the Typing procedure
    raw_alignment = align_best_reference( sequence_file, genomic_reference )
    reoriented = orient_sequences( sequence_file, alignment_file=raw_alignment )
    selected = extract_alleles( reoriented, alignment_file=raw_alignment, method=grouping )
    gDNA_alignment = full_align_best_reference( selected, genomic_reference )
    cDNA_file = extract_cDNA( selected, exon_fofn, alignment_file=gDNA_alignment )
    cDNA_alignment = align_by_identity( cDNA_file, cDNA_reference )
    summarize_typing( gDNA_alignment, cDNA_alignment )

if __name__ == '__main__':
    import sys
    logging.basicConfig( level=logging.INFO )

    input = sys.argv[1]
    grouping = sys.argv[2] if len(sys.argv) > 2 else GROUPING
    exon_fofn = sys.argv[3] if len(sys.argv) > 3 else None
    genomic_reference = sys.argv[4] if len(sys.argv) > 4 else None
    cDNA_reference = sys.argv[5] if len(sys.argv) > 5 else None

    type_sequences( input, grouping, exon_fofn, genomic_reference, cDNA_reference )