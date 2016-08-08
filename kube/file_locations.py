import os

class FileLocations(object):
    def __init__(self,**kwargs):
        self.kube_root = kwargs['kube_root']
        self.secrets_root = kwargs['secrets_root']
        self.cluster = kwargs['cluster']
        self._check_directory(self.kube_root,message="Not sure how you managed this, but the openstack kube root repo appears to missing")
        self._check_directory(self.secrets_root,message="Kube secrets repo does not exist. It should be cloned at the smae level as the main repository")

    def config_root(self):
        return os.path.join(self.kube_root,"config")

    def cluster_root(self):
        return os.path.join(self.config_root(),"clusters",self.cluster)


    def local_root(self):
        return os.path.join(self.secrets_root,"clusters",self.cluster)

    def local_root(self):
        return os.path.join(self.secrets_root,"clusters",self.cluster)


    def _config_path(self,*locations):
        path = os.path.join(self.config_root(),*locations)
        self._check_directory(path)
        return path

    def _release_path(self,*locations):
        return os.path.join(self.release_root(),*locations)

    def _check_directory(self,location,**kwargs):
        message = kwargs.get('message',"File location {} does not exist".format(location))
        if not os.path.isdir(location):
            raise Exception(message)

    def source_openstack(self):
        return self._config_path("openstack")

    def source_global_etc(self):
        return self._config_path("etc")


    def source_volumes(self):
        return self._config_path("volumes")


    def source_local_etc(self):
        return self._config_path(self.local_root(),"etc")

    def source_local_configmaps(self):
        return self._config_path(self.local_root(),"configmaps")

    def source_bin(self):
        return self._config_path("bin")

    def source_configmaps(self):
        return self._config_path("configmaps")

    def source_cluster_config(self):
        return self._config_path(self.local_root(),"config")

    def source_patches(self):
        return self._config_path("patches")

    def source_secrets(self):
        return os.path.realpath(os.path.join(self.secrets_root,"clusters",self.cluster,"secrets"))

    def release_root(self):
        return os.path.join(self.cluster_root(),'release')

    def release_openstack(self):
        return self._release_path("openstack")

    def release_etc(self):
        return self._release_path("etc")

    def release_config(self):
        return self._release_path("config")


    def release_bin(self):
        return self._release_path("bin")

    def release_configmaps(self):
        return self._release_path("configmaps")

    def release_patches(self):
        return self._release_path("patches")

    def release_secrets(self):
        return self._release_path("secrets")

    def release_volumes(self):
        return self._release_path("volumes")



    def location_mappings(self):
        return   {  self.source_openstack():self.release_openstack(),
                    self.source_global_etc():self.release_etc(),
                    self.source_cluster_config():self.release_config(),
                    self.source_local_etc():self.release_etc(),
                    self.source_bin():self.release_bin(),
                    self.source_volumes():self.release_volumes(),
                    self.source_configmaps():self.release_configmaps(),
                    self.source_local_configmaps():self.release_configmaps(),
                    self.source_patches():self.release_patches()
                 }