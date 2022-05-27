#!/usr/bin/env nextflow

/*
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
    Edmund Su
*/

nextflow.enable.dsl = 2
version = '0.1.0'  // package version

// universal params go here, change default value as needed
params.container = ""
params.container_registry = ""
params.container_version = ""
params.cpus = 1
params.mem = 1  // GB
params.publish_dir = ""  // set to empty string will disable publishDir

// tool specific parmas go here, add / change as needed
params.cleanup = true

params.registered_samples=''
params.method=''
params.program_id=''
params.submitter_donor_id=''
params.gender=''
params.submitter_specimen_id=''
params.specimen_tissue_source=''
params.tumour_normal_designation=''
params.specimen_type=''
params.submitter_sample_id=''
params.sample_type=''
params.matchedNormalSubmitterSampleId=''
params.EGAX=''
params.EGAN=''
params.EGAR=''
params.EGAF=''
params.json=''

include { SongScoreUpload } from "./wfpr_modules/nextflow-data-processing-utility-tools/song-score-upload@2.6.1/main.nf" 
include { downloadAspera } from "./wfpr_modules/download-aspera/main.nf"
include { downloadPyega3 } from "./wfpr_modules/download-pyega3/main.nf"
include { generateJson } from "./wfpr_modules/generate-json/main.nf"
//include { diffJson } from "./wfpr_modules/differentiate-json/main.nf"

workflow ArgoDataSubmissionWf {
  take:
    method
    program_id
    submitter_donor_id
    gender
    submitter_specimen_id
    specimen_tissue_source
    tumour_normal_designation
    specimen_type
    submitter_sample_id
    sample_type
    matchedNormalSubmitterSampleId
    EGAX
    EGAN
    EGAR
    EGAF
    json
    
  main:

    EGAFs = Channel.from(EGAF.split(","))
    if (method.toLowerCase() == 'aspera') {
      downloadAspera(EGAFs,program_id)
      output_files=downloadAspera.out.output_files.collect()
      output_md5=downloadAspera.out.md5_file.collect()
    } else {
      downloadPyega3(EGAFs,program_id)
      output_files=downloadPyega3.out.output_files.collect()
      output_md5=downloadPyega3.out.md5_file.collect()
    }    
    
    generatePayloads(
      program_id,
      submitter_donor_id,
      gender,
      submitter_specimen_id,
      specimen_tissue_source,
      tumour_normal_designation,
      specimen_type,
      submitter_sample_id,
      sample_type,
      matchedNormalSubmitterSampleId,
      EGAX,
      EGAN,
      EGAR,
      EGAF,
      output_files,
      output_md5
    )
   
    if (json.size()>0){
      diffJson(json,generatePayloads.out.json)
      output_json=json
    } else {
      output_json=generatePayloads.out.json
    }


    SongScoreUpload(
      program_id,
      output_json
    )
  
    emit:
      output_json
      output_files
      output_analysis_id=SongScoreUpload.out.analysis_id
}

// this provides an entry point for this main script, so it can be run directly without clone the repo
// using this command: nextflow run <git_acc>/<repo>/<pkg_name>/<main_script>.nf -r <pkg_name>.v<pkg_version> --params-file xxx
workflow {
  ArgoDataSubmissionWf(
    params.method,
    params.program_id,
    params.submitter_donor_id,
    params.gender,
    params.submitter_specimen_id,
    params.specimen_tissue_source,
    params.tumour_normal_designation,
    params.specimen_type,
    params.submitter_sample_id,
    params.sample_type,
    params.matchedNormalSubmitterSampleId,
    params.EGAX,
    params.EGAN,
    params.EGAR,
    params.EGAF,
    params.json
  )
}
