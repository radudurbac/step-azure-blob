#!/usr/bin/env python

from azure_sas_upload import upload_using_sas
import glob
import os.path
import sys

path = sys.argv[1]
storage_path = sys.argv[2]
storage_sas = sys.argv[3]

# Check if path is a single file or a directory
if os.path.isfile(path):
    files = [path]
else:
    files = glob.glob(path + '/**', recursive=True)
    files = list(filter(lambda file: os.path.isfile(file), files))

# SAS URL
sas_url_for_upload = ( storage_path + "?" + storage_sas)
# File to upload
file_to_upload = "/path/to/file/filename.zip"

# Start upload
for file_to_upload in files:
    print ("Uploading: " + file_to_upload)
    r = upload_using_sas(sas_url_for_upload, file_to_upload)
    if r != 201:
    	print ("Invalid status code received: " + str(r))
    	sys.exit(1) 
