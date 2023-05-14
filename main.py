# Começo do sistema simples sem comentários apenas o sistema puro.

def db(data='', create=False, read=False, update=False, update_content=False, update_category=False, delete=False):

    # Formatação do banco de dados
    # tipo, valor, alteração, dia, mês, ano, código
    try:
        if create and not read and not update and not delete:
            with open('./database/financas.csv', 'a') as file:
                file.write(f'\n{data}')
                return "Done!"
            
        elif read and not create and not update and not delete:
            with open('./database/financas.csv', 'r') as file:
                return file.readlines()
            
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

            with open('./database/financas.csv', 'r') as file:
                lines=file.readlines()

            for i in lines:
                if not data in i:
                    banco_salvo.append(i)
            
            with open('./database/financas.csv', 'w') as file:
                file.write(''.join(banco_salvo))
                    
            return "Deleted!"
        else:
            return "[ERROR] (00) Não foi definido uma ação para realizar com a informação passada!"
    except:
        return "[ERROR] (01) Não definido!"

print(db())

def console(cmd):
    print("""
        
    """)
    if cmd.lower() == "extrato":
        for i in db(data='', read=True):
            data=i.replace('\n', '').split(', ')
            print('|\tCategoria\t|\tValor\t|\tMovimentação\t|\tData')
            print(f'|\t{data[0]}\t\t|\t{data[1]}\t|\t{data[2]}\t\t|\t{data[3]}/{data[4]}/{data[5]}')
    if cmd.lower() == "pesquisar":
        pesquisa=input("Digite o ID único de sua compra: ")
        print(db(data=f'{pesquisa}', read=True))

console(input("Digite seu comando: "))