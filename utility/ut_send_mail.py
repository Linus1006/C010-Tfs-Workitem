#!/usr/bin/env python3
#coding=utf-8
import esun_mail_helper as ml

mail = ml.EsunMailHelper(sender= 'ybt-11964@email.esunbank.com.tw', host= '172.17.223.39', port=25)

#測試多人
receivers = []
receivers.append('ybt-11964@email.esunbank.com.tw')
receivers.append('daniel-16053@email.esunbank.com.tw')
receivers.append('swc@email.esunbank.com.tw')
receivers.append('ctwkuan-12473@email.esunbank.com.tw')
receivers.append('joe-04414@email.esunbank.com.tw')
subject= '您的需求:2246 測試 TFS 客製化設定已逾期，請儘速處理'
body = '\n\
        id = 2246\n\
        類型 = 需求\n\
        標題 = 測試 TFS 客製化設定\n\
        專案 = C010-Tfs-Workitem\n\
        負責人 = 詹益安11965 <OANT\ESB11965>\n\
        開始日期 = 2018-12-06T00:00:00Z\n\
        完成日期 = 2018-12-06T09:00:00Z\n\
        變更日期 = 2018-12-06T05:12:46.993Z\n\
        連結 = https://tfsa0w0p02:8080/tfs/web/wi.aspx?pcguid=2fb3264f-00c6-44ca-b0ae-9e7429f12a87&id=2246'

mail.send(receivers, subject, body)
