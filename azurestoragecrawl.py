from azure.storage.blob import BlobServiceClient
import argparse


def main():
    parser = argparse.ArgumentParser(description='Enumerate storage containers & the blobs within them by providing a connection string')
    parser.add_argument('-cs', '--connection-string', help="Azure Connection String", required=True)
    args = parser.parse_args()
    
    connectionHandle = BlobServiceClient.from_connection_string(args.connection_string)
    enumerateContainerNames(connectionHandle)

def enumerateContainerNames(connectionHandle):
    print("[...] Enumerating Azure storage container names...")
    containerList = connectionHandle.list_containers()
    for container in containerList:
        print("[+] Container discovered: {0}".format(container.name))
        enumerateBlobs(connectionHandle, container.name)

def enumerateBlobs(connectionHandle, containerName):
    print("[...] Checking {0} for any accessible storage blobs...".format(containerName))
    containerClient = connectionHandle.get_container_client(containerName)
    blobs = containerClient.list_blobs()
    for blob in blobs:
        print("[+] Blob discovered within {0} blob name: {1}".format(containerName, blob.name))
        print("[...] Downloading blob data from: {0}".format(blob.name))
        blobClient = containerClient.get_blob_client(blob.name)
        blobData = blobClient.download_blob()
        content = blobData.readall()
        print("[+] Content of blob: {0} is: {1}".format(blob.name, content.decode('utf-8')))


if __name__ == '__main__':
    main()
