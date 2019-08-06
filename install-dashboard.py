# Import modules
import wget
import subprocess
import fileinput

## Welcome Message
print("##### Welcome to the TJTH Kubernetes Dashboard installer #####")

## Get Dashboard IP/Hostname
masterIp=raw_input("Please enter your K8s Master IP or Hostname: ")

## Download Kubernetes Dashboard file
dashYaml="/tmp/kubernetes-dashboard.yaml"
dashYamlURL="https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml"
downloadDash= wget.download(dashYamlURL, dashYaml)
print("\nDownloading Kubernetes Dashboard Yaml File..")
downloadDash

## Set NodePort
print("\nSetting Service to NodePort..")
f=open(dashYaml,"a")
f.write("  type: NodePort")
f.close()

## Create Dashboard in Kubernetes
def createFromYaml(yamlFile):
    print("\nDeploying: "+yamlFile)
    subprocess.call(["kubectl","apply","-f",yamlFile])
    print("\nDeployed..")
createFromYaml(dashYaml)

## Get Dashbaord Token
def getToken():
    print("\nGetting Token from Kube System..")
    getTokenCmd="kubectl -n kube-system describe secrets $(kubectl -n kube-system get secret | grep 'dashboard-token' | awk {'print $1'}) | grep 'token:' | awk {'print $2'}"
    getToken= subprocess.Popen(getTokenCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    tokenName= getToken.communicate()[0]
    return tokenName.rstrip()
token = getToken()

## Get Dashboard Service Port
def getDashPort():
    print("\nGetting Dashboard ServicePort")
    getPortCmd="kubectl get svc -n kube-system | grep 'dash' | awk {'print $5'} | grep -o -P '(?<=:).*(?=/)'"
    getPort= subprocess.Popen(getPortCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    svcPort= getPort.communicate()[0]
    return svcPort
masterPort = getDashPort()

## Set Dashboard user as Admin
def makeAdmin():
    print("\nMaking Dashboard User a K8s Admin")
    makeAdminCmd="kubectl create clusterrolebinding kubernetes-dashboard --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard"
    makeAdmin=subprocess.Popen(makeAdminCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    confAdmin=makeAdmin.communicate()[0]
makeAdmin()

## Update docker-compose with Token
nginxConf="config/nginx.conf"
def updateNginxConf():
    print("Updating Nginx Config with Token Env Variable and K8s Master Address..")
    for line in fileinput.input(nginxConf,inplace=True):
        print line.replace("CHANGETOKEN",token),
    for line in fileinput.input(nginxConf,inplace=True):
        print line.replace("CHANGEIP",masterIp),
    for line in fileinput.input(nginxConf,inplace=True):
        print line.replace("CHANGEPORT",masterPort),
updateNginxConf()

print("##### Task Complete! #####")