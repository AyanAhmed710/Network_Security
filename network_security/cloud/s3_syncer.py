import os


class S3Sync:

    def sync_folder_to_s3(self,folder,bucket_url):
        command=f"aws s3 sync {folder} {bucket_url}"
        os.system(command)


    def sync_folder_from_s3(self,folder,bucket_url):
        command=f"aws s3 sync {bucket_url} {folder}"
        os.system(command)


    