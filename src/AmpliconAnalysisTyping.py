#! /usr/bin/env python

from pbhla.typing.sequences import type_sequences

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    add = parser.add_argument
    add('amplicon_analysis', metavar='INPUT',
        help="Fasta/Fastq/Folder of Amplicon Analysis output")
    add('-g', '--grouping', metavar='METHOD', default='both',
        help="Method of selecting output sequences {locus, barcode, both, all} default=both")
    add('-e', '--exon_reference', metavar='REFERENCE', default=None,
        help='Dictionary file of Locus-specific exon references')
    add('-n', '--nucleotide_reference', metavar='FASTA', default=None,
        help='File of FASTA sequences from nucleotide references')
    add('-c', '--cDNA_reference', metavar='FASTA', default=None,
        help='File of FASTA sequences from cDNA references')
    add('-t', '--trim', metavar='INT', default=0, type=int,
        help='Number of bases to trim from the ends of sequences before typing')
    add('--debug', action='store_true',
        help="Flag to enable Debug mode")
    args = parser.parse_args()

    type_sequences( args.amplicon_analysis, grouping=args.grouping,
                                            exon_fofn=args.exon_reference,
                                            genomic_reference=args.nucleotide_reference,
                                            cDNA_reference=args.cDNA_reference,
                                            trim=args.trim )
