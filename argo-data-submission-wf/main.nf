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
params.input_file = ""
params.cleanup = true


include { SongScoreUpload } from "./wfpr_modules/nextflow-data-processing-utility-tools/song-score-upload@2.6.1/local_modules/main.nf" 



// please update workflow code as needed
workflow ArgoDataSubmissionWf {
  take:  // update as needed
    val registered_samples


  main:  // update as needed
    Channel
        .fromPath(params.registered_samples)
        .splitCsv(header:true)
        .map{ row-> tuple(
        row.program_id,
        row.submitter_donor_id,
        row.gender,
        row.submitter_specimen_id,
        row.specimen_tissue_source,
        row.tumour_normal_designation,
        row.specimen_type,
        row.submitter_sample_id,
        row.sample_type,
        row.matchedNormalSubmitterSampleId,
        row.EGAX,
        row.EGAN,
        row.EGAR,
        row.EGAF
        )
        }
        .set{ samples_ch }
      
     if (params.download.toLowerCase() == 'aspera') {
         EGAFs = Channel.fromList(row.EGAF.split(","))
         
         downloadAspera(EGAFs,row.program_id)
         
         if (row.json) {
             output_json=row.json
         } else {
             generatePayloads(
                row.program_id,
                row.submitter_donor_id,
                row.gender,
                row.submitter_specimen_id,
                row.specimen_tissue_source,
                row.tumour_normal_designation,
                row.specimen_type,
                row.submitter_sample_id,
                row.sample_type,
                row.matchedNormalSubmitterSampleId,
                row.EGAX,
                row.EGAN,
                row.EGAR,
                row.EGAF,
                downloadAspera.out.output_files,
                downloadAspera.out.md5_files,
            )
            output_json=generatePayloads.out.json
        }
    } else {
         EGAFs = Channel.fromList(row.EGAF.split(","))
         downloadPyega3(EGAFs,row.program_id)
         
         if (row.json) {
             output_json=row.json
         } else {         
             generatePayloads(
                row.program_id,
                row.submitter_donor_id,
                row.gender,
                row.submitter_specimen_id,
                row.specimen_tissue_source,
                row.tumour_normal_designation,
                row.specimen_type,
                row.submitter_sample_id,
                row.sample_type,
                row.matchedNormalSubmitterSampleId,
                row.EGAX,
                row.EGAN,
                row.EGAR,
                row.EGAF,
                downloadPyega3.out.output_files,
                downloadPyega3.out.md5_files,
            )
            output_json=generatePayloads.out.json
        }
         
    }
     
     SongScoreUpload(
     row.program_id,
     output_json
     )

}

// this provides an entry point for this main script, so it can be run directly without clone the repo
// using this command: nextflow run <git_acc>/<repo>/<pkg_name>/<main_script>.nf -r <pkg_name>.v<pkg_version> --params-file xxx
workflow {
  ArgoDataSubmissionWf(
    params.registered_samples
  )
}