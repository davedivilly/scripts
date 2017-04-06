#!/usr/bin/python

import boto3 
import sys
import getopt
from boto.s3.connection import S3Connection


#class to perform file operations
class file_ops:

        def __init__(self,regFile):
        #Global Variables
                self.regFile=regFile 
                re = open(self.regFile,"r")

                #Reading the file
                for i in re:
                        if 'AWS_REG'in i:
                                j=i.split('=')
                                for n in j:
                                        if 'AWS_REG' in n:
                                                continue
                                        else:
                                                self.AWS_REGION= ''.join(n.split())
                        if 'ACC_KEY' in i:
                                 j=i.split('=')
                                 for n in j:
                                      if 'ACC_KEY'in n:
                                                continue
                                      else:
                                              self.ACCESS_KEY= ''.join(n.split())
                        if 'ACC_SEC' in i:
                                 j=i.split('=')
                                 for n in j:
                                        if 'ACC_SEC' in n:
                                                continue
                                        else:
                                                self.ACCESS_SECRET= ''.join(n.split())
                        if 'BUC_NAM' in i:
                                 j=i.split('=')
                                 for n in j:
                                       if 'BUC_NAM' in n:
                                                continue
                                       else:
                                                self.BUCKET_NAME= ''.join(n.split())

                re.close()

                 #Connecting to the bucket

                self.s3 = boto3.resource('s3',
                     region_name=self.AWS_REGION,
                     aws_access_key_id=self.ACCESS_KEY,
                     aws_secret_access_key=self.ACCESS_SECRET)

                self.bucket = self.s3.Bucket(self.BUCKET_NAME)



        #Funtions defining file operations
        def upload_file(self,local_file_path, s3_key):
                self.file_path=local_file_path
                self.s3_key=s3_key
                self.data = open(self.file_path, 'rb')
                self.bucket.put_object(Key=self.s3_key, Body=self.data)

        def download_file(self,s3_file_name, local_file_path):
                self.s3_file_name=s3_file_name
                self.local_file_path=local_file_path
                self.bucket.download_file(self.s3_file_name,self.local_file_path)

        def delete_file(self,s3_delete_file):
                self.delete_file=s3_delete_file
                self.s3.Object(self.BUCKET_NAME,s3_delete_file).delete()


def main(argv):
           local_file_name =''
           config_file =''
           dest_file_name=''
           dest_removal_file=''
           operation=''

           try:
                opts, args = getopt.getopt(argv, "m:c:d:l:r:h")
           except getopt.GetoptError:
                print("-m=download OR upload OR delete;/n c=config_file;/n d=dest_file_name;/n l=local_file_name") 
                print("./bucket-ops.py -m delete -c config_file -r dest_file_name")
                print("./bucket-ops.py -m download -c config_file -d dest_file_name -l local_file_name")
                sys.exit(2)

        #Assigning parameters that were inputted

           for opt, arg in opts:
                if opt == "-h":
                        print("Options:" + '\n' + "         m=download OR upload OR delete"+ '\n'+"         c=config_file" + '\n' + "         d=dest_file_name"+ '\n' + "         l=local_file_name" + '\n' + "         r=s3_file_to_remove" + '\n')
                        print("Example:"+ '\n' + "         ./bucket-ops.py -m download -c config_file -d dest_file_name -l local_file_name" + '\n' + "         ./bucket-ops.py -m upload -c config_file -d dest_file_name -l local_file_name" + '\n' + "         ./bucket-ops.py -m delete -c config_file -r file_to_delete"+ '\n')
                        sys.exit()
                elif opt == "-c":
                        config_file = arg
                elif opt == "-l":
                        local_file_name = arg
                elif opt == "-d":
                        dest_file_name = arg
                elif opt == "-m":
                        operation = arg
                elif opt == "-r":
                        dest_removal_file = arg

        #Validating the input parameters are correct and taking appropriate action


           if config_file =='':
                print ' Use the -h option for correct parameters'
                sys.exit()
           fo = file_ops(config_file)
           if operation == 'download':
                if  config_file =='' or dest_file_name=='' or local_file_name =='':
                        print ' Use the -h option for correct parameters'
                        sys.exit()
                fo.download_file(dest_file_name,local_file_name)
           elif operation == 'upload':
                if  config_file =='' or dest_file_name=='' or local_file_name =='':
                        print ' Use the -h option for correct parameters'
                        sys.exit()
                fo.upload_file(local_file_name,dest_file_name)
           elif operation == 'delete':
                if  config_file =='' or dest_removal_file=='':
                        print ' Use the -h option for correct parameters'
                        sys.exit()
                fo.delete_file(dest_removal_file)
           elif operation == '':
                        print("Missing operation option, that is -m option is missing")
                        sys.exit()
           else:
                print("Invalid Option -m download OR Upload")

if __name__ == "__main__":
    main(sys.argv[1:])