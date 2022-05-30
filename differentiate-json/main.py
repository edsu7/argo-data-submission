#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Copyright (c) 2022, Your Organization Name

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.

  Authors:
    edsu7
"""

import os
import sys
import argparse
import subprocess
import random


def main():
    """
    Python implementation of tool: differentiate-json

    This is auto-differentiated Python code, please update as needed!
    """

    parser = argparse.ArgumentParser(description='differentiate JSON metadata payload for SONG upload')
    parser.add_argument('-a', '--program_id', dest="program_id", help="Name of the ICGC project", required=True)
    parser.add_argument('-b', '--submitter_donor_id',dest="submitter_donor_id", help="Submitter donor id conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=a%20Program%20ID.-,submitter_donor_id,-Unique%20identifier%20of", required=True)
    parser.add_argument('-c', '--gender', dest="gender", help="Gender : Female/Male/Other ", required=True)
    parser.add_argument('-d', '--submitter_specimen_id', dest="submitter_specimen_id", help="Submitter specimen id conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=Other-,submitter_specimen_id,-Unique%20identifier%20of",, required=True)
    parser.add_argument('-e', '--specimen_tissue_source', dest="specimen_tissue_source", help="Specimen tissue source conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=specimen_tissue_source", required=True)
parser.add_argument('-f', '--tumour_normal_designation', dest="tumour_normal_designation", help="Designation : Tumour/Normal", required=True)
    parser.add_argument('-g', '--specimen_type', dest="specimen_type", help="Specimen type conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=Tumour-,specimen_type,-Description%20of%20the", required=True)
    parser.add_argument('-h', '--submitter_sample_id', dest="submitter_sample_id", help="Submitter sample id conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=VIEW%20SCRIPT-,submitter_sample_id,-Unique%20identifier%20of", required=True)
    parser.add_argument('-i', '--sample_type', dest="sample_type", help="Sample type conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=CCG_34_94583%2C%20BRCA47832%2D3239%2C-,sample_type,-Description%20of%20the", required=True)
parser.add_argument('-j', '--matchedNormalSubmitterSampleId', dest="matchedNormalSubmitterSampleId", help="Using existing submitter_donor_id if tumour_normal_designation==Tumour. If Normal, leave field empty ", required=False)
    parser.add_argument('-k', '--EGAX', dest="EGAX", help="List of EGAX ids per EGA", required=False)
    parser.add_argument('-l', '--EGAN', dest="EGAN", help="List of EGAN ids per EGA", required=False)
    parser.add_argument('-m', '--EGAR', dest="EGAR", help="List of EGAR ids per EGA", required=False)
    parser.add_argument('-n', '--EGAF', dest="EGAF", help="List of EGAF ids per EGA", required=True)
    parser.add_argument('-o', '--output_files',dest="output_files",help="List of output files downloaded by pyega3/aspera", required=True)
    parser.add_argument('-p', '--md5_files', dest="md5",help="List of md5sum per output file downloaded by pyega3/aspera", required=True)
    parser.add_argument('-q', '--output_dir', dest="output_dir", help="Output directory for JSON write", required=True)

    args = parser.parse_args()

    output_dict={}
    
    output_dict["studyId"]=args.program_id
    
    output_dict["analysisType"]={}
    output_dict["analysisType"]['name']="sequencing_experiment"
    
    output_dict["samples"]=[]
    output_dict["samples"].append({})

    output_dict["samples"][0]["submitterSampleId"]=args.submitter_sample_id ###MISSING
    output_dict["samples"][0]["matchedNormalSubmitterSampleId"]=args.matchedNormalSubmitterSampleId
    output_dict["samples"][0]["sampleType"]=args.sampleType
    
    output_dict["samples"][0]['specimen']={}
    output_dict["samples"][0]['specimen']['submitterSpecimenId']=args.submitterSpecimenId
    output_dict["samples"][0]['specimen']['specimenTissueSource']=args.specimenTissueSource
    output_dict["samples"][0]['specimen']['tumourNormalDesignation']=args.tumourNormalDesignation
    output_dict["samples"][0]['specimen']['specimenType']=args.specimenType
    
    output_dict["samples"][0]['donor']={}
    output_dict["samples"][0]['donor']['gender']=args.submitter_specimen_id
    output_dict["samples"][0]['donor']['submitterDonorId']=args.submitter_specimen_id
    
    output_dict["experiment"]={}
    output_dict["experiment"]["experimental_strategy"]="WGS"
    output_dict["experiment"]["library_isolation_protocol"]=None
    output_dict["experiment"]["library_preparation_kit"]=None
    output_dict["experiment"]["library_strandedness"]=None
    output_dict["experiment"]["rin"]=None
    output_dict["experiment"]["dv200"]=None
    output_dict["experiment"]["spike_ins_included"]=None
    output_dict["experiment"]["spike_ins_fasta"]=None
    output_dict["experiment"]["spike_ins_concentration"]=None
    output_dict["experiment"]["sequencing_center"]=None
    output_dict["experiment"]["platform"]=None
    output_dict["experiment"]["platform_model"]=None
    output_dict["experiment"]["sequencing_date"]=None
    output_dict["experiment"]["submitter_sequencing_experiment_id"]=None
    
    output_dict["files"]=[]
    
    for ind,(file,EGAF,md5) in enumerate(zip(args.output_files,args.EGAF,args.md5)):
        
    
        output_dict[ind]["fileName"]=file
        output_dict[ind]["fileType"],output_dict[ind]["fileSize"]=determineFile(file)
        output_dict[ind]["dataType"]="Submitted Reads"
        output_dict[ind]["fileMd5sum"]=md5

        output_dict[ind]["info"]={}
        output_dict[ind]["info"]['experiment']=args.EGAX
        output_dict[ind]["info"]['sample']=args.EGAN
        output_dict[ind]["info"]['run']=args.EGAR
        output_dict[ind]["info"]['file']=[EGAF]
        
    output_dict['read_groups']=determineReadGroup(output_dict["files"])
    
    output_dict["read_group_count"]=len(output_dict['read_groups'])
    

                        
    

    subprocess.run(f"fastqc -o {args.output_dir} {args.input_file}", shell=True, check=True)

def determineFile(file):
    return(fileType,fileSize)

def determineReadGroup(file):
    
if __name__ == "__main__":
    main()
