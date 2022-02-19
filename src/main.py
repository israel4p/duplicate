#!/usr/bin/env python3
# Script para coletar logins PPPoE repetidos no Huawei
# Desenvolvido por Israel P. da Silva <israel4p@gmail.com>
# License: MIT

import os
import re
import socket
from getpass import getpass

from paramiko import AutoAddPolicy, SSHClient, ssh_exception


def acesso_ssh(username, password, hostname):
    cmd = """display access-user slot 0 | \
            exclude PPPoE | \
            exclude '------' | \
            exclude UserID | \
            exclude IPv6 | \
            exclude users | \
            no-more"""

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    try:
        ssh.connect(
            hostname=hostname, username=username, password=password, timeout=10
        )

    except ssh_exception.AuthenticationException:
        print('Usuário ou senha incorreta.')

    except ssh_exception.NoValidConnectionsError:
        print('Host inacessível')

    except socket.timeout:
        print('Host inacessível')

    else:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        logins = stdout.readlines()

        stdin.close()
        stderr.close()
        ssh.close()

        return logins

    return False


def lista_login_repetidos(data):
    logins = []
    for i in data:
        i = i.strip()

        if not re.match(r'^\s*$', i):
            if '.' not in i[-1] and '>' not in i[-1] and '-' not in i[-1]:
                logins.append(i.split()[1])

    lista_sem_repetidos = set(logins)
    repetidos = [x for x in lista_sem_repetidos if logins.count(x) > 1]

    return repetidos


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')

    print('Entre com os dados do concentrador Huawei\n')
    username = input('\tUsuário: ')
    password = getpass('\tSenha: ')
    hostname = input('\tIP: ')
    print('Aguarde...')

    logins = acesso_ssh(username, password, hostname)

    if logins:
        repetidos = lista_login_repetidos(logins)
        os.system('cls' if os.name == 'nt' else 'clear')
        print('------ Logins Repetidos -----\n')

        for repetido in repetidos:
            print(repetido)
