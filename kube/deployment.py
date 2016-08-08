import sys,os, distutils, yaml,subprocess,hashlib, jinja2,traceback
from os.path import basename
from jinja2 import Environment, FileSystemLoader
from distutils import dir_util
from distutils import file_util


from file_locations import FileLocations
from secrets import Secrets

class Deployment(object):


    def __init__(self,**kwargs):
        self.kube_root=kwargs['kube_root']
        self.cluster=kwargs['cluster']
        self.secrets_root = os.path.realpath(os.path.realpath(os.path.join(self.kube_root,'..','openstack-kube-secrets')))
        self.file_locations= FileLocations(kube_root=self.kube_root,secrets_root=self.secrets_root,cluster=self.cluster)

    def execute(self):

        if not os.path.isdir(self.file_locations.cluster_root()):
            dir_util.mkpath(self.file_locations.cluster_root())

        if os.path.isdir(self.file_locations.release_root()):
            dir_util.remove_tree(self.file_locations.release_root())

        dir_util.mkpath(self.file_locations.release_root())

        for source,destination in self.file_locations.location_mappings().iteritems() :
           dir_util.copy_tree(source, destination)



        print "Preparing Openstack release for {} environment.".format(self.cluster)

        print "Preparing secrets"
        secrets = Secrets(self.file_locations)
        secrets.process_secrets()

        cluster_config = self._merge_dicts(self.cluster_config(),self.secrets_config(),self.images_config(),)

        print "Preparing config"
        self._prepare_specs(self.file_locations.release_etc(),cluster_config)

        print "Preparing start scripts"
        self._prepare_specs(self.file_locations.release_bin(),cluster_config)


        print "Preparing consolated config maps"
        self._prepare_configmaps()


        file_util.copy_file(os.path.join(self.file_locations.source_local_configmaps(),"cluster-configmap.yaml"),os.path.join(self.file_locations.release_configmaps()))
        file_util.copy_file(os.path.join(self.file_locations.source_local_configmaps(),"image-versions.yaml"),os.path.join(self.file_locations.release_configmaps()))



        print "Preparing checksums"
        self._prepare_checksums(self.file_locations.release_configmaps(),self.file_locations.release_secrets())


        print "Preparing specs"
        self._prepare_specs(self.file_locations.release_openstack(),cluster_config)







    def _prepare_component_specs(self,subdir,template, component_configs,cluster_config, destination_dir):
        for config in component_configs:

            if os.path.join(subdir).endswith(config['template']) :
                print "Generating component spec from {} for {}".format(config['template'],config['name'])

                target_dir = os.path.join(self.file_locations.release_openstack(),destination_dir)
                if not os.path.isdir(target_dir) :
                    os.mkdir(target_dir)

                target_file = config.get('spec_type', template.name.rsplit( ".", 1 )[0])
                with open(os.path.join(target_dir, "{}-{}".format(config['name'],target_file)), 'w') as stream:
                    stream.write(template.render(component_config=config,cluster_config=cluster_config,checksums=self.checksums()))
                    stream.close()





    def images_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_configmaps(),"image-versions.yaml"),'data')

    def cluster_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_configmaps(),"cluster-configmap.yaml"),'data')

    def share_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_config(), "shares.yaml"),'shares')

    def monasca_kafka_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_config(),"monasca-kafka-cluster.yaml"),'kafka-cluster')

    def monasca_es_data_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_config(),"monasca-es-data-cluster.yaml"),'es-data-cluster')

    def monasca_zookeeper_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_config(),"monasca-zookeeper-cluster.yaml"),'zookeeper-cluster')

    def hypervisor_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_config(),"hypervisors.yaml"),'hypervisors')

    def volume_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_config(),"volumes.yaml"),'volumes')

    def neutron_agent_config(self):
        return self._load_yaml_config(os.path.join(self.file_locations.release_config(),"neutron-agents.yaml"),'neutron.agents')


    def checksums(self):
        path =  os.path.join(self.file_locations.release_root(),"checksums.yaml")
        if not os.path.isfile(path) :
            return {}

        return self._load_yaml_config(path,'checksums')


    def secrets_config(self):
        secrets = Secrets(self.file_locations)

        return secrets.plain_secrets()


    def _load_yaml_config(self,config_file,root):
        with open(config_file, 'r') as stream:
            try:
                return  yaml.load(stream)[root]
            except yaml.YAMLError as exc:
                print(exc)

    def _prepare_specs(self,root, cluster_config):


        for subdir, dirs, files in os.walk(root):
            for file in files:
                if file == ".DS_Store":
                    continue

                env = Environment(loader=FileSystemLoader(subdir))
                template = env.get_template(file)



                if file.endswith('.template'):
                    env = Environment(loader=FileSystemLoader(subdir))
                    template = env.get_template(file)

                    self._prepare_component_specs(subdir,template,self.hypervisor_config(),cluster_config,'nova-hypervisors')
                    self._prepare_component_specs(subdir,template,self.volume_config(),cluster_config,'cinder-volumes')
                    self._prepare_component_specs(subdir,template,self.share_config(),cluster_config,'manila-shares')
                    self._prepare_component_specs(subdir,template,self.neutron_agent_config(),cluster_config,'neutron-agents')
                    self._prepare_component_specs(subdir,template,self.monasca_zookeeper_config(),cluster_config,'monasca-zookeeper')
                    self._prepare_component_specs(subdir,template,self.monasca_kafka_config(),cluster_config,'monasca-kafka')
                    self._prepare_component_specs(subdir,template,self.monasca_es_data_config(),cluster_config,'monasca-es-data')


                else:
                    with open(os.path.join(subdir, file), 'w') as stream:
                        try:
                            stream.write(template.render(cluster_config=cluster_config,checksums=self.checksums()))
                        except Exception as e:
                            print "Failed to process spec {}: {}".format(os.path.join(subdir, file), repr(e))
                            traceback.print_exc(file=sys.stderr)
                        stream.close()



    def _prepare_configmaps(self):

        config={}

        self._build_config(self.file_locations.release_etc(),config)
        self._build_config(self.file_locations.release_bin(),config)
        self._build_config(self.file_locations.release_patches(),config)

        for subdir, dirs, files in os.walk(self.file_locations.release_configmaps()):
            base = os.path.basename(subdir)

            for file in files:
                if file == ".DS_Store":
                    continue

                env = Environment(loader=FileSystemLoader(subdir))
                template = env.get_template(file)

                #with open(os.path.join(subdir, file), 'r') as stream:
                #    config_map = yaml.load(stream)
                #    stream.close()

                #for k,v in config_map['data'].iteritems():
                #    config_map['data'][k] =  literal(config.get(k))


                #yaml.add_representer(literal, literal_presenter)

                #with open(os.path.join(subdir, file), 'w') as outfile:
                #    outfile.write( yaml.dump(config_map,default_flow_style=False,default_style='') )
                #    outfile.close

                with open(os.path.join(subdir, file), 'w') as stream:
                    try:
                        stream.write(template.render(config=config))
                    except Exception as e:
                        print "Failed to process configmap {}: {}".format(os.path.join(subdir, file), repr(e))
                        traceback.print_exc(file=sys.stderr)
                    stream.close()


    def _build_config(self,path,config):

        for subdir, dirs, files in os.walk(path):

            base = os.path.relpath(subdir, path)
            if base == ".":
                base = None

            for file in files:
                if file == ".DS_Store":
                    continue

                if base:
                    key = "{}/{}".format(base,file)
                else:
                    key = file

                with open(os.path.join(subdir, file), 'r') as stream:
                    data=stream.read()
                    stream.close()

                if config.get(key) :
                    print "Duplicate script or config detected for name {} in base path {} please check output release".format(file,base);

                config[key] = jinja2.filters.do_indent(data,4)



    def _prepare_checksums(self,*sources):
        checksums = {'checksums':{}}
        for i,root in enumerate(sources):
            for subdir, dirs, files in os.walk(root):
                for file in files:
                  path = os.path.join(subdir,file)
                  checksums['checksums'][file] = self._md5(path)

        with open(os.path.join(self.file_locations.release_root(),'checksums.yaml'), 'w') as outfile:
            outfile.write( yaml.dump(checksums,default_flow_style=False,default_style='') )
            outfile.close


    def _merge_dicts(self,x, *args):
        z = x.copy()
        for i,dict in enumerate(args):

            z.update(dict)

        return z



    def _md5(self,fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        #return "{}-2".format(hash_md5.hexdigest())
        return hash_md5.hexdigest()




def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

class literal(str): pass

