import csv

def insert(filepath,item):
    with open(filepath,'a',encoding='utf-8') as f:
        fieldnames = list(item.keys())
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writerow(item)

if __name__=='__main__':
    '''
    执行程序前手动写入文件表头字段
    filepath: 文件路径
    filednames: 字段列表
    '''
    filepath= 'xxx.csv'
    with open(filepath,'a',encoding='utf-8') as f:
        fieldnames = []
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
