#!/usr/bin/env python3
#coding=utf-8
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import io
import re
import difflib
import json

class TfsHelper:
    def __init__(self, url, collection, user, token):
        '''建構子'''
        self.__url = url
        self.__collection = collection
        self.__user = user
        self.__token = token
        self.__api_version = {'api-version':'4.1'}
        

    def list_projects(self):
        '''List a collection of team project properties.
            取得collection的project list'''
        tfs_url = self.__url + '{0}/_apis/projects'.format(self.__collection)
        auth_token = HTTPBasicAuth(self.__user, self.__token)

        return requests.get(url=tfs_url, params=self.__api_version, auth=auth_token, verify=True)

    #Git 版控
    def list_git_repositories(self, project):
        '''Retrieve git repositories.'''
        tfs_url = self.__url + '{0}/{1}/_apis/git/repositories'.format(self.__collection, project)
        auth_token = HTTPBasicAuth(self.__user, self.__token)

        return requests.get(url=tfs_url, params=self.__api_version, auth=auth_token, verify=False )
    
    def get_git_repositories(self, project, repository_id):
        '''Retrieve a git repository.'''
        tfs_url = self.__url + '{0}/{1}/_apis/git/repositories/{2}'.format(self.__collection, project, repository_id)
        auth_token = HTTPBasicAuth(self.__user, self.__token)

        return requests.get(url=tfs_url, params=self.__api_version, auth=auth_token, verify=False )

    def list_git_commits(self, project, repository_id):
        '''列出repository所有的commit'''
        tfs_url = self.__url + '{0}/{1}/_apis/git/repositories/{2}/commits'.format(self.__collection, project, repository_id)
        auth_token = HTTPBasicAuth(self.__user, self.__token)

        return requests.get(url=tfs_url, params=self.__api_version, auth=auth_token, verify=False )

    def get_git_commit_info(self, project, repository_id, commit_id):
        '''列出單一commit資料'''
        tfs_url = self.__url + '{0}/{1}/_apis/git/repositories/{2}/commits/{3}'.format(self.__collection, project, repository_id, commit_id)
        auth_token = HTTPBasicAuth(self.__user, self.__token)

        return requests.get(url=tfs_url, params=self.__api_version, auth=auth_token, verify=False )

    def get_git_changes(self, project, repository_id, commit_id):
        '''列出單一commit的改變'''
        tfs_url = self.__url + '{0}/{1}/_apis/git/repositories/{2}/commits/{3}/changes'.format(self.__collection, project, repository_id, commit_id)
        auth_token = HTTPBasicAuth(self.__user, self.__token)

        return requests.get(url=tfs_url, params=self.__api_version, auth=auth_token, verify=False )
    
    #Tfvc 版控功能
    def list_tfvc_changesets(self, project):
        '''Retrieve git repositories.'''
        tfs_url = self.__url + '{0}/{1}/_apis/tfvc/changesets'.format(self.__collection, project)
        auth_token = HTTPBasicAuth(self.__user, self.__token)

        return requests.get(url=tfs_url, params=self.__api_version, auth=auth_token, verify=False )
    
    #Work Item
    def list_workitems(self, wiql):
        ''' List Work Item 傳入work item query language 進行wit的Query'''
        tfs_url = self.__url + 'C004/_apis/wit/wiql?api-version=4.1'
        auth_token = HTTPBasicAuth(self.__user, self.__token)
        headers = {'Content-Type': 'application/json'}
        data = wiql

        return requests.post(url=tfs_url, data=json.dumps(data), auth=auth_token, verify=False, headers=headers)
    

    #共用功能
    def tfs_api_call(self, url):
        '''直接執行tfs url'''
        auth_token = HTTPBasicAuth(self.__user, self.__token)

        return requests.get(url=url, params=self.__api_version,auth=auth_token, verify=False )

    def code_compare(self, source, target):
        '''程式碼比對 回覆dict add and delete'''
        a = io.StringIO(source)
        b = io.StringIO(target)
        diff = difflib.unified_diff(a.readlines(),b.readlines(), n=0)

        add = -1
        delete = -1
        for item in diff:
            if(re.match(r'\++',item)):
                add+=1
            if(re.match(r'-+',item)): 
                delete+=1
        return {"add":add,"del":delete}