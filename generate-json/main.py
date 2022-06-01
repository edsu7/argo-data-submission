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
import numpy
import json


def main():
    """
    Python implementation of tool: generate-json

    This is auto-generated Python code, please update as needed!
    """
    threads=4
    
    
    parser = argparse.ArgumentParser(description='generate JSON metadata payload for SONG upload')
    parser.add_argument('-a', '--program_id', dest="program_id", help="Name of the ICGC project", required=True)
    parser.add_argument('-b', '--submitter_donor_id',dest="submitterDonorId", help="Submitter donor id conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=a%20Program%20ID.-,submitter_donor_id,-Unique%20identifier%20of", required=True)
    parser.add_argument('-c', '--gender', dest="gender", help="Gender : Female/Male/Other ", required=True)
    parser.add_argument('-d', '--submitter_specimen_id', dest="submitterSpecimenId", help="Submitter specimen id conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=Other-,submitter_specimen_id,-Unique%20identifier%20of", required=True)
    parser.add_argument('-e', '--specimen_tissue_source', dest="specimenTissueSource", help="Specimen tissue source conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=specimen_tissue_source", required=True)
    parser.add_argument('-f', '--tumour_normal_designation', dest="tumourNormalDesignation", help="Designation : Tumour/Normal", required=True)
    parser.add_argument('-g', '--specimen_type', dest="specimenType", help="Specimen type conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=Tumour-,specimen_type,-Description%20of%20the", required=True)
    parser.add_argument('-i', '--submitter_sample_id', dest="submitterSampleId", help="Submitter sample id conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=VIEW%20SCRIPT-,submitter_sample_id,-Unique%20identifier%20of", required=True)
    parser.add_argument('-j', '--sample_type', dest="sampleType", help="Sample type conforming to ICGC-ARGO standards https://docs.icgc-argo.org/dictionary#:~:text=CCG_34_94583%2C%20BRCA47832%2D3239%2C-,sample_type,-Description%20of%20the", required=True)
    parser.add_argument('-k', '--matchedNormalSubmitterSampleId', dest="matchedNormalSubmitterSampleId", help="Using existing submitter_donor_id if tumour_normal_designation==Tumour. If Normal, leave field empty ", required=False)
    parser.add_argument('-l', '--EGAX', dest="EGAX", help="List of EGAX ids per EGA", required=False)
    parser.add_argument('-m', '--EGAN', dest="EGAN", help="List of EGAN ids per EGA", required=False)
    parser.add_argument('-n', '--EGAR', dest="EGAR", help="List of EGAR ids per EGA", required=False)
    parser.add_argument('-o', '--EGAD', dest="EGAD", help="List of EGAD ids per EGA", required=False)
    parser.add_argument('-p', '--EGAS', dest="EGAS", help="List of EGAS ids per EGA", required=False)
    parser.add_argument('-q', '--EGAF', dest="EGAF", help="List of EGAF ids per EGA", required=True)
    parser.add_argument('-r', '--output_files',dest="output_files",help="List of output files downloaded by pyega3/aspera", required=True)
    parser.add_argument('-s', '--md5_files', dest="md5",help="List of md5sum per output file downloaded by pyega3/aspera", required=True)
    

    args = parser.parse_args()

    output_dict=setupBaseDictionary()
    
    output_dict["studyId"]=args.program_id
    
    output_dict["analysisType"]['name']="sequencing_experiment"

    output_dict["samples"][0]["submitterSampleId"]=args.submitterSampleId
    output_dict["samples"][0]["matchedNormalSubmitterSampleId"]=args.matchedNormalSubmitterSampleId
    output_dict["samples"][0]["sampleType"]=args.sampleType
    
    output_dict["samples"][0]['specimen']['submitterSpecimenId']=args.submitterSpecimenId
    output_dict["samples"][0]['specimen']['specimenTissueSource']=args.specimenTissueSource
    output_dict["samples"][0]['specimen']['tumourNormalDesignation']=args.tumourNormalDesignation
    output_dict["samples"][0]['specimen']['specimenType']=args.specimenType
    
    output_dict["samples"][0]['donor']['gender']=args.gender
    output_dict["samples"][0]['donor']['submitterDonorId']=args.submitterDonorId
    
    #print(json.dumps(output_dict,indent=2))
          
    if "RNA" in args.sampleType:
        output_dict["experiment"]["experimental_strategy"]="RNAseq"
    else:
        output_dict["experiment"]["experimental_strategy"]="WGS"
    
    
    for ind,(file,md5) in enumerate(zip([args.output_files],[args.md5])):
        output_dict['files'].append(setupDictFiles())
        output_dict["files"][ind]["fileName"]=file
        output_dict["files"][ind]["fileType"]=determineFileType(file)
        output_dict["files"][ind]["fileSize"]=os.path.getsize(file)
        output_dict["files"][ind]["dataType"]="Submitted Reads"
        output_dict["files"][ind]["fileMd5sum"]=md5

        output_dict["files"][ind]["info"]={}
        output_dict["files"][ind]["info"]['experiment']=args.EGAX.split(",")
        output_dict["files"][ind]["info"]['sample']=args.EGAN.split(",")
        output_dict["files"][ind]["info"]['run']=args.EGAR.split(",")
        output_dict["files"][ind]["info"]['file']=args.EGAF.split(",")
        output_dict["files"][ind]["info"]['dataset']=args.EGAD.split(",")
        output_dict["files"][ind]["info"]['study']=args.EGAS.split(",")
    
    
    if len(set([file['fileType'] for file in output_dict['files']]))>1:
        raise ValueError("Raising error, multiple read types provided. Better to mannually annotate")
    
    print(output_dict)
    output_dict['read_groups']=determineReadGroup(output_dict["files"])
    
    output_dict["read_group_count"]=len(output_dict['read_groups'])
    
    with open("auto_generated.json", "w") as outfile:
        outfile.write(json.dumps(output_dict,indent = 2))
    
                    

    
def setupBaseDictionary():
    object_dict={}
    
    for entry in ["studyId","read_group_count"]:
        object_dict[entry]=None
        
    object_dict['analysisType']={"name":"sequencing_experiment"}
    
    object_dict['samples']=\
    [
        {"specimen":{"submitterSpecimenId":None,"specimenTissueSource":None,"specimenType":None,"tumourNormalDesignation":None},
         "donor":{"gender":None,"submitterDonorId":None},
         "submitterSampleId":None,
         "matchedNormalSubmitterSampleId":None,
         "sampleType":None
         }
    ]
    
    object_dict["experiment"]=\
    {"experimental_strategy": None,
     "sequencing_center":None,
     "platform":None,
     "platform_model":None,
     "sequencing_date":None,
     "submitter_sequencing_experiment_id":None
    }
    object_dict['files']=[]
    return(object_dict)
    
def setupDictFiles():
    return({"fileName":None,
         "fileType":None,
         "dataType":None,
         "fileSize":None,
         "fileMd5sum":None,
         "info":{
             "origin":"EGA",
             "data_category": "Sequencing Reads",
             "legacyAnalysisId":None,
             "ega_IDs":{"experiment":None,"file":None,"sample":None,"dataset":None,"study":None,"run":None}
         }
        })
def setupDictReadGroups():
    return({
          "insert_size": None,
          "platform_unit": None,
          "file_r2": None,
          "file_r1": None,
          "read_group_id_in_bam": None,
          "submitter_read_group_id": None,
          "is_paired_end": None,
          "read_length_r1": None,
          "read_length_r2": None,
          "library_name": None,
          "sample_barcode": None
        })

def determineFileType(file):
    bam_result=subprocess.run("samtools quickcheck "+file, shell=True, check=True)      
    if bam_result.returncode==0:
        return("BAM")
    
    fastq_result=subprocess.run("zcat "+file+"| head -n1 | egrep \"^@\" || false")
    if fastq_result==0:
        return("FASTQ")
    else:
        raise ValueError("'"+file+"' failed BAM and FASTQ check")
        
def determineReadGroup(file_list):
    if file_list[0]['fileType']=='BAM':
        return(determineReadGroupBam([file["fileName"] for file in file_list]))
    else:
        return(determineReadGroupFastq([file["fileName"] for file in file_list]))

def determineReadGroupBam(file_list):
    rg_dict=[]
    for file in file_list:
        
        
        ###Populate readgroups
        list_IDs=getHeaderInfo(file,"ID",4)
        print(file)
        for rg_id in list_IDs:
            rg_dict.append(setupDictReadGroups())
            rg_dict[-1]["read_group_id_in_bam"]=rg_id
            rg_dict[-1]["submitter_read_group_id"]=rg_id
            
            rg_dict[-1]["is_paired_end"]=getPairedStatus(file,rg_id,4)
            if rg_dict[-1]["is_paired_end"]:
                rg_dict[-1]["read_length_r2"]=getReadLength(file,rg_id,2,4)
                rg_dict[-1]["file_r2"]=file
                rg_dict[-1]["insert_size"]=getInsertSize(file,rg_id,4)
            
            rg_dict[-1]["read_length_r1"]=getReadLength(file,rg_id,1,4)
            rg_dict[-1]["file_r1"]=file
            rg_dict[-1]["platform_unit"]=getHeaderInfo(file,"PL",4,rg_id)
            rg_dict[-1]["library_name"]=getHeaderInfo(file,"LB",4,rg_id)
            
    return(rg_dict)
            
                
def getInsertSize(file,rg_id,threads):
    cmd="samtools view -@"+str(threads)+" -F 256 -f 128 "+file+" | egrep '^@|"+rg_id+"'  | cut -f9"
    print(cmd)
    result=subprocess.run(cmd,stdout=subprocess.PIPE,shell=True)
    return(numpy.median([abs(int(line)) for line in result.stdout.decode("utf-8").split("\n")[:-1]]))

def getReadLength(file,rg_id,read,threads):
    if read==1:
        cmd="samtools view -@"+str(threads)+" -F 256 -f 64 "+file+" | egrep '^@|"+rg_id+"'  | cut -f10"
    else:
        cmd="samtools view -@"+str(threads)+" -F 256 -f 128 "+file+" | egrep '^@|"+rg_id+"'  | cut -f10"

    result=subprocess.run(cmd,stdout=subprocess.PIPE,shell=True)
    
    if result.returncode!=0:
        raise ValueError("Error determining read length in:"+file)
        
    return(numpy.median([len(line) for line in result.stdout.decode("utf-8").split("\n")[:-1]]))
    
def getHeaderInfo(file,subject,threads,rg=None):
    if rg:
        cmd="samtools view -@"+str(threads)+" "+file+" -H | grep '@RG' | grep "+rg+" | egrep '"+subject+":[a-zA-Z0-9._:-]+' -o | sed 's/"+subject+"://g' | sort | uniq"
    else:
        cmd="samtools view -@"+str(threads)+" "+file+" -H | grep '@RG' | egrep '"+subject+":[a-zA-Z0-9._:-]+' -o | sed 's/"+subject+"://g' | sort | uniq"
        
    result=subprocess.run(cmd,stdout=subprocess.PIPE,shell=True)
    if result.returncode!=0:
        raise ValueError("No readgroups found in "+file)
    elif rg:
        return(result.stdout.decode("utf-8").split("\n")[:-1][0])
    else:
        return(list(set(result.stdout.decode("utf-8").split("\n")[:-1])))
            
def getPairedStatus(file,rg_id,threads):
    cmd="samtools view -@"+str(threads)+" "+file+" -f2 | egrep '^@|"+rg_id+"' | head | wc -l | awk '{ if ($1!=10) exit 1}' "
    result=subprocess.run(cmd,stdout=subprocess.PIPE,shell=True)
    if result.returncode!=0:
        return(False)
    else:
        return(True)

def determineReadGroupFastq(file_list):
    raise ValueError("Not yet implemented")
    
if __name__ == "__main__":
    main()
