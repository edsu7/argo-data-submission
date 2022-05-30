# Argo data submission packages

Workflow for interacting with EGA and download files off their servers using Pyega3 or Aspera.

Given a CSV file of: 
1. Registered samples
2. EGA ids (minimum EGAFs) 
3. metadata json payloads (Optional. If provided will verify elements otherwise will auto generate)

Run generate_params_json.py for nextflow params file specific to one sample:
```
python3 generate_params_json.py -o ${working_directory} -c ${input_csv} -s {sample_of_interest}
```

[For output see example_config.json ](https://github.com/edsu7/argo-data-submission#:~:text=10%20days%20ago-,example_config.json,-update%20to%20workflow)

Requires the following environment variables to be populated :
```
ASCP_SCP_HOST
ASCP_SCP_USER
ASPERA_SCP_PASS
PYEGA3_EGA_USER
PYEGA3_EGA_PASS

```
Variable variables can be set in bash via:
```
export ASCP_SCP_HOST=demo.asperasoft.com
export ASCP_SCP_USER=aspera
export ASPERA_SCP_PASS=demoaspera
export PYEGA3_EGA_USER=""
export PYEGA3_EGA_PASS=""
```
(Profiles to be added to avoid populating variables related to unused method)


Given an EGA id to download via Pyega3 - The following directories are populated:
```
Nextflow instance
  |--DOWNLOAD.SUCCESS (or DOWNLOAD.FAILURE Flag)
  |--download.log (bash log of download)
  |--pyega3_output.log (Pyega3 generated log)
  |--EGAFXXXXXXXXXXX
    |--EGA download file
    |--EGA file md5sum
```

Given an File to download via Aspera - The following directories are populated:
```
Nextflow instance
  |--download.log (bash log of download)
  |--PROJECT_NAME
    |--FILE_NAME
      |--EGA download file
      |--EGA file md5sum
      |--DOWNLOAD.SUCCESS (or DOWNLOAD.FAILURE Flag)
      |--MD5SUM.SUCCESS (or MD5SUM.FAILURE Flag)
```
