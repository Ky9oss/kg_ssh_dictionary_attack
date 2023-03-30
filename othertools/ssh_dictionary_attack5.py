#这是一个失败的程序，fabric的Connection中的timeout并不好使，超时后并不会强行中断连接,反观pexpect库，其超时比较好用
from fabric import Connection
import time

# 设置最大重试次数和等待时间
max_retries = 3
timeout = 1

def ssh_connect_with_retry(host, username, password_file):
    # 初始化变量
    
    with open(password_file) as f:
        for password in f:
            retry_count = 0
            success = False

            password = password.strip()
            print(f"尝试使用密码 {password} 连接远程主机...")
            
            while not success and retry_count < max_retries:
                try:
                    # 尝试连接并设置超时时间
                    with Connection(host=host, user=username, connect_kwargs={"password": password}, connect_timeout=timeout) as conn:
                        if conn.is_connected:
                            print('conn.is_connected!')
                            # 连接成功，设置成功标志并退出循环
                            success = True
                    
                except Exception as e:
                    print(f'{e}')
                    print('Timeout')
                    # 超时异常，增加重试计数器
                    retry_count += 1

                time.sleep(timeout)
                    
            if success:
                # 连接成功，执行命令并将结果保存到本地文件中
                result = conn.run('ls -al', hide=True)
                with open("output.txt", "w") as f:
                    f.write(result.stdout)
                break
    
    return conn if success else None

def main():
    host = '127.0.0.1'
    username = 'user1'
    password_file = 'passwords.txt'

    conn = ssh_connect_with_retry(host, username, password_file)
    
    if conn:
        print("成功连接到远程主机！")
    else:
        print("无法连接到远程主机。")

if __name__ == '__main__':
    main()
