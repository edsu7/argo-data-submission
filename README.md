# Argo data submission packages

Workflow for interacting with EGA and download files off their servers using Pyega3 or Aspera.

Requires the following environment variables to be populated:
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
```

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
