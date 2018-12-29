import hashlib
import os
import requests



class Update_md5(object):

    def __init__(self, url):
        self.url = url
        self.filename = url[-36:]
        self.download()

    def download(self):
        with open("./{}".format(self.filename), "wb") as f:
            f.write(requests.get(self.url).content)

    def getFileMD5(self):
        f = open("./{}".format(self.filename), 'rb')
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        f.close()
        return str(hash).upper()

    def __del__(self):
        os.remove("./"+self.filename)