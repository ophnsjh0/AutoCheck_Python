import re

# Tested model: Cisco C3550, C3560
# Check list is ip, model, hostname, %cpu, %memory, temp, fan, power.
# Parsing result.
class citrixParse:
    def __init__(self, rawdata):
        # rawdata is list type..
        print(rawdata)
        self.rawdata=rawdata
        # parsing result stored this dictionary...
        self.result=dict()
        

    def getip(self):
        ip=list()
        p=re.compile('^ipaddr')
        # print(p)
        for i in self.rawdata:
            m=p.search(i)
            if m:               
                i=' '.join(i.split())                
                ip=i.split(':')
                print(i)
        if ip:
            self.result['ip']=ip[1].strip()
        else:
            self.result['ip']='unknown'
        return self.result

    def getmodel(self):
        model=list()
        # p=re.compile('^Model Number')
        p=re.compile('Platform:')
        for i in self.rawdata:
            m=p.search(i)
            if m:               
                i=' '.join(i.split())
                model=i.split(' ')
                
        if model:
            self.result['model']=model[1].strip()
        else:
            self.result['model']='unknown'
        return self.result

    def gethostname(self):
        hosts=list()
        p=re.compile('set ns hostName')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                hosts=i.split(' ')
        if hosts:
            self.result['hostname']=hosts[3].strip()
        else:
            self.result['hostname']='unknown'
        return self.result

    def getcpu(self):
        cpu=list()
        p=re.compile('Packet CPU usage')
        for i in self.rawdata:
            m=p.search(i)
            if m:                
                i=' '.join(i.split())            
                cpu=i.split(' ')
                
        if cpu:
            self.result['cpu util']=cpu[-1].strip()+'%'
        else:
            self.result['cpu util']='unknown'
        return self.result

    def getmem(self):
        mem=list()
        p=re.compile('InUse Memory')
        for i in self.rawdata:
            m=p.search(i)
            if m:                
                i=' '.join(i.split())               
                mem=i.split(' ')               
        if mem:
            self.result['mem util']=mem[-1].strip()+'%'
        else:
            self.result['mem util']='unknown'
        return self.result

    def gettemp(self):
        temp=list()
        p=re.compile('Internal Temperature')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                temp=i.split(' ')
        if temp:
            self.result['temperature']=temp[-1]+'(Celsius)'
        else:
            self.result['temperature']='unknown'
        return self.result

    def getfan(self):
        fan=list()
        p=re.compile('System Fan Speed')
        for i in self.rawdata:
            # print(i)
            m=p.search(i)           
            if m:
                i=' '.join(i.split())
                fan=i
                # fan=i.split(' ')
        print(m)
        if fan:
            self.result['fan']=fan[-1]
            # self.result['fan']=fan[-1]
        else:
            self.result['fan']='unknown'
        return self.result

    def getpower(self):
        ps=list()
        p=re.compile('Power supply 1')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                ps=i.split(' ')
        if ps:
            self.result['power']=ps[-1].strip()
        else:
            self.result['power']='unknown'
        return self.result

    def saveresult(self):
        self.getip()
        self.getmodel()
        self.gethostname()
        self.getcpu()
        self.getmem()
        self.gettemp()
        self.getfan()
        self.getpower()
        return self.result
#
#    def showresult(self):
#        for key, val in self.result.items():
#            print('key={key}, value={value}'.format(key=key, value=val))




