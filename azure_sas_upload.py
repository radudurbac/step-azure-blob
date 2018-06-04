#!/usr/bin/env python
import os
import mimetypes
from azure.storage.blob import ContentSettings
from urllib.parse import urlparse
from requests import Request, Session


def upload_using_sas(sas_url , file_name_full_path):
    """
    Upload File using Azure SAS url.
    This function uploads file to Azure blob container
    :param sas_url:  Azure sas url with write access on a blob storage
    :param file_name_full_path:  File name with fill path
    :return:  HTTP response status of file upload
    """
    o = urlparse(sas_url)
    # Remove first / from path
    if o.path[0] == '/':
        blob_storage_path = o.path[1:]
    else:
        blob_storage_path = o.path

    storage_account = o.scheme + "://" + o.netloc + "/"
    file_name_only = file_name_full_path.replace('\\', '/')
    response_status = put_blob(storage_account,blob_storage_path,file_name_only,o.query,file_name_full_path)
    return response_status


def put_blob(storage_url, container_name, blob_name, qry_string, file_name_full_path):
    """
    This function sets file extensions,
    prepares the PUT request,
    sets 'Content-Length' and clears 'Transfer-Encoding' headers for 0-size files
    :return: HTTP request status code
    """
    file_name_only = os.path.basename(file_name_full_path)
    try:
        file_ext = '.' + file_name_only.split('.')[-1]
    except IndexError:
        file_ext = None
    # Set content Type
    header = {
        'x-ms-blob-type': 'BlockBlob'
    }
    if file_ext is not None and file_ext in mimetypes.types_map:
        content_type_string = ContentSettings(content_type=mimetypes.types_map[file_ext])
        header['Content-Type'] = content_type_string.content_type

    # Set content-length header for empty files
    if os.path.getsize(file_name_full_path) == 0:
        length = os.path.getsize(file_name_full_path)
        header['Content-Length'] = str(length)

    # Prepare request headers
    with open(file_name_full_path, 'rb') as fh:
        s = Session()
        url = storage_url + container_name + '/' + blob_name + '?' + qry_string
        req = Request('PUT', url, data=fh, headers=header, params={'file': file_name_full_path})
        prepped = s.prepare_request(req)
        try:
            del prepped.headers['Transfer-Encoding']
        finally:
            response = s.send(prepped)
            return response.status_code
