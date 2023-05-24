# Começo do sistema simples sem comentários apenas o sistema puro.

import os;os.system('cls')
import time
import datetime
import random

def db(user, data='', create=False, read=False, read_choose="data", update=False, update_content=False, update_category=False, delete=False):

    # Formatação do banco de dados
    # tipo, valor, alteração, dia, mês, ano, código
    try:
        if create and not read and not update and not delete:
            with open(f'./database/financas-{user}.csv', 'a') as file:
                file.write(f'{data}\n')
                return "Done!"
            
        elif read and not create and not update and not delete:
            with open(f'./database/financas-{user}.csv', 'r') as file:
                linhas_tratadas=[]
                for i in file.readlines():
                    linhas_tratadas.append(i.replace('\n', '').split(','))
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

            with open(f'./database/financas-{user}.csv', 'r') as file:
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

            with open(f'./database/financas-{user}.csv', 'w') as file:
                file.write(''.join(banco_salvo))

            return 'Updated'
        
        elif delete and not read and not update and not create:
            banco_salvo=[]

            with open(f'./database/financas-{user}.csv', 'r+') as file:
                lines=file.readlines()

                for i in lines:
                    if not data in i.strip():
                        banco_salvo.append(i)
                        
            with open(f'./database/financas-{user}.csv', 'w') as file:
                file.write(''.join(banco_salvo))
                
            return "Deleted!"
        else:
            return "[ERROR] (00) Não foi definido uma ação para realizar com a informação passada!"
    except FileExistsError as e:
        with open(f'./database/financas-{user}.csv', 'w') as file:
            file.write('')
        return e
    except:
        return "[ERROR] (01) Não definido!"

def banner(texto, subtitulo=''):
    linha=f"+ {len(texto)*'=' if len(texto) > len(subtitulo) else len(subtitulo)*'='} +"

    print(linha)

    if subtitulo != '':
        print(f"| {texto}{(len(subtitulo)-len(texto))*' ' if len(subtitulo) > len(texto) else ''} |")
        print(f"| {subtitulo}{(len(texto)-len(subtitulo))*' ' if len(texto) > len(subtitulo) else ''} |")
    else:
        print(f"| {texto} |")
    
    print(linha)

def moldura(texto):
    linhas=texto.split('\n')
    maior_linha=''
    for linha_tamanho in linhas:
        if len(linha_tamanho) > len(maior_linha):
            maior_linha=linha_tamanho

    print(f'+ {"="*len(maior_linha)} +')
    for linha in linhas:
        print(f'| {linha}{" "*(len(maior_linha)-len(linha))} |')
    print(f'+ {"="*len(maior_linha)} +')

def balanco(user):
    db(user)

def id(numeros=5):
    letras=list("abcdefghijklmnopqrstuvwxyz")
    token=[]

    for numero in range(numeros):
        metade = random.randint(0, 1)
        caps = random.randint(0, 1)
        if metade:
           token.append(str(random.randint(0, 9)))
        else:
            if caps:
                token.append(random.choice(letras).upper())
            else:
                token.append(random.choice(letras))   	
    return ''.join(token)


def console(user):
    os.system('cls')
    usr=None
    with open('ares.key', 'r') as file:
        for usuario in file.readlines():
            if user in usuario:
                usr=usuario.strip().split(";")

    opcoes='[1] - Ver extrato  [2] - Adicionar movimentação  [3] - Limpar  [4] - Sair'

    banner(f"Menu {' '*(len(opcoes) - (len(f'Conta: [{usr[1]}]')+len('Menu ')))}Conta: [{usr[1]}] Saldo: []", opcoes)

    while True:
        try:
            resposta=input('> Digite uma opção: ')
            while resposta not in ['1', '2', '3', '4']:
                print('>> Opção inválida, por gentileza digite novamente!')
                resposta=input('> Digite uma opção: ')
            
            if resposta=="1":
                os.system('cls')
                moldura('Categoria | Nome | Valor | Data e hora | Movimentação | ID\nComandos disponíveis: remover [id], editar [id] ou sair') 

                despesas=db(user, read=True)

                print()

                if len(despesas) == 0:
                    print('>> Nada por aqui...')
                else:
                    for item in despesas:
                        print(f'{item[6]}\t|\t{item[5]}\t|\t{item[0]}\t|\t{item[1]}/{item[2]}/{item[3]} às {item[4]}\t|\t{item[7]} [{item[8]}]')

                while True:
                    try:
                        resposta=input('\n> ').strip().split(' ')
                        resposta_parametro1 = resposta[0]
                        while resposta_parametro1 != "remover" and resposta_parametro1 != "editar":
                            print('>> Comando não encontrado!')
                            resposta=input('\n> ').strip().split(' ')
                            resposta_parametro1 = resposta[0]
                        resposta_parametro2 = resposta[1]
                    except:
                        print('>> Por gentileza, use o seguinte formato de comando: remover [ID] (Sem os colchetes)')
                    else:
                        break

                while resposta_parametro1 != 'remover' and resposta_parametro1 != 'editar' and not len(resposta_parametro2) == 5:
                    while True:
                        try:
                            resposta=input('\n> ').strip().split(' ')
                            resposta_parametro1 = resposta[0]
                            resposta_parametro2 = resposta[1]
                        except:
                            print('>> Por gentileza, use o seguinte formato de comando: remover [ID] (Sem os colchetes)')
                        else:
                            break

                if resposta_parametro1 == "remover":
                    db(user, resposta_parametro2, delete=True)
                    print('>> Deletando!')
                    time.sleep(1)
                    print('>> Deletado!')
                    time.sleep(1)
                else:
                    print('Editando!')

                
                console(user)

            elif resposta=="2":
                os.system('cls')
                moldura('Aqui você poderá adicionar suas movimentações!\nPara começar, digite se sua movimentação é uma "entrada" ou "saída".\nUse "/sair" para voltar para o menu')
                resposta=input('> Digite se sua movimentação é uma "entrada" ou "saída": ').strip().lower().replace('í','i')
                while resposta != "entrada" and resposta != "saida" and resposta != "sair":
                    print('>> Opção não encontrada')
                    resposta=input('> Digite se sua movimentação é uma "entrada" ou "saída": ').strip().lower().replace('í','i')

                if resposta == "sair":
                    print('Ok! Voltando para o menu...')
                    time.sleep(1)
                    console(user)
                elif resposta == "entrada":
                    confirmar='n'

                    while confirmar != 's':
                        os.system('cls')
                        moldura('Adicionando uma nova entrada!\nSiga os passos a seguir para adicionar a sua entrada.')

                        nome_despesa=input('> Digite o nome da sua entrada (Ex.: Gasolina): ')
                        valor_despesa=input('> Digite o valor da sua entrada (Ex.: 200,00): ').replace(',', '.').strip()
                        
                        valor_erro=1

                        while valor_erro != 0:
                            try:
                                valor_despesa=str(float(valor_despesa))
                            except:
                                continue
                            else:
                                valor_erro=0
                            
                        categoria_despesa=input('> Digite a categoria de sua entrada (Ex.: Lazer): ')
                        data_atual=datetime.datetime.now()
                        pergunta_um=input(f'> Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa entrada? [S ou N] ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            pergunta_um=input(f'Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa entrada? [S ou N] ')
                        if pergunta_um == 's':
                            dia_despesa=data_atual.day
                            mes_despesa=data_atual.month
                            ano_despesa=data_atual.year
                            hora_despesa=data_atual.hour
                            minuto_despesa=data_atual.minute
                        else:
                            dia_despesa=input('> Informe o dia da sua entrada (Ex.: 20): ')
                            mes_despesa=input('> Informe o mês da sua entrada (Ex.: 2): ')
                            ano_despesa=input('> Informe o ano da sua entrada (Ex.: 2023): ')
                            hora_despesa=input('> Informe a hora da sua entrada (Ex.: 23): ')
                            minuto_despesa=input('> Informe o minuto da sua entrada (Ex.: 46): ')

                        despesa=[str(valor_despesa), str(dia_despesa), str(mes_despesa), str(ano_despesa), f'{hora_despesa}:{minuto_despesa}', str(nome_despesa), str(categoria_despesa), str('entrada'), str(id())]
                        
                        os.system('cls')
                        moldura('Adicionando uma nova entrada!\nSiga os passos a seguir para adicionar a sua entrada.')
                        
                        print('Categoria\t|\tNome\t|\tValor\t|\tData e hora')
                        print(f'{despesa[6]}\t|\t{despesa[5]}\t|\t{despesa[0]}\t|\t{despesa[1]}/{despesa[2]}/{despesa[3]} às {despesa[4]}')
            
                        confirmar=input('Você deseja cofirmar a sua entrada? [S e N] ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            confirmar=input('Você deseja cofirmar a sua entrada? [S e N] ').lower().strip()
                        if confirmar == 's':
                            print('>> Salvando sua entrada...')
                            time.sleep(1)

                            despesa=','.join(despesa)
                            db(user, create=True, data=despesa)
                            print('>> Despesa salva!')
                            time.sleep(1)
                        else:
                            print('>> Voltando para o menu...')
                            time.sleep(1)
                    console(user)
                else:
                    confirmar='n'

                    while confirmar != 's':
                        os.system('cls')
                        moldura('Adicionando uma nova despesa!\nSiga os passos a seguir para adicionar a sua despesa.')

                        nome_despesa=input('> Digite o nome da sua despesa (Ex.: Gasolina): ')
                        valor_despesa=input('> Digite o valor da sua despesa (Ex.: 200,00): ').replace(',', '.').strip()
                        
                        valor_erro=1

                        while valor_erro != 0:
                            try:
                                valor_despesa=str(float(valor_despesa))
                            except:
                                continue
                            else:
                                valor_erro=0
                            
                        categoria_despesa=input('> Digite a categoria de sua despesa (Ex.: Lazer): ')
                        data_atual=datetime.datetime.now()
                        pergunta_um=input(f'> Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa despesa? [S ou N] ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            pergunta_um=input(f'Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa despesa? [S ou N] ')
                        if pergunta_um == 's':
                            dia_despesa=data_atual.day
                            mes_despesa=data_atual.month
                            ano_despesa=data_atual.year
                            hora_despesa=data_atual.hour
                            minuto_despesa=data_atual.minute
                        else:
                            dia_despesa=input('> Informe o dia da sua despesa (Ex.: 20): ')
                            mes_despesa=input('> Informe o mês da sua despesa (Ex.: 2): ')
                            ano_despesa=input('> Informe o ano da sua despesa (Ex.: 2023): ')
                            hora_despesa=input('> Informe a hora da sua despesa (Ex.: 23): ')
                            minuto_despesa=input('> Informe o minuto da sua despesa (Ex.: 46): ')

                        despesa=[str(valor_despesa), str(dia_despesa), str(mes_despesa), str(ano_despesa), f'{hora_despesa}:{minuto_despesa}', str(nome_despesa), str(categoria_despesa), str('saida'), str(id())]
                        
                        os.system('cls')
                        moldura('Adicionando uma nova despesa!\nSiga os passos a seguir para adicionar a sua despesa.')
                        
                        print('Categoria\t|\tNome\t|\tValor\t|\tData e hora')
                        print(f'{despesa[6]}\t|\t{despesa[5]}\t|\t{despesa[0]}\t|\t{despesa[1]}/{despesa[2]}/{despesa[3]} às {despesa[4]}')
            
                        confirmar=input('Você deseja cofirmar a sua despesa? [S e N] ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            confirmar=input('Você deseja cofirmar a sua despesa? [S e N] ').lower().strip()
                        if confirmar == 's':
                            print('>> Salvando sua despesa...')
                            time.sleep(1)

                            despesa=','.join(despesa)
                            db(user, create=True, data=despesa)
                            print('>> Despesa salva!')
                            time.sleep(1)
                        else:
                            print('>> Voltando para o menu...')
                            time.sleep(1)
                    console(user)

            elif resposta == "4":
                console(user)
            elif resposta == "5":
                print('>> Uma pena você ir, até mais!')
                time.sleep(1)
                exit()
        except KeyboardInterrupt:
            os.system('cls')
            resposta=input('> Você realmente deseja sair do programa? [S ou N] ').lower().strip()
            while resposta != 's' and resposta != 'n':
                print('>> Opção não encontrada!')
                resposta=input('> Você realmente deseja sair do programa? [S ou N] ')
            if resposta=='s':
                print('>> Uma pena você ir, até mais!')
                time.sleep(1)
                exit()
            else:
                print('>> Excelente, voltando...')
                time.sleep(1)
                console(user)
        
def login():
    try:
        os.system('cls')
        with open('./ares.config', "r+") as config:
            with open('./ares.key', "r+") as key_file:
                ultimo_acesso_cpf=config.readline().replace('ultima_sessao=', '')
                ultimo_acesso_nome=None
                pin = None
                usuarios = key_file.readlines()
                senha=None

                for usuario in usuarios:
                    if ultimo_acesso_cpf in usuario:
                        senha=usuario.strip().split(';')[4]
                        ultimo_acesso_nome=usuario.strip().split(';')[1]

                tentativas = 3

                banner('Olá, seja bem-vindo(a) ao banco Ares!')

                print(f"> A última sessão encontrada foi de {ultimo_acesso_nome}!")

                res = int(input('> Você deseja continuar [0] ou realizar um novo login [1]? '))

                while res != 1 and res != 0:
                    print('> Opção não encontrada, por gentileza digite novamente.')

                    res = int(input('> Você deseja continuar [0] ou realizar um novo login [1]? '))

                if res == 0:
                    while pin != senha:
                        pin = input('> Digite o seu pin: ')
                        
                        if pin == senha:
                            console(ultimo_acesso_cpf)
                        else:
                            tentativas-=1

                            if tentativas < 1:
                                print(f'> Você acabou com suas tentativas, encerrando aplicativo.')
                                exit()
                            else:
                                print(f'> PIN inválido! Mais {tentativas} tentativas!')
                else:
                    os.system('cls')

                    banner('Ok, vamos entrar em uma nova conta! ')

                    res = int(input('> Você deseja realizar um novo login [0] ou criar uma nova conta [1]?'))

                    while res != 1 and res != 0:
                        print('> Opção não encontrada, por gentileza digite novamente.')

                        res = int(input('> Você deseja realizar um novo login [0] ou criar uma nova conta [1]?'))
                        
                    if res == 1:
                        os.system('cls')
                        banner('Vamos criar uma nova conta!')

                        acc_nome=input('> Digite o seu primeiro nome (Ex.: Carlos): ')
                        acc_sobrenome=input('> Digite o seu sobrenome (Ex.: Souza): ')
                        acc_nascimento=input('> Digite o ano do seu nascimento (Ex.: 2000): ')
                        acc_cpf=input('> Digite o seu CPF (Ex.: 12345678910): ').replace('.','')
                        acc_senha=input('> Crie sua senha (Ex.: 12345): ')

                        key_file.write(f"\n{acc_cpf};{acc_nome};{acc_sobrenome};{acc_nascimento};{acc_senha}")

                        with open(f'./database/financas-{acc_cpf}.csv', 'w') as file:
                            file.write('')
                        
                        key_file.close()
                        config.close()

                        with open('./ares.config', 'w') as configv2:
                            configv2.write("ultima_sessao="+acc_cpf)
                        
                        print('>> Sua conta está sendo criada...')
                        
                        time.sleep(1)
                        print('>> Sua conta foi criada com sucesso!')
                        time.sleep(1)
                        print('>> Entrando...')
                        time.sleep(1)
                        console(acc_cpf)

                    if res == 0:
                        os.system('cls')

                        banner('Vamos fazer login em uma nova conta!')

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
                                    console(acc_cpf)
                                else:
                                    tentativas-=1

                                    if tentativas < 1:
                                        print(f'> Você acabou com suas tentativas, encerrando aplicativo.')
                                        exit()
                                    else:
                                        print(f'> PIN inválido! Mais {tentativas} tentativas!')
    except KeyboardInterrupt:
        os.system('cls')
        resposta=input('> Você realmente deseja sair do programa? [S ou N] ').lower().strip()
        while resposta != 's' and resposta != 'n':
            print('>> Opção não encontrada!')
            resposta=input('> Você realmente deseja sair do programa? [S ou N] ')
        if resposta=='s':
            print('>> Uma pena você ir, até mais!')
            time.sleep(1)
            exit()
        else:
            print('>> Excelente, voltando...')
            time.sleep(1)
            login()

login()