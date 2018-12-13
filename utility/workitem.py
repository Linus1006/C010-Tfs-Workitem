#!/usr/bin/env python3
#coding=utf-8
import re

class WorkItem:
    def __init__(self):
        '''建構子'''
        pass
    
    def get_workitem(self, workitem):
        '''傳入json轉換為物件的方式傳回 如果需要多的寄送資料可以在這邊新增 違反開閉原則'''
        self.id = workitem['id']
        self.type = workitem['fields']['System.WorkItemType']
        self.title = workitem['fields']['System.Title']
        self.project = workitem['fields']['System.TeamProject']
        self.assigned = workitem['fields']['System.AssignedTo']
        self.staff_id = self.get_staff_id(self.assigned)
        self.srart_date = workitem['fields']['Microsoft.VSTS.Scheduling.StartDate']
        self.finish_date = workitem['fields']['Microsoft.VSTS.Scheduling.FinishDate']
        self.change_date = workitem['fields']['System.ChangedDate']
        
        self.html = workitem['_links']['html']['href']
        
        return self

    def get_staff_id(self, assigned):
        '''使用正規表示式取員編'''
        pattern = r'[0-9]{1,5}>'
        find = re.findall(string=assigned, pattern=pattern)[0]
        pattern = r'>'
    
        staff_id = re.split(pattern=pattern, string= find)
        return staff_id[0]

    def get_mail_address(self, staff_id, mail_lists): 
        '''使用員工編號取得mail address'''
        fliter = (mail_lists['PID'] == int(staff_id))
        return mail_lists[fliter]['EML'].values[0]
    
    def to_string(self):
        return '\n\
        id = {0} \n\
        類型 = {1} \n\
        標題 = {2} \n\
        專案 = {3} \n\
        負責人 = {4} \n\
        開始日期 = {6} \n\
        完成日期 = {7} \n\
        變更日期 = {8} \n\
        連結 = {9} \n\
        '.format(self.id,
        self.type,
        self.title,
        self.project,
        self.assigned,
        self.staff_id,
        self.srart_date,
        self.finish_date,
        self.change_date,
        self.html
        )
        