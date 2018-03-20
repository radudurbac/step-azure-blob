#!/bin/bash

if [ -z "$WERCKER_AZURE_BLOB_PATH_OR_FILE" ]; then
  fail "You must specify a path or a file to upload to azure"
fi

if [ -z "$WERCKER_AZURE_BLOB_STORAGE_ACCOUNT" ]; then
  fail "You must specify a storage account"
fi

if [ -z "$WERCKER_AZURE_BLOB_STORAGE_SAS" ]; then
  fail "You must specify a storage SAS"
fi

IS_PYTHON=$(python --version | grep " 3.")
if [ -z "$IS_PYTHON" ]; then
  fail "Python not installed"
fi

IS_REQUESTS=$(pip -q freeze | grep requests)
if [ -z "$IS_REQUESTS" ]; then
  info "Requests package not installed. Attepmt to install it."
  pip install requests
fi

IS_AZURE=$(pip -q freeze | grep azure-storage-blob)
if [ -z "$IS_AZURE" ]; then
  info "Azure-storage-blob package not installed. Attepmt to install it."
  pip install azure-storage-blob
fi

if ! ./upload.py "$WERCKER_AZURE_BLOB_PATH_OR_FILE" "$WERCKER_AZURE_BLOB_STORAGE_ACCOUNT" "$WERCKER_AZURE_BLOB_STORAGE_SAS"; then
	fail "Unable to upload."
fi

success "Uploaded"
