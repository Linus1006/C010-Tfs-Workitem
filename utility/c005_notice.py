#!/usr/bin/env python3
#coding=utf-8
import tfs_api_helper as th
import pandas as pd
import re
import workitem as wit
import esun_mail_helper as ml
import sys

def main():
    '''程式進入點'''
    print(sys.path)
    tfs = th.TfsHelper(url='https://tfsa0w0p02:8080/tfs/', collection='C004', user='ESB11964', token='lfj2ve7ttgozouyvvb3azmlvgfvs7m47gbxmqfuw3ackoo6kzoca')
    mail_lists = pd.read_csv('./email_rank.csv', encoding = 'utf-8', skipinitialspace = True)
    
    overdue_notice(tfs, mail_lists)
    need_help_notice(tfs, mail_lists)
    maybe_delay_notice(tfs, mail_lists)

def overdue_notice(tfs, mail_lists):
    '''工作逾期通知'''

    wiql = {'query': 'Select [System.ID] From WorkItems \
    Where [System.TeamProject] = "C010-Tfs-Workitem" \
    AND [Microsoft.VSTS.Scheduling.FinishDate] < @Today \
    AND ([System.State] = "已提議" OR [System.State] = "作用中" )'}  
    
    tfs_list_workitems = tfs.list_workitems(wiql).json()['workItems'] #取得查詢的WIT
    wit_infos = get_workitem_infos(tfs, mail_lists, tfs_list_workitems)
    send_mail_to_wit_owner(wit_infos)
    
def need_help_notice(tfs, mail_lists):
    '''需要幫忙的通知'''
    wiql = {'query': 'Select [System.ID] From WorkItems \
    Where [System.TeamProject] = "C010-Tfs-Workitem" \
    AND [C005.CallHelp] = true AND [System.WorkItemType] = "工作" \
    AND ([System.State] = "已提議" OR [System.State] = "作用中" )'}        
    
    tfs_list_workitems = tfs.list_workitems(wiql).json()['workItems'] #取得查詢的WIT
    wit_infos = get_workitem_infos(tfs, mail_lists, tfs_list_workitems)
    send_mail_to_supervisor_help(wit_infos)

def maybe_delay_notice(tfs, mail_lists):
    '''專案可能逾期'''
    wiql = {'query': 'Select [System.ID] From WorkItems \
    Where [System.TeamProject] = "C010-Tfs-Workitem" \
    AND [C005.OnSchedule] = false AND [System.WorkItemType] = "工作" \
    AND ([System.State] = "已提議" OR [System.State] = "作用中" )'}           
    
    tfs_list_workitems = tfs.list_workitems(wiql).json()['workItems'] #取得查詢的WIT
    wit_infos = get_workitem_infos(tfs, mail_lists, tfs_list_workitems)
    send_mail_to_supervisor_delay(wit_infos)

def get_workitem_infos(tfs, mail_lists, tfs_list_workitems):
    '''取得wit資料'''
    wit_infos = []
    for i in tfs_list_workitems:
        workitem = tfs.tfs_api_call(i['url']).json() #取得詳細的wit資料
        #print(workitem)
        wit_info = wit.WorkItem().get_workitem(workitem)
        wit_info.mail_address = wit_info.get_mail_address(wit_info.staff_id, mail_lists)     
        wit_infos.append(wit_info)
    return wit_infos

def send_mail_to_supervisor_delay(wit_infos):
    
    for wit_info in wit_infos:
        mail = ml.EsunMailHelper(sender= 'swc@mail.esunbank.com.tw', host= '172.17.223.39', port=25)
        
        #組合訊息
        receivers = []
        receivers.append('ctwkuan-12473@email.esunbank.com.tw')
        receivers.append('joe-04414@email.esunbank.com.tw')
        subject = '{0}:{1} {2}可能有逾期風險，請儘速關懷'.format(wit_info.type, wit_info.id, wit_info.title)
        body = wit_info.to_string()

        print(subject)
        mail.send(receivers, subject, body)
    return 1

def send_mail_to_supervisor_help(wit_infos):
    
    for wit_info in wit_infos:
        mail = ml.EsunMailHelper(sender= 'swc@mail.esunbank.com.tw', host= '172.17.223.39', port=25)
        
        #組合訊息
        receivers = []
        receivers.append('ctwkuan-12473@email.esunbank.com.tw')
        receivers.append('joe-04414@email.esunbank.com.tw')
        subject = '{0}:{1} {2}需要幫助，請PMO儘速協助'.format(wit_info.type, wit_info.id, wit_info.title)
        body = wit_info.to_string()

        print(subject)
        mail.send(receivers, subject, body)
    return 1

def send_mail_to_wit_owner(wit_infos):
    
    for wit_info in wit_infos:
        mail = ml.EsunMailHelper(sender= 'swc@mail.esunbank.com.tw', host= '172.17.223.39', port=25)
        
        #組合訊息
        receivers = []
        receivers.append(wit_info.mail_address)
        subject = '您的{0}:{1} {2}已逾期，請儘速處理'.format(wit_info.type, wit_info.id, wit_info.title)
        body = wit_info.to_string()

        print(subject)
        mail.send(receivers, subject, body)
    return 1
    
if __name__ == "__main__":
    main()
