# Azure Blob Upload Path or File

Uploads an entire directory structure to azure storage blob, or a specific file maintaining the file relative path.

You will need to create a storage and a SAS in Azure.

## Prerequisites

* Python 3.x
* pip install requests 
* pip install azure-storage-blob

Example:

    build:
      steps:
        - petrica/azure-blob:
            path_or_file: /path/file.txt
            storage_account: https://mystorage.blob.core.windows.net/myblob
            storage_sas: sv=2017-07-29&ss=b&srt=sco&sp=rwdlac&se=2018-03-20T21:34:39Z&st=2018-03-20T13:34:39Z&spr=https&sig=aAB4NrDgCbm7uYUCrEsD1A8kVozL2G5GURB80b618vw%3D




