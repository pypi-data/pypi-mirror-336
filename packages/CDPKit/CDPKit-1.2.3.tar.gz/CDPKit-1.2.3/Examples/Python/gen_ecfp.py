#!/bin/env python

##
# gen_ecfp.py 
#
# This file is part of the Chemical Data Processing Toolkit
#
# Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with
# or without fee is hereby granted.
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN
# NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
##


import sys
import argparse

import CDPL.Chem as Chem
import CDPL.Descr as Descr
import CDPL.Util as Util


# generates the binary ECFP of the given molecule
def genECFP(mol: Chem.Molecule, num_bits: int, radius: int, inc_hs: bool, inc_config: bool) -> Util.BitSet:
    Chem.calcBasicProperties(mol, False)            # calculate basic molecular properties (if not yet done)
   
    ecfp_gen = Descr.CircularFingerprintGenerator() # create ECFP generator instance

    if inc_config:
        ecfp_gen.includeChirality(True)                  # allow atom chirality to have an impact on the ECFP generation
        Chem.calcCIPPriorities(mol, False)               # calculate atom symmetry classes for chiral atom perception and set corresponding property for all atoms
        Chem.perceiveAtomStereoCenters(mol, False, True) # perceive chiral atoms and set corresponding property for all atoms
        Chem.calcAtomStereoDescriptors(mol, False)       # calculate atom stereo descriptors and set corresponding property for all atoms

    if inc_hs:        
        ecfp_gen.includeHydrogens(True)                # include explicit hydrogens in the ECFP generation
        Chem.makeHydrogenComplete(mol)                 # make any implicit hydrogens explicit
         
    fp = Util.BitSet()                                 # create fingerprint bitset
    fp.resize(num_bits)                                # set desired fingerprint size

    ecfp_gen.setNumIterations(radius)                  # set num. iterations (=atom. env. radius)
    ecfp_gen.generate(mol)                             # extract chracteristic structural features
    ecfp_gen.setFeatureBits(fp)                        # set bits associated with the extracted structural features

    # if needed, fp could be converted into a numpy single precision float array as follows:
    # fp = numpy.array(fp, dtype=numpy.float32)
    
    return fp
    
def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generates extended connectivity fingerprints (ECFPs) for given input molecules.')

    parser.add_argument('-i',
                        dest='in_file',
                        required=True,
                        metavar='<file>',
                        help='Input molecule file')
    parser.add_argument('-o',
                        dest='out_file',
                        required=True,
                        metavar='<file>',
                        help='Fingerprint output file')
    parser.add_argument('-n',
                        dest='num_bits',
                        required=False,
                        metavar='<integer>',
                        default=1024,
                        help='Fingerprint size in bits (default: 1024)',
                        type=int)
    parser.add_argument('-r',
                        dest='radius',
                        required=False,
                        metavar='<integer>',
                        default=2,
                        help='Max. atom environment radius in number of bonds (default: 2)',
                        type=int)
    parser.add_argument('-y',
                        dest='inc_hs',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Do not ignore hydrogens (by default, the fingerprint is generated for the H-deplete molecular graph)')
    parser.add_argument('-c',
                        dest='inc_config',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Include atom chirality (by default, atom chirality is not considered)')

    return parser.parse_args()
    
def main() -> None:
    args = parseArgs()

    # create reader for input molecules (format specified by file extension)
    reader = Chem.MoleculeReader(args.in_file) 

    # open output file storing the generated fingerprints
    out_file = open(args.out_file, 'w')
    
    # create an instance of the default implementation of the Chem.Molecule interface
    mol = Chem.BasicMolecule()

    # read and process molecules one after the other until the end of input has been reached
    try:
        while reader.read(mol):
            try:
                fp = genECFP(mol, args.num_bits, args.radius, args.inc_hs, args.inc_config)

                out_file.write(str(fp))
                out_file.write('\n')

            except Exception as e:
                sys.exit('Error: processing of molecule failed: ' + str(e))
                
    except Exception as e: # handle exception raised in case of severe read errors
        sys.exit('Error: reading molecule failed: ' + str(e))

    out_file.close()
    sys.exit(0)
        
if __name__ == '__main__':
    main()
