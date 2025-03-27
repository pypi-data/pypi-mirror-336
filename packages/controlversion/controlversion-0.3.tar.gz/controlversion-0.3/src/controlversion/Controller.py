from git import Repo
import gitlab
import os

class Controller:
        
    def __init__(self,rt,token):
        self.data = []
        self.rt = rt
        self.token = token
        self.__gl = gitlab.Gitlab(self.rt, private_token=self.token)
    
    def get_groups(self):
        group = self.__gl.groups.list(get_all=True)
        return group
    
    def get_reports_from_grup(self,id):
        group = self.__gl.groups.get(id, lazy=True)
        project_lst = group.projects.list(get_all=True)  #pagination
        projects = []
        for item in project_lst:
            projects.append([item.attributes['id'],item.attributes['path']])
        return projects
    
    def _get_data_repo(self,id):
        return self.__gl.projects.get(id)
    
    def clone_repo(self,id,rut_clone):
        if id:
            rp = self._get_data_repo(id)
            rp_dir = rut_clone+'/'+rp.http_url_to_repo.split('.git')[0].split('/')[-1]
            if not os.path.exists(rp_dir):
                os.makedirs(rp_dir)
            Repo.clone_from(rp.http_url_to_repo, rp_dir)
            return True
        else:
            return False
        
    def clone_all_group(self,id,rut_clone):
        group = self.__gl.groups.get(id, lazy=True)
        for repo in group.projects.list(get_all=True):
            rp_dir = rut_clone+'/'+repo.http_url_to_repo.split('.git')[0].split('/')[-1]
            if not os.path.exists(rp_dir):
                os.makedirs(rp_dir)
            Repo.clone_from(repo.http_url_to_repo, rp_dir)