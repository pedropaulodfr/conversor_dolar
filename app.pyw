from time import asctime
from tkinter import *
from functools import partial

import os
import json
import requests

janela_segunda = None
janela_terceira = None

tempo = asctime().split()
dia = int(tempo[2])
ano = int(tempo[4])
rel = tempo[3]  # Hora em formato de string
diasSemana = {'Mon': 'Segunda-feira',
              'Tue': 'Terça-feira',
              'Wed': 'Quarta-feira',
              'Thu': 'Quinta-feira',
              'Fri': 'Sexta-feira',
              'Sat': 'Sábado',
              'Sun': 'Domingo'}
meses = {'Jan': 'Janeiro', 'Feb': 'Fevereiro', 'Mar': 'Março', 'Apr': 'Abril', 'May': 'Maio', 'Jun': 'Junho',
         'Jul': 'Julho', 'Aug': 'Agosto', 'Sep': 'Setembro', 'Oct': 'Outubro', 'Nov': 'Novembro', 'Dec': 'Dezembro'}
mesesNum = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
            'Nov': 11, 'Dec': 12}


def conversor(var):
    moeda = var.get()
    # Gravando valor atual do Radiobutton no cache
    gravaCache = open('value.cache', 'w')
    gravaCache.write(moeda)
    gravaCache.close()

    if(moeda == 'RD'):
        valorMoeda = campo.get()
        if (valorMoeda.isalpha()) != True:
            resultado = (float(valorMoeda) / float(preco))
            texto = ('R$ {} equivale a US$ {:.6}').format(valorMoeda, str(resultado))
            lb['text'] = texto
            lb['bg'] = 'light gray'
            lb['foreground'] = 'black'
        else:
            lb['text'] = 'VALOR INVÁLIDO!'
            lb['foreground'] = 'red'
    if(moeda == 'DR'):
        valorMoeda = campo.get()
        if (valorMoeda.isalpha()) != True:
            resultado = (float(valorMoeda) * float(preco))
            texto = 'US$ {} equivale a R$ {:.6}'.format(valorMoeda, str(resultado))
            lb['text'] = texto
            lb['bg'] = 'light gray'
            lb['foreground'] = 'black'
        else:
            lb['text'] = 'VALOR INVÁLIDO!'
            lb['foreground'] = 'red'

def save(cifra):
    open('cifras/' + ('{}-{}-{}').format(dia, mesesNum[tempo[1]], ano) + '.cifra', 'w').write('R$' + str(cifra))

def cifrasSalvas():
    def get_list(event):
        index = lista.curselection()[0]
        seltext = lista.get(index)

        global janela_terceira
        janela_terceira = Tk()

        cotDat = open('cifras/' + seltext + '.cifra', 'r')

        Label(janela_terceira, text='\n\nNo dia ' + seltext + '\n o dólar estava valendo R$ ' + cotDat.readline(),
              foreground='green').pack()

        janela_terceira.title('Resultado')
        janela_terceira.geometry('200x100+' + str(janela_segunda.winfo_x()) + '+' + str(janela_segunda.winfo_y()+300))
        janela_terceira.minsize(width=200, height=100)
        janela_terceira.maxsize(width=200, height=100)
        janela_terceira.focus_force()


    # Criando janela secundária
    global janela_segunda
    janela_segunda = Tk()

    # Procurando as cifras salvas
    cifras_salvas = os.listdir('cifras')

    # Criando Listbox onde os valores serão exibidos
    lista = Listbox(janela_segunda, cursor='hand2')
    lista.pack(side=LEFT, expand=TRUE, fill='both')
    lista.delete(END)
    lista.insert(END, 'Cotações anteriores:')
    lista['font'] = 'Calibri'
    lista.insert(END, '')

    # Criar barra de rolagem
    sb = Scrollbar(janela_segunda)
    sb.pack(side=RIGHT, fill=Y)
    sb.configure(command=lista.yview)
    lista.configure(yscrollcommand=sb.set)

    # Inserindo valores dentro da lista
    for i in range(0, len(cifras_salvas)):
        lista.insert(END, cifras_salvas[i].replace('.cifra', ''))

    lista.bind('<Double-Button-1>', get_list)  # Abrindo data selecionada

    # Configurando janela secundária
    janela_segunda.title('Cotações anteriores')
    janela_segunda.geometry('200x250+' + str(janela.winfo_x()-230) + '+' +  str(janela.winfo_y()))
    janela_segunda.minsize(width=200, height=250)
    janela_segunda.maxsize(width=200, height=250)
    janela_segunda.focus_force()

def sair():
    janela.destroy()
    janela_segunda.destroy()
    janela_terceira.destroy()

janela = Tk()

# Menu Toplevel
principal = Menu(janela)
arquivo = Menu(principal, tearoff=0)

principal.add_cascade(label='Ferramentas', menu=arquivo)

arquivo.add_command(label='Ver cotações anteriores', command=cifrasSalvas)
principal.add_command(label='Sair', command=sair)
janela.configure(menu=principal)

# Em caso de erro, usar essa chave: 7e43fe0e
requisicao = requests.get('https://api.hgbrasil.com/finance/quotations?format=json&key=7ebb58a4')
cotacao = json.loads(requisicao.text)
#cotacao = {'results':{'currencies': {'USD':{'buy': 3.8688}}}} # Apagar linha de testes
preco = cotacao['results']['currencies']['USD']['buy']

Label(janela, text='{} - {} de {} de {}'.format(diasSemana[tempo[0]], dia, meses[tempo[1]], ano)).pack(anchor=W)
Label(janela, text='Cotação: R${:.3} '.format(preco)).pack(anchor=W)

Label(janela, text='Digite um valor').place(x=10, y=100)
campo = Entry(janela)
campo.focus_force()
campo.place(x=100, y=100)

# Radiobuttons
var = StringVar(janela)
cache = open('value.cache', 'r') # Verificando valor do Radiobutton anterior
var.set(cache.readline()) # Valor padrão do Radiobutton
cache.close()

Radiobutton(janela, text='Real para dólar', variable=var, value='RD').place(x=100, y=130)
Radiobutton(janela, text='Dólar para Real', variable=var, value='DR').place(x=200, y=130)

# Botão Converter
Button(janela, text='CONVERTER', command=partial(conversor, var)).place(x=230, y=95)

# Criando Botão de Salvar
saveButton = Button(janela, text='Salvar', width=30, command=partial(save, preco)).place(x=50, y=220)

lb = Label(janela, text='', width=30)
lb.place(x=50, y=170)

janela.title('Conversor Real para Dólar')
janela.geometry('320x300+530+180')
janela.minsize(width=320, height=300)
janela.maxsize(width=320, height=300)
janela.iconbitmap('favicon.ico')
janela.mainloop()
