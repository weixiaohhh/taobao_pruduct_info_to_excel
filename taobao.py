# coding:utf8
import sys
import re
import pandas as pd
import requests
import urllib
import threading
from time import sleep




# 多线程
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
       
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print "Starting " +self.name
        print "Exiting " + self.name
        
    def get_df(self,raw_url):
        url = re.sub('page=\d+','page='+str(i) ,raw_url)
        json_data = requests.get(url).json()
        df = pd.DataFrame(json_data['listItem'],columns = ['itemNumId','title',
                        'price','originalPrice','sold','nick','area',
                        'img2','url'])
        return df
    
    
def save_as_excel(all_df,fileName):
    writer =  pd.ExcelWriter(u'{}.xlsx'.format(fileName), engine='openpyxl')
    all_df[0].to_excel(writer ,index=False)

    i = 1
    for df in all_df[1:]:
        df.to_excel(writer, startrow=((len(df)+2)*i), header=None,index=False)
        i+=1
    writer.save()

    
if __name__ == "__main__":
    all_df = []
    link = 'https://s.m.taobao.com/search?q=404&tab=all&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=15&wlsort=15&page=1'
    pageNum = int(sys.argv[1])
    fileName = sys.argv[2].decode('gbk')
    all_q = sys.argv[2].split('+') # 用+代替空格查询
    print all_q
    q = '+'.join([ urllib.quote(qs.decode('gbk').encode('utf8')) for qs in all_q]) #  查询时候将空格变为+号
    print q
    raw_url = re.sub('q=\d+','q='+q,link)
    
    
    for i in range(1,pageNum):

        thread = myThread(str(i))
        thread.start()
        i+=1
        df = thread.get_df(raw_url)
        all_df.append(df)
        
    save_as_excel(all_df,fileName)
    



    




