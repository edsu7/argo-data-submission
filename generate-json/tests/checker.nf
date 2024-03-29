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

/*
 This is an auto-generated checker workflow to test the generated main template workflow, it's
 meant to illustrate how testing works. Please update to suit your own needs.
*/

/********************************************************************/
/* this block is auto-generated based on info from pkg.json where   */
/* changes can be made if needed, do NOT modify this block manually */
nextflow.enable.dsl = 2
version = '0.1.0'  // package version

container = [
    'ghcr.io': 'ghcr.io/icgc-argo/argo-data-submission.generate-json'
]
default_container_registry = 'ghcr.io'
/********************************************************************/

// universal params
params.container_registry = ""
params.container_version = ""
params.container = ""

// tool specific parmas go here, add / change as needed
params.input_file = ""
params.expected_output = ""

include { generateJson } from '../main'

params.program_id=''
params.submitter_donor_id=''
params.gender=''
params.submitter_specimen_id=''
params.specimen_tissue_source=''
params.tumour_normal_designation=''
params.specimen_type=''
params.submitter_sample_id=''
params.sample_type=''
params.matched_normal_submitter_sample_id=''
params.EGAX=''
params.EGAN=''
params.EGAR=''
params.EGAF=''
params.experimental_strategy=''
params.EGAD=''
params.EGAS=''
params.output_files=''
params.md5_files=''

process file_smart_diff {
  container "${params.container ?: container[params.container_registry ?: default_container_registry]}:${params.container_version ?: version}"

  input:
    path output_file
    path expected_file

  output:
    stdout()

  script:
    """
    # Note: this is only for demo purpose, please write your own 'diff' according to your own needs.
    # in this example, we need to remove date field before comparison eg, <div id="header_filename">Tue 19 Jan 2021<br/>test_rg_3.bam</div>
    # sed -e 's#"header_filename">.*<br/>test_rg_3.bam#"header_filename"><br/>test_rg_3.bam</div>#'

    diff ${output_file} ${expected_file} \
      && ( echo "Test PASSED" && exit 0 ) || ( echo "Test FAILED, output file mismatch." && exit 1 )
    """
}


workflow checker {
  take:
    program_id
    submitter_donor_id
    gender
    submitter_specimen_id
    specimen_tissue_source
    tumour_normal_designation
    specimen_type
    submitter_sample_id
    sample_type
    matched_normal_submitter_sample_id
    EGAX
    EGAN
    EGAR
    EGAF
    experimental_strategy
    EGAD
    EGAS
    output_files
    md5_files
    expected_output

  main:
      generateJson(
	program_id,
	submitter_donor_id,
	gender,
	submitter_specimen_id,
	specimen_tissue_source,
	tumour_normal_designation,
	specimen_type,
	submitter_sample_id,
	sample_type,
	matched_normal_submitter_sample_id,
	EGAX,
	EGAN,
	EGAR,
	EGAF,
        experimental_strategy,
        EGAD,
        EGAS,
	output_files,
	md5_files
    )

    file_smart_diff(
      generateJson.out.json_file,
      expected_output
    )
}


workflow {
  checker(
    params.program_id,
    params.submitter_donor_id,
    params.gender,
    params.submitter_specimen_id,
    params.specimen_tissue_source,
    params.tumour_normal_designation,
    params.specimen_type,
    params.submitter_sample_id,
    params.sample_type,
    params.matched_normal_submitter_sample_id,
    params.EGAX,
    params.EGAN,
    params.EGAR,
    params.EGAF,
    params.experimental_strategy,
    params.EGAD,
    params.EGAS,
    params.output_files,
    params.md5_files,
    params.expected_output
  )
}
