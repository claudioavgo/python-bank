# Começo do sistema simples sem comentários apenas o sistema puro.

import os;os.system('cls')

def db(data='', create=False, read=False, read_choose="data", update=False, update_content=False, update_category=False, delete=False):

    # Formatação do banco de dados
    # tipo, valor, alteração, dia, mês, ano, código
    try:
        if create and not read and not update and not delete:
            with open('./database/financas.csv', 'a') as file:
                file.write(f'\n{data}')
                return "Done!"
            
        elif read and not create and not update and not delete:
            with open('./database/financas.csv', 'r') as file:
                linhas_tratadas=[]
                for i in file.readlines():
                    linhas_tratadas.append(i.replace('\n', '').split(', '))
                if read_choose == "data":
                    return linhas_tratadas
                elif read_choose[0] == "#":
                    filtro=[]
                    for item in linhas_tratadas:
                        if read_choose in item:
                            filtro.append(item)
                    return filtro

        elif update and update_content and update_category and not read and not create and not delete:
            changer=None
            changer_index=0
            banco_salvo=[]

            with open('./database/financas.csv', 'r') as file:
                lines=file.readlines()

            for index, i in enumerate(lines):
                if data in i:
                    changer=i.split(', ')
                    changer_index=index
                else:
                    banco_salvo.append(i)
                
            if update_category == "tipo":
                changer.pop(0)
                changer.insert(0, update_content)

            banco_salvo.insert(changer_index, ', '.join(changer))

            with open('./database/financas.csv', 'w') as file:
                file.write(''.join(banco_salvo))

            return 'Updated'
        
        elif delete and not read and not update and not create:
            banco_salvo=[]

            with open('./database/financas.csv', 'r+') as file:
                lines=file.readlines()

                for i in lines:
                    if not data in i:
                        banco_salvo.append(i)
                
                file.write(''.join(banco_salvo))
                
            return "Deleted!"
        else:
            return "[ERROR] (00) Não foi definido uma ação para realizar com a informação passada!"
    except:
        return "[ERROR] (01) Não definido!"

def console():
    print("a")

with open('./ares.config', "r+") as config:
    with open('./ares.key', "r+") as key_file:
        ultimo_acesso_cpf=config.readline().replace('ultima_sessao=', '')
        ultimo_acesso_nome=None
        pin = None
        usuarios = key_file.readlines()
        senha=None

        for usuario in usuarios:
            if ultimo_acesso_cpf in usuario:
                senha=usuario.split(';')[4]
                ultimo_acesso_nome=usuario.split(';')[1]

        tentativas = 3

        print("+ ======================================= +")
        print("| Olá, seja bem-vindo(a) ao banco Ares!   |")
        print("+ ======================================= +")
        print(f"> A última sessão encontrada foi de {ultimo_acesso_nome}!")

        res = int(input('> Você deseja continuar [0] ou realizar um novo login [1]? '))
        while res != 1 and res != 0:
            print('> Opção não encontrada, por gentileza digite novamente.')
            res = int(input('> Você deseja continuar [0] ou realizar um novo login [1]? '))
        if res == 0:
            while pin != senha:
                pin = input('> Digite o seu pin: ')
                
                if pin == senha:
                    os.system('cls')
                    console()
                else:
                    tentativas-=1

                    if tentativas < 1:
                        print(f'> Você acabou com suas tentativas, encerrando aplicativo.')
                        exit()
                    else:
                        print(f'> PIN inválido! Mais {tentativas} tentativas!')
        else:
            os.system('cls')
            print("+ ======================================= +")
            print("| Ok, vamos entrar em uma nova conta!     |")
            print("+ ======================================= +")
            res = int(input('> Você deseja realizar um novo login [0] ou criar uma nova conta [1]?'))
            while res != 1 and res != 0:
                print('> Opção não encontrada, por gentileza digite novamente.')
                res = int(input('> Você deseja realizar um novo login [0] ou criar uma nova conta [1]?'))
            if res == 1:
                os.system('cls')
                print("+ ======================================= +")
                print("| Vamos criar uma nova conta!             |")
                print("+ ======================================= +")
                acc_nome=input('> Digite o seu primeiro nome: ')
                acc_sobrenome=input('> Digite o seu sobrenome: ')
                acc_nascimento=input('> Digite o ano do seu nascimento: ')
                acc_cpf=input('> Digite o ano o seu CPF: ')
                acc_senha=input('> Digite a sua senha: ')
                key_file.write(f"\n{acc_cpf};{acc_nome};{acc_sobrenome};{acc_nascimento};{acc_senha}")
                with open('./ares.config', "w") as config:
                    config.write("ultima_sessao="+acc_cpf)
            if res == 0:
                os.system('cls')
                print("+ ======================================= +")
                print("| Vamos fazer login em uma nova conta!    |")
                print("+ ======================================= +")
                acc_cpf=input('> Digite o seu CPF: ')
                for conta in usuarios:
                    if acc_cpf in conta:
                        senha = conta.strip().split(';')[4]
                else:
                    while pin != senha:
                        pin = input('> Digite o seu pin: ')
                        
                        if pin == senha:
                            with open('./ares.config', "w") as config:
                                config.write("ultima_sessao="+acc_cpf)
                            os.system('cls')
                            console()
                        else:
                            tentativas-=1

                            if tentativas < 1:
                                print(f'> Você acabou com suas tentativas, encerrando aplicativo.')
                                exit()
                            else:
                                print(f'> PIN inválido! Mais {tentativas} tentativas!')
