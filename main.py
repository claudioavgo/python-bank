# Começo do sistema simples sem comentários apenas o sistema puro.

import os;os.system('cls')
import time
import datetime
import random
import requests

def send_file(user):
    usr=0
    with open('ares.key', 'r') as file:
        for i in file:
            if user in i:
                usr=i.split(';')

    files = {
    'file': (f'./database/financas-{user}.csv', open(f'./database/financas-{user}.csv', 'rb')),
    }
    
    payload = {
        'content': f"# Olá {usr[1]}! Aqui está suas últimas movimentações!" 
    }

    r = requests.post("https://discord.com/api/webhooks/1111288672688553994/YXfGyHlnB43IFZuk9C3EGdr1ahAiMjYw6cJbhsGqnxGdj0MCPbAa38buGMksdYZJ4Raf", data=payload, files=files)

class bcolors:
    green = '\033[92m' #GREEN
    RESET = '\033[0m' #RESET COLOR
    negrito = '\033[1m' #Negrito

def db(user, data='', create=False, create_write=False, read=False, read_choose="data", update=False, update_content=False, delete=False):

    # Formatação do banco de dados
    # tipo, valor, alteração, dia, mês, ano, código
    try:
        if create and not read and not update and not delete:
            if create_write:
                with open(f'./database/financas-{user}.csv', 'w') as file:
                    file.write(f'')
                    file.close()
                with open(f'./database/financas-{user}.csv', 'a') as fila_append:
                    for i in data:
                        fila_append.write(f'{i}\n')
                    fila_append.close()
                return 'Ok!'
            else:
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
            file.close()

        elif update and data and update_content and not read and not create and not delete:
            banco_salvo=[]

            cont = db(user, read=True)

            for item in cont:
                if data in item:
                    banco_salvo.append(update_content)
                else:
                    banco_salvo.append(','.join(item))
            
            db(user, create=True, create_write=True, data=banco_salvo)

            return 'Updated'
        
        elif delete and not read and not update and not create:
            banco_salvo=[]

            with open(f'./database/financas-{user}.csv', 'r+') as file:
                lines=file.readlines()

                for i in lines:
                    if not data in i.strip():
                        banco_salvo.append(i)
            file.close()
                        
            with open(f'./database/financas-{user}.csv', 'w') as file:
                file.write(''.join(banco_salvo))
            file.close()
                
            return "Deleted!"
        else:
            return "[ERROR] (00) Não foi definido uma ação para realizar com a informação passada!"
    except FileExistsError as e:
        with open(f'./database/financas-{user}.csv', 'w') as file:
            file.write('')
        return e

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
    data = db(user, read=True)
    total=0
    if data:
        for i in data:
            if i[7] == "saida":
                total-=float(i[0])
            else:
                total+=float(i[0])
    
    return total


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

    saldo = balanco(user)

    with open('./ares.key', 'r') as usuarios:
        for userx in usuarios:
            if user in userx:
                usr=userx.split(';')

    opcoes= f'[{bcolors.green}1{bcolors.RESET}] - Ver extrato  [{bcolors.green}2{bcolors.RESET}] - Adicionar movimentação  [{bcolors.green}3{bcolors.RESET}] - Limpar  [{bcolors.green}4{bcolors.RESET}] - Sair'
    menu=f"Menu - Conta: [{usr[1]}] - Saldo: [{saldo}]"
    banner(f"Menu - Conta: [{usr[1]}] - Saldo: [{saldo}]{' '*(len(opcoes)-len(menu))}", opcoes)

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

                        if resposta_parametro1 == "sair":
                            print('>> Ok, voltando para o menu...')
                            time.sleep(1)
                            console(user)
                        
                        while resposta_parametro1 != "remover" and resposta_parametro1 != "editar" and resposta_parametro1 != "sair":
                            print('>> Comando não encontrado!')
                            resposta=input('\n> ').strip().split(' ')
                            resposta_parametro1 = resposta[0]
                        resposta_parametro2 = resposta[1]
                    except:
                        print('>> Por gentileza, use o seguinte formato de comando: remover [ID] (Sem os colchetes)')
                    else:
                        break

                while resposta_parametro1 != 'remover' and resposta_parametro1 != "editar" and resposta_parametro1 != "sair" and not len(resposta_parametro2) == 5:
                    if resposta_parametro1 == "sair":
                        print('>> Ok, voltando para o menu...')
                        time.sleep(1)
                        console(user)
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
                    info = db(user, read=True)
                    tem=False
                    transacao=0
                    for i in info:
                        if resposta_parametro2 in i:
                            tem=True
                            transacao=i
                    
                    if tem:
                        os.system('cls')
                        moldura(f'Alterando o item de ID: {resposta_parametro2}!\n{transacao}')
                        print()
                        entrada_despesa=input(f'Digite se alteração irá ser uma [saída ou entrada]: ').replace('í', 'i')

                        nome_despesa=input(f'> Digite o nome da sua alteracão {bcolors.negrito}(Ex.: Gasolina){bcolors.RESET}: ')
                        valor_despesa=input(f'> Digite o valor da sua alteracão {bcolors.negrito}(Ex.: 200,00){bcolors.RESET}: ').replace(',', '.').strip()
                        
                        valor_erro=1

                        while valor_erro != 0:
                            try:
                                valor_despesa=str(float(valor_despesa))
                            except:
                                continue
                            else:
                                valor_erro=0
                            
                        categoria_despesa=input(f'> Digite a nova categoria {bcolors.negrito}(Ex.: Lazer){bcolors.RESET}: ')
                        data_atual=datetime.datetime.now()
                        pergunta_um=input(f'> Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa alteracão? {bcolors.negrito}[S ou N]{bcolors.RESET} ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            pergunta_um=input(f'Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa alteracão? {bcolors.negrito}[S ou N]{bcolors.RESET} ')
                        if pergunta_um == 's':
                            dia_despesa=data_atual.day
                            mes_despesa=data_atual.month
                            ano_despesa=data_atual.year
                            hora_despesa=data_atual.hour
                            minuto_despesa=data_atual.minute
                        else:
                            dia_despesa=input(f'> Informe o dia da sua alteracão {bcolors.negrito}(Ex.: 20){bcolors.RESET}: ')
                            mes_despesa=input(f'> Informe o mês da sua alteracão {bcolors.negrito}(Ex.: 2){bcolors.RESET}: ')
                            ano_despesa=input(f'> Informe o ano da sua alteracão {bcolors.negrito}(Ex.: 2023){bcolors.RESET}: ')
                            hora_despesa=input(f'> Informe a hora da sua alteracão {bcolors.negrito}(Ex.: 23){bcolors.RESET}: ')
                            minuto_despesa=input(f'> Informe o minuto da sua alteracão {bcolors.negrito}(Ex.: 46){bcolors.RESET}: ')

                        despesa=f'{str(valor_despesa)},{str(dia_despesa)},{str(mes_despesa)},{str(ano_despesa)},{f"{hora_despesa}:{minuto_despesa}"},{str(nome_despesa)},{str(categoria_despesa)},{str(entrada_despesa)},{str(resposta_parametro2)}'

                        db(user, data=resposta_parametro2, update=True, update_content=despesa)
                        print()
                        print('>> Alteração feita com sucesso!')
                        time.sleep(1)
                        console(user)

                    else:
                        print('>> Item não encontrado! Voltando para o menu...')
                        time.sleep(1)
                        console(user)

                
                console(user)

            elif resposta=="2":
                os.system('cls')
                moldura(f'Aqui você poderá adicionar suas movimentações!\nPara começar, digite se sua movimentação é uma {bcolors.green}"entrada"{bcolors.RESET} ou {bcolors.green}"saída"{bcolors.RESET}.\nUse {bcolors.green}"sair"{bcolors.RESET} para voltar para o menu')
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

                        nome_despesa=input(f'> Digite o nome da sua entrada {bcolors.negrito}(Ex.: Gasolina){bcolors.RESET}: ')
                        valor_despesa=input(f'> Digite o valor da sua entrada {bcolors.negrito}(Ex.: 200,00){bcolors.RESET}: ').replace(',', '.').strip()
                        
                        valor_erro=1

                        while valor_erro != 0:
                            try:
                                valor_despesa=str(float(valor_despesa))
                            except:
                                continue
                            else:
                                valor_erro=0
                            
                        categoria_despesa=input(f'> Digite a categoria de sua entrada {bcolors.negrito}(Ex.: Lazer){bcolors.RESET}: ')
                        data_atual=datetime.datetime.now()
                        pergunta_um=input(f'> Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa entrada? {bcolors.negrito}[S ou N]{bcolors.RESET} ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            pergunta_um=input(f'Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa entrada? {bcolors.negrito}[S ou N]{bcolors.RESET} ')
                        if pergunta_um == 's':
                            dia_despesa=data_atual.day
                            mes_despesa=data_atual.month
                            ano_despesa=data_atual.year
                            hora_despesa=data_atual.hour
                            minuto_despesa=data_atual.minute
                        else:
                            dia_despesa=input(f'> Informe o dia da sua entrada {bcolors.negrito}(Ex.: 20){bcolors.RESET}: ')
                            mes_despesa=input(f'> Informe o mês da sua entrada {bcolors.negrito}(Ex.: 2){bcolors.RESET}: ')
                            ano_despesa=input(f'> Informe o ano da sua entrada {bcolors.negrito}(Ex.: 2023){bcolors.RESET}: ')
                            hora_despesa=input(f'> Informe a hora da sua entrada {bcolors.negrito}(Ex.: 23){bcolors.RESET}: ')
                            minuto_despesa=input(f'> Informe o minuto da sua entrada {bcolors.negrito}(Ex.: 46){bcolors.RESET}: ')

                        despesa=[str(valor_despesa), str(dia_despesa), str(mes_despesa), str(ano_despesa), f'{hora_despesa}:{minuto_despesa}', str(nome_despesa), str(categoria_despesa), str('entrada'), str(id())]
                        
                        os.system('cls')
                        moldura('Adicionando uma nova entrada!\nSiga os passos a seguir para adicionar a sua entrada.')
                        
                        print('Categoria\t|\tNome\t|\tValor\t|\tData e hora')
                        print(f'{despesa[6]}\t|\t{despesa[5]}\t|\t{despesa[0]}\t|\t{despesa[1]}/{despesa[2]}/{despesa[3]} às {despesa[4]}')
            
                        confirmar=input(f'Você deseja cofirmar a sua entrada? {bcolors.negrito}[S e N]{bcolors.RESET} ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            confirmar=input(f'Você deseja cofirmar a sua entrada? {bcolors.negrito}[S e N]{bcolors.RESET} ').lower().strip()
                        if confirmar == 's':
                            print('>> Salvando sua entrada...')
                            time.sleep(1)
                            send_file(user)
                            print('>> A nova atualização das suas movimentações foram enviados para o seu discord!')
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

                        nome_despesa=input(f'> Digite o nome da sua despesa {bcolors.negrito}(Ex.: Gasolina){bcolors.RESET}: ')
                        valor_despesa=input(f'> Digite o valor da sua despesa {bcolors.negrito}(Ex.: 200,00){bcolors.RESET}: ').replace(',', '.').strip()
                        
                        valor_erro=1

                        while valor_erro != 0:
                            try:
                                valor_despesa=str(float(valor_despesa))
                            except:
                                continue
                            else:
                                valor_erro=0
                            
                        categoria_despesa=input(f'> Digite a categoria de sua despesa {bcolors.negrito}(Ex.: Lazer){bcolors.RESET}: ')
                        data_atual=datetime.datetime.now()
                        pergunta_um=input(f'> Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa despesa? {bcolors.negrito}[S ou N]{bcolors.RESET} ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            pergunta_um=input(f'Você deseja atribuir a data atual ({data_atual.day}/{data_atual.month}/{data_atual.year} às {data_atual.hour}:{data_atual.minute}) a essa despesa? {bcolors.negrito}[S ou N]{bcolors.RESET} ')
                        if pergunta_um == 's':
                            dia_despesa=data_atual.day
                            mes_despesa=data_atual.month
                            ano_despesa=data_atual.year
                            hora_despesa=data_atual.hour
                            minuto_despesa=data_atual.minute
                        else:
                            dia_despesa=input(f'> Informe o dia da sua despesa {bcolors.negrito}(Ex.: 20){bcolors.RESET}: ')
                            mes_despesa=input(f'> Informe o mês da sua despesa {bcolors.negrito}(Ex.: 2){bcolors.RESET}: ')
                            ano_despesa=input(f'> Informe o ano da sua despesa {bcolors.negrito}(Ex.: 2023){bcolors.RESET}: ')
                            hora_despesa=input(f'> Informe a hora da sua despesa {bcolors.negrito}(Ex.: 23){bcolors.RESET}: ')
                            minuto_despesa=input(f'> Informe o minuto da sua despesa {bcolors.negrito}(Ex.: 46){bcolors.RESET}: ')

                        despesa=[str(valor_despesa), str(dia_despesa), str(mes_despesa), str(ano_despesa), f'{hora_despesa}:{minuto_despesa}', str(nome_despesa), str(categoria_despesa), str('saida'), str(id())]
                        
                        os.system('cls')
                        moldura('Adicionando uma nova despesa!\nSiga os passos a seguir para adicionar a sua despesa.')
                        
                        print('Categoria\t|\tNome\t|\tValor\t|\tData e hora')
                        print(f'{despesa[6]}\t|\t{despesa[5]}\t|\t{despesa[0]}\t|\t{despesa[1]}/{despesa[2]}/{despesa[3]} às {despesa[4]}')
            
                        confirmar=input(f'Você deseja cofirmar a sua despesa? {bcolors.negrito}[S e N]{bcolors.RESET} ').lower().strip()
                        while pergunta_um != 's' and pergunta_um != 'n':
                            print('>> Opção não encontrada!')
                            confirmar=input(f'Você deseja cofirmar a sua despesa? {bcolors.negrito}[S e N]{bcolors.RESET} ').lower().strip()
                        if confirmar == 's':
                            print('>> Salvando sua despesa...')
                            time.sleep(1)
                            send_file(user)
                            print('>> A nova atualização das suas movimentações foram enviados para o seu discord!')
                            despesa=','.join(despesa)
                            db(user, create=True, data=despesa)
                            time.sleep(1)
                            print('>> Despesa salva!')
                            time.sleep(1)
                        else:
                            print('>> Voltando para o menu...')
                            time.sleep(1)
                    console(user)
        
            elif resposta == "3":
                console(user)
            elif resposta == "4":
                print('>> Uma pena você ir, até mais!')
                time.sleep(1)
                exit()
        except KeyboardInterrupt:
            os.system('cls')
            resposta=input(f'> Você realmente deseja sair do programa? {bcolors.negrito}[S ou N]{bcolors.RESET} ').lower().strip()
            while resposta != 's' and resposta != 'n':
                print('>> Opção não encontrada!')
                resposta=input(f'> Você realmente deseja sair do programa? {bcolors.negrito}[S ou N]{bcolors.RESET} ')
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

                res = int(input(f'> Você deseja continuar [{bcolors.green}0{bcolors.RESET}] ou realizar um novo login [{bcolors.green}1{bcolors.RESET}]? '))

                while res != 1 and res != 0:
                    print('> Opção não encontrada, por gentileza digite novamente.')

                    res = int(input(F'> Você deseja continuar [{bcolors.green}0{bcolors.RESET}] ou realizar um novo login [{bcolors.green}1{bcolors.RESET}]? '))

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
                                print(f'> PIN inválido! Mais {bcolors.green}{tentativas}{bcolors.RESET} tentativas!')
                else:
                    os.system('cls')

                    banner('Ok, vamos entrar em uma nova conta! ')

                    res = int(input(f'> Você deseja realizar um novo login [{bcolors.green}0{bcolors.RESET}] ou criar uma nova conta [{bcolors.green}1{bcolors.RESET}]?'))

                    while res != 1 and res != 0:
                        print('> Opção não encontrada, por gentileza digite novamente.')

                        res = int(input(f'> Você deseja realizar um novo login [{bcolors.green}0{bcolors.RESET}] ou criar uma nova conta [{bcolors.green}1{bcolors.RESET}]?'))
                        
                    if res == 1:
                        os.system('cls')
                        banner('Vamos criar uma nova conta!')

                        acc_nome=input(f'> Digite o seu primeiro nome {bcolors.negrito}(Ex.: Carlos){bcolors.RESET}: ')
                        acc_sobrenome=input(f'> Digite o seu sobrenome {bcolors.negrito}(Ex.: Souza){bcolors.RESET}: ')
                        acc_nascimento=input(f'> Digite o ano do seu nascimento {bcolors.negrito}(Ex.: 2000){bcolors.RESET}: ')
                        acc_cpf=input(f'> Digite o seu CPF {bcolors.negrito}(Ex.: 12345678910){bcolors.RESET}: ').replace('.','')
                        acc_senha=input(f'> Crie sua senha {bcolors.negrito}(Ex.: 12345){bcolors.RESET}: ')
                        acc_saldo = 0

                        key_file.write(f"\n{acc_cpf};{acc_nome};{acc_sobrenome};{acc_nascimento};{acc_senha};{acc_saldo}")

                        with open(f'database/financas-{acc_cpf}.csv', 'w') as file:
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
                                        print(f'> PIN inválido! Mais {bcolors.green}{tentativas}{bcolors.RESET} tentativas!')
    except KeyboardInterrupt:
        os.system('cls')
        resposta=input(f'> Você realmente deseja sair do programa? {bcolors.green}[S ou N]{bcolors.RESET} ').lower().strip()
        while resposta != 's' and resposta != 'n':
            print('>> Opção não encontrada!')
            resposta=input(f'> Você realmente deseja sair do programa? {bcolors.negrito}[S ou N]{bcolors.RESET} ')
        if resposta=='s':
            print('>> Uma pena você ir, até mais!')
            time.sleep(1)
            exit()
        else:
            print('>> Excelente, voltando...')
            time.sleep(1)
            login()

login()