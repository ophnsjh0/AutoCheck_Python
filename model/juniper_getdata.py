import telnetlib
import paramiko

class Juniper:
    def __init__(self, switch):
        print(switch)
        self.switch = switch
        self.rawdata = list()
        self.cmd = ['set cli screen-length 0 ', 'show chassis routing-engine',
                     'show chassis environment','show configuration | match host-name', 'exit']

    def get_telnet(self):
        ip = self.switch[0]
        port = self.switch[1]
        uid = self.switch[2]
        password = self.switch[3]
        protocol = self.switch[4]
        vendor = self.switch[5]
        cmd = str()
        for i in self.cmd:
            cmd += i+'\n'
            print(i)

        if vendor != 'juniper' or protocol != 'telnet':
            print('Not suppported switch %s or protocol %s' %
                  (vendor, protocol))
            exit
        data = 'ipaddr: '+ip+'\n'
        try:
            tn = telnetlib.Telnet(ip, port, 20)
            # tn.set_debuglevel(1)
            tn.read_until('Username: '.encode('ascii'))
            tn.write(uid.encode('ascii')+b'\n')
            tn.read_until('Password: '.encode('ascii'))
            tn.write(password.encode('ascii')+b'\n')
            tn.write(cmd.encode('ascii')+b'\n')
            data += tn.read_all().decode('ascii')
            tn.close()
        except Exception as ex:
            print('Something is wrong...\n', ex)
            data += 'error'
        f = open(ip + '.txt', 'w')
        f.write(data)
        f.close()
        self.rawdata = data.split('\n')
        return self.rawdata

    def get_ssh(self):
        ip = self.switch[0]
        ports = self.switch[1]
        uid = self.switch[2]
        passwd = self.switch[3]
        proto = self.switch[4].strip()
        vendor = self.switch[5].strip()
        data = str()
        data += 'ipaddr: '+ip+'\n'
        if proto != 'ssh' or vendor != 'juniper':
            print('Not supported switch %s or vendor %s' % (vendor, proto))
            exit()

        for i in self.cmd:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip, port=ports,
                            username=uid, password=passwd)
                stdin, stdout, stderr = ssh.exec_command(i.encode('ascii'))
                # stdin, stdout, stderr = ssh.exec_command(i.encode('cp949', 'ignore'))
                #data+=((stdin.read()).decode('ascii')).replace('\r\n', '\n')
                data += ((stdout.read()).decode('ascii')).replace('\r\n', '\n')
                # data += ((stdout.read()).decode('cp949', 'ignore')).replace('\r\n', '\n')
            except Exception as ex:
                print('Something is wrong...\n', ex)
                data += 'error'
        f = open(ip + '.txt', 'w')
        f.write(data)
        f.close()
        self.rawdata = data.split('\n')
        return self.rawdata

    def get_tacacs(self):
        ip = self.switch[0]
        ports = self.switch[1]
        uid = self.switch[2]
        passwd = self.switch[3]
        proto = self.switch[4].strip()
        vendor = self.switch[5].strip()
        data = str()
        data += 'ipaddr: '+ip+'\n'
        if proto != 'tacacs' or vendor != 'juniper':
            print('Not supported switch %s or vendor %s' % (vendor, proto))
            exit()

        for i in self.cmd:
            try:
                # print(i)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip, port=ports,
                            username=uid, password=passwd)
                # stdin, stdout, stderr = ssh.exec_command(i.encode('ascii'))
                stdin, stdout, stderr = ssh.exec_command(i.encode('cp949', 'ignore'))
                #data+=((stdin.read()).decode('ascii')).replace('\r\n', '\n')
                # data += ((stdout.read()).decode('ascii')).replace('\r\n', '\n')
                data += ((stdout.read()).decode('cp949', 'ignore')).replace('\r\n', '\n')
            except Exception as ex:
                print('Something is wrong...\n', ex)
                data += 'error'
        f = open(ip + '.txt', 'w')
        f.write(data)
        f.close()
        self.rawdata = data.split('\n')
        return self.rawdata


# below is just for test...
if __name__ == '__main__':
    f = open('switch.txt', 'r')
    s = f.read()
    f.close()
    sw = s.split('\n')
    for i in sw:
        switch = i.split('\t')
        protocol = switch[4]
        data = C35xxGetRawData(switch)
        if protocol == 'ssh':
            rawdata = data.get_ssh()
        elif protocol == 'telnet':
            rawdata = data.get_telnet()
        else:
            print('Not supported!!!\n')
        print(i)
        print(rawdata)
