import re

# Tested model: Cisco C3550, C3560
# Check list is ip, model, hostname, %cpu, %memory, temp, fan, power.
# Parsing result.
class C35xxParse:
    def __init__(self, rawdata):
        # rawdata is list type...
        self.rawdata=rawdata
        # parsing result stored this dictionary...
        self.result=dict()

    def getip(self):
        ip=list()
        p=re.compile('^ipaddr')
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
        p=re.compile('^Model number|^Model Number')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                model=i.split(':')
        if model:
            self.result['model']=model[1].strip()
        else:
            self.result['model']='unknown'
        return self.result

    def gethostname(self):
        hosts=list()
        p=re.compile('^.+#')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                hosts=i.split('#')
        if hosts:
            self.result['hostname']=hosts[0].strip()
        else:
            self.result['hostname']='unknown'
        return self.result

    def getcpu(self):
        cpu=list()
        p=re.compile('^CPU')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                cpu=i.split(' ')
        if cpu:
            self.result['cpu util']=cpu[-1].strip()
        else:
            self.result['cpu util']='unknown'
        return self.result

    def getmem(self):
        mem=list()
        p=re.compile('^Processor Pool')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                mem=i.split(' ')
        if mem:
            memusage=int(mem[5])*100/int(mem[3])
            self.result['mem util']=str(int(memusage))+'%'
        else:
            self.result['mem util']='unknown'
        return self.result

    def gettemp(self):
        temp=list()
        p=re.compile('^TEMPERATURE')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                temp=i.split(' ')
        if temp:
            self.result['temperature']=temp[-1]
        else:
            self.result['temperature']='unknown'
        return self.result

    def getfan(self):
        fan=list()
        p=re.compile('^FAN')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                fan=i.split(' ')
        if fan:
            self.result['fan']=fan[-1]
        else:
            self.result['fan']='unknown'
        return self.result

    def getpower(self):
        ps=list()
        p=re.compile('POWER|Built-in')
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

class C2950Parse(C35xxParse):
    def getmem(self):
        mem=list()
        p=re.compile('^Total')
        for i in self.rawdata:
            m=p.search(i)
            if m:
                i=' '.join(i.split())
                mem=i.split(' ')
        if mem:
            memusage=int(mem[3].strip(','))*100/int(mem[1].strip(','))
            self.result['mem util']=str(int(memusage))+'%'
        else:
            self.result['mem util']='unknown'
        return self.result

    def gettemp(self):
        self.result['temperature']='NotSupport'
        return self.result

# below is just for test...
if __name__=='__main__':
    f=open('raw.txt', 'r')
    s=f.read()
    f.close
    raw=s.split('\n')

    switch=C35xxParse(raw)
    result=switch.saveresult()
    print(result)
    switch=C2950Parse(raw)
    result=switch.saveresult()
    print(result)
