#!/usr/bin/python
import sys
import getopt

# class to search the # of URLs to be regsitered in a file

class noofURLs:

        def __init__(self,file_name):
                self.file_name = file_name
                self.noofurls = 1   # Assuming the funtion was called only when there was atleast one valid change in the file
                self.firsturl = 0   # Since we have not set a first url change this value is 0
                

        def search(self):               #search and let you know if the string(URL) exists.
                f=open(self.file_name,"r")
                for i in f:
                        l= i.split()
                        for s in l:
                                spt=s.split('=')
                                for j in spt:
                                        if j == 'url':
                                                if self.firsturl > 1:
                                                        self.noofurls= self.noofurls + 1
                        self.firsturl=self.firsturl + 1
                f.close()
        

#class to find URL & ACO and validate their present in the vhost

class find_obj:


        def __init__(self,file_name,server_conf):
        #Global Vairables
                self.file_name = file_name
                self.server_conf = server_conf
                self.vhost_template = 'input_files/vhost_template.txt'
                self.found_url = 0
                self.found_aco = 0
                self.list_url = []
                self.list_aco = []
                self.aco_find = 0
                self.url_find = 0
                self.hnv = 0  #counters to make sure hostnames is updated only once
                self.rhnv =0

        #funtion to find objects

        def find(self): #find and get the objects
                f = open(self.file_name,"r")
                for i in f:
                        l= i.split()
                        for s in l:
                                spt=s.split('=')
                                for j in spt:
                        #the following conditions are for creating the list or url and aco to be added to the server.conf file
                                        if j == 'url':
                                                self.found_url = self.found_url +1
                                                continue
                                        if j == 'aco':
                                                self.found_aco = self.found_aco +1
                                                continue
                                        if self.found_url > 0:
                                                j = j.lower()
                                                self.list_url.append(j)
                                                self.found_url = self.found_url -1
                                        if self.found_aco > 0:
                                                j = j.lower()
                                                self.list_aco.append(j)
                                                self.found_aco = self.found_aco -1
                f.close()                       


        #function to validate objects against server.conf

        def validate(self):
                while self.aco_find < len(self.list_aco):
                #Local Variables
                        f=open(self.server_conf,"r")
                        f.seek(0) # moving the file pointer to the start
                        aco_present= 'false'
                        url_present= 'false'
                        aco=self.list_aco[self.aco_find]
                        search_stg= '<VirtualHost name=' + aco  # vhost syntax as per the server.conf file
                        url_find = 0   # counter for validating URL is registered to an existing ACO
        # This section looks up to see if the aco &/ URL are present in the configurations.
                        for i in f:
                                if search_stg in i: # if true the aco is present
                                        aco_present='true'
                                        continue
                                if (aco_present == 'true' and 'hostnames' in i): #Based on the format of the vhost next hostnames in 'i' is within the vhost 
                                        j = i.split('=')
                                        for k in j:
                                                if self.list_url[self.url_find].lstrip('"').rstrip('"') in k:
                                                        url_present= 'true'
                                                        break
                                if (aco_present == 'true' and url_present == 'true'): # if both r present get of this loop
                                        break
                                if (aco_present  == 'true' and i == '</VirtualHost>'): # come to the end of vhost
                                        break
                        if (aco_present == 'true' and url_present == 'true'):
                                self.aco_find = self.aco_find +1
                                self.url_find = self.url_find +1
                                continue        #continue with the next aco & url in the while loop
         #This loop validates if URL is registered to someother ACO
                        f.seek(0)
                        for i in f:
                                if self.list_url[self.url_find].lstrip('"') in i:
                                        print 'URL is already registered to an existing ACO', self.list_url[self.url_find]
                                        url_find = 1
                                        break
                        f.close()
                        if url_find == 1:
                                self.aco_find = self.aco_find +1
                                self.url_find = self.url_find +1
                                continue

         #This section deals with the case where aco is not present so creates a new vhost
                        if aco_present == 'false':
                                s= open(self.vhost_template,'r')
                                d= open(self.server_conf,'a')
                                for i in s:
                                        if '<VirtualHost name=' in i:
                                                i = i.translate(None,i[-3:])
                                                i = i + self.list_aco[self.aco_find] + '>' + '\n'
                                        if ('hostnames' in i and self.hnv == 0):
                                                hn = self.list_url[self.url_find].lstrip('"')
                                                j = i.split('=')
                                                for k in j:
                                                        if 'hostnames' in k:
                                                                i = k
                                                                continue
                                                        else:
                                                                m = k.strip('\n').replace('\"','')  #python cannot make changes to existing string so new string m is created
                                                                i = i + '=' + '"' + m
                                                                break
                                                i = i + hn + '\n'
                                                self.hnv = 1
                                        if ('redirectrewritablehostnames' in i and self.hnv == 1 and self.rhnv == 0):
                                                rhn = 'awsbe-' + self.list_url[self.url_find].lstrip('"')
                                                j = i.split('=')
                                                for k in j:
                                                        if 'redirectrewritablehostnames' in k:
                                                                i = k
                                                                continue
                                                        else:
                                                                m = k.strip('\n').replace('\"','')
                                                                i = i + '=' + '"' + m
                                                                break
                                                i = i + rhn + '\n'
                                                self.rhnv = 1
                                        d.write(i)
                                self.hnv = 0  #counters to make sure hostnames is updated only once
                                self.rhnv =0
                                s.close()
                                d.close()
                                print 'NEW vhost has been created'
         #This section deals with the case where URL is not present but aco is , so adds the url
                        if (aco_present== 'true' and url_present == 'false'):
                                 s=open(self.server_conf,'r+')
                                 rl = s.readlines()
                                 s.seek(0)
                                 vh = 0  # counter to make sure the correct vhost is reached.
                                 for i in rl:
                                        if search_stg in i:
                                                vh = 1
                                        if ('hostnames' in i and vh == 1 and self.hnv == 0):
                                                hn = self.list_url[self.url_find].lstrip('"')
                                                j = i.split('=')
                                                for k in j:
                                                        if 'hostnames' in k:
                                                                h = k
                                                                continue
                                                        else:
                                                                m = k.strip('\n').replace('\"','')
                                                                h = h + '=' + '"' + m + ','
                                                                break
                                                h = h + hn + '\n'
                                                self.hnv = 1
                                                s.write(h) # writing the line with added site URL
                                                continue
                                        if ('redirectrewritablehostnames' in i and self.hnv == 1 and self.rhnv == 0 and vh == 1):
                                                rhn = 'awsbe-' + self.list_url[self.url_find].lstrip('"')
                                                j = i.split('=')
                                                for k in j:
                                                        if 'redirectrewritablehostnames' in k:
                                                                rh = k
                                                                continue
                                                        else:
                                                                m = k.strip('\n').replace('\"','')
                                                                rh = rh + '=' + '"' + m + ','
                                                                break
                                                rh = rh + rhn + '\n'
                                                self.rhnv = 1
                                                s.write(rh)  # Writing the line with added awsbe- site url
                                                if (self.hnv == 1 and self.rhnv == 1 and vh == 1):
                                                        vh = 0
                                                        continue
                                        s.write(i)
                                 self.hnv = 0  #counters to make sure hostnames is updated only once
                                 self.rhnv =0   
                                 s.close()
                                 print 'NEW URL has been added to the existing ACO'
                        self.url_find = self.url_find +1
                        self.aco_find = self.aco_find +1
                        aco_present = ''
                        url_present= ''
                        aco= ''
                        search_stg= ''


def main(argv):

        #Local Variables
        server_file_name =''
        reg_file =''
          
        try:
            opts, args = getopt.getopt(argv, "s:r:h")
        except getopt.GetoptError:
            print("s3.py -s 'server.conf' -r 'reg.xml'")
            print("url-reg.py -s 's3_upload/server.conf' -r 's3_download/registration.xml'")
            sys.exit(2)

        for opt, arg in opts:
              if opt == "-h":
                   print("s3.py -s 'server.conf' -r 'reg.xml'")
                   sys.exit()
              elif opt == "-s":
                   server_file_name = arg
              elif opt == "-r":
                   reg_file = arg
        

        #calling class to figure out # of urls

        nourls = noofURLs(reg_file)
        nourls.search()
        print 'No of URLs :', nourls.noofurls

        #calling class to figure of URL & aco names using find funtion and make config changes accordingly using validate
        o = find_obj(reg_file,server_file_name)
        o.find()
        print 'URL List:' , o.list_url
        print 'ACO List:' , o.list_aco
        o.validate()

#condition to execure main funtion
if __name__ == "__main__":
    main(sys.argv[1:])