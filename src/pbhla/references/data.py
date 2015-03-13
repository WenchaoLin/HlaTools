#! /usr/bin/env python

__author__ = 'Brett Bowman'
__email__ = 'bbowman@pacificbiosciences.com'

import os, re
import logging

from pbcore.io import FastaReader, FastaWriter

from pbhla import data
from pbhla.utils import valid_file

log = logging.getLogger()

GEN_PATTERN  = '_gen.fasta$'
CDNA_PATTERN = '_nuc.fasta$'
EXON_FASTA_PAT = '_exon\d+.fasta$'
EXON_FOFN_PAT = '_exons.fofn$'

DATA_PATH = data.get_data_path()
GEN_REF  = data.get_genomic_fasta()
CDNA_REF = data.get_cDNA_fasta()
EXON_REF = data.get_exon_fofn()

def get_genomic_reference():
    if valid_file( GEN_REF ):
        logging.info('Using existing Genomic Reference fasta')
        return GEN_REF
    else:
        logging.info('Creating new Genomic Reference fasta')
        create_genomic_reference()
        return get_genomic_reference()

def get_cDNA_reference():
    if valid_file( CDNA_REF ):
        logging.info('Using existing cDNA Reference fasta')
        return CDNA_REF
    else:
        logging.info('Creating new cDNA Reference fasta')
        create_cDNA_reference()
        return get_cDNA_reference()

def get_exon_reference():
    if valid_file( EXON_REF ):
        logging.info('Using existing Exon Reference fofn')
        return EXON_REF
    else:
        logging.info('Creating new Exon Reference fofn')
        create_exon_fofns()
        create_exon_reference()
        return get_exon_reference()

def list_data_files( end_pattern, root=DATA_PATH ):
    for root, dirs, files in os.walk( root ):
        for filename in sorted(files):
            if re.search( end_pattern, filename ):
                yield os.path.join(root, filename)

def append_records( handle, filepath ):
    for record in FastaReader( filepath ):
        handle.writeRecord( record )

def create_genomic_reference():
    with FastaWriter( GEN_REF ) as handle:
        for filepath in list_data_files( GEN_PATTERN ):
            append_records( handle, filepath )
    return GEN_REF

def create_cDNA_reference():
    with FastaWriter( CDNA_REF ) as handle:
        for filepath in list_data_files( CDNA_PATTERN ):
            append_records( handle, filepath )
    return CDNA_REF

def create_exon_fofns():
    for root, dirs, files in os.walk( DATA_PATH ):
        if 'exons' in dirs:
            exon_path = os.path.join( root, 'exons' )
            locus = os.path.split( root )[1]
            fofn = '%s_exons.fofn' % (locus)
            fofn_path = os.path.join( root, fofn )
            create_exon_fofn( exon_path, fofn_path )

def create_exon_fofn( exon_path, fofn_path ):
    with open( fofn_path, 'w' ) as handle:
        for filepath in list_data_files( EXON_FASTA_PAT, exon_path ):
            handle.write( filepath + '\n' )

def create_exon_reference():
    with open( EXON_REF, 'w' ) as handle:
        for filepath in list_data_files( EXON_FOFN_PAT ):
            root_folder = os.path.split( filepath )[0]
            locus = os.path.split( root_folder )[1]
            handle.write( '%s\t%s\n' % (locus, filepath) )

if __name__ == '__main__':
    print "START"
    print GEN_REF
    print DATA_PATH
    print get_genomic_reference()
    print get_cDNA_reference()
    print get_exon_reference()
