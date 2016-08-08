import yaml,os, distutils,base64

from distutils import dir_util

class Secrets(object):
    def __init__(self,file_locations):
        self.file_locations = file_locations


    def process_secrets(self):
        dir_util.mkpath(self.file_locations.release_secrets())

        for subdir, dirs, files in os.walk(self.file_locations.source_secrets()):
            for file in files:
                if file == ".DS_Store":
                    continue

                secret_out = None

                with open(os.path.join(subdir,file), 'r') as stream:
                        secret_in = yaml.load(stream)

                        data_in = secret_in['data']
                        data_out = {}
                        for k,v in data_in.iteritems():
                            data_out[k] = base64.b64encode(v)

                        secret_out = secret_in
                        secret_out['data'] = data_out
                        stream.close
                with open(os.path.join(self.file_locations.release_secrets(),file), 'w') as outfile:
                    outfile.write( yaml.dump(secret_out,default_flow_style=False,default_style='') )
                    outfile.close

    def plain_secrets(self):
        plain_secrets={}

        for subdir, dirs, files in os.walk(self.file_locations.release_secrets()):
            for file in files:
                if file == ".DS_Store":
                    continue

                secret_out = None

                with open(os.path.join(subdir,file), 'r') as stream:
                        secret_in = yaml.load(stream)

                        data_in = secret_in['data']
                        data_out = {}
                        for k,v in data_in.iteritems():
                            data_out[k] = base64.b64decode(v)

                        plain_secrets = self._merge_dicts(plain_secrets,data_out)

        return plain_secrets


    def _merge_dicts(self,x, y):
        z = x.copy()
        z.update(y)
        return z