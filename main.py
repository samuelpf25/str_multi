# última edição 04/03/2024
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from datetime import date, datetime
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

# ocultar menu
hide_streamlit_style = """
<meta http-equiv="Content-Language" content="pt-br">
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# fim ocultar menu

# 1) DECLARAÇÃO DE VARIÁVEIS GLOBAIS ####################################################################################
scope = ['https://spreadsheets.google.com/feeds']
k = "@MEngenharia"
creds = ServiceAccountCredentials.from_json_keyfile_name("controle.json", scope)

cliente = gspread.authorize(creds)

# sheet = cliente.open("Ciente Limpeza").sheet1 # Open the spreadhseet

sheet = cliente.open_by_url(
    'https://docs.google.com/spreadsheets/d/1uS7_GS6KR9ax4tOhAeEzhpnlPJX6_13m0CCD_9QWbKk/edit?gid=0#gid=0').get_worksheet(
    0)  # https://docs.google.com/spreadsheets/d/1PhJXFOKdEAjcILQCDyJ-couaDM6EWBUXM1GVh-3gZWM/edit#gid=96577098

dados = sheet.get_all_records()  # Get a list of all records

df = pd.DataFrame(dados)
df = df.astype(str)

#
datando = []
data_hora = []
nome_solicitante = []
area_manutencao = []
tipo_solicitacao = []
descricao_sucinta = []
localizacao = []
info_adicionais = []
data_solicitacao = []
ordem_servico = []
obsinterna = []
urg_ufes = []
urg_multi = []
status_multi = []
data_status = []
alerta_coluna = []
pontos = []
obs_usuario = []
obs_interna = []

horas = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
         '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30']

# 2) padroes #####################################################################################################
padrao = '<p style="font-family:Courier; color:Blue; font-size: 16px;">'
infor = '<p style="font-family:Courier; color:Green; font-size: 16px;">'
alerta = '<p style="font-family:Courier; color:Red; font-size: 17px;">'
titulo = '<p style="font-family:Courier; color:Blue; font-size: 20px;">'
cabecalho = '<div id="logo" class="span8 small"><h1>CONTROLE DE ORDENS DE SERVIÇO - UFES</h1></div>'


# @st.cache
# def carrega_todos(status,indice,os,obsemail,obsinterna):
#     status = st.selectbox('Selecione o status:', status, index=indice)
#     os = st.text_input('Número da OS:', value=os[n])
#     obs_email = st.text_area('Observação para o Usuário:', value=obsemail[n])
#     obs_interna = st.text_area('Observação Interna:', value=obsinterna[n])
#     s = st.text_input("Senha:", value="", type="password")  # , type="password"
#     return status,os,obs_email,obs_interna,s

# 3) FUNÇÕES GLOBAIS #############################################################################################


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list) + 1)


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='OS')
    workbook = writer.book
    worksheet = writer.sheets['OS']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.close()
    processed_data = output.getvalue()
    return processed_data


# 4) PÁGINAS ####################################################################################


st.sidebar.title('Gestão Manutenção Predial')
a = k
# pg=st.sidebar.selectbox('Selecione a Página',['Solicitações em Aberto','Solicitações a Finalizar','Consulta'])
pg = st.sidebar.radio('', ['Edição individual', 'Edição em Lote', 'Consulta'])
status = ['', 'Todas Ativas', 'OS Aberta','Pendente de Material','Pendente Solicitante','Pendente Outros','Atendida','Material Solicitado','Material Disponível']
status_todos = ['', 'OS Aberta','Pendente de Material','Pendente Solicitante','Pendente Outros','Atendida','Material Solicitado','Material Disponível']
if (pg == 'Edição individual'):
    # PÁGINA EDIÇÃO INDIVIDUAL ******************************************************************************************
    st.markdown(cabecalho, unsafe_allow_html=True)
    st.subheader(pg)
    # cabeçalho

    col1, col2 = st.columns(2)
    filtrando = col1.multiselect('Selecione o Status para Filtrar', status)
    # print(filtrando)
    filtra_os = col2.text_input('Filtrar OS:', value='')
   #data_hora	nome_solicitante	area_manutencao	tipo_solicitacao	descricao_sucinta	localizacao	info_adicionais	data_solicitacao		urg_ufes	urg_multi	status_multi	data_status	alerta_coluna	pontos
    for dic in df.index:
        if (filtrando == ['Todas Ativas']):
            filtrando = status_todos
        if filtra_os != '':
            if df['status_multi'][dic] in filtrando and df['area_manutencao'][dic] != '' and str(df['ordem_servico'][dic]) == str(filtra_os):
                # print(df['Código da UFT'][dic])
                data_hora.append(df['data_hora'][dic])
                nome_solicitante.append(df['nome_solicitante'][dic])
                area_manutencao.append(df['area_manutencao'][dic])
                tipo_solicitacao.append(df['tipo_solicitacao'][dic])
                descricao_sucinta.append(df['descricao_sucinta'][dic])
                localizacao.append(df['localizacao'][dic])
                info_adicionais.append(df['info_adicionais'][dic])
                data_solicitacao.append(df['data_solicitacao'][dic])
                urg_ufes.append(df['urg_ufes'][dic])
                urg_multi.append(df['urg_multi'][dic])
                status_multi.append(df['status_multi'][dic])
                data_status.append(df['data_status'][dic])
                alerta_coluna.append(df['alerta_coluna'][dic])
                pontos.append(df['pontos'][dic])
                ordem_servico.append(df['ordem_servico'][dic])
                obs_usuario.append(df['obs_usuario'][dic])
                obs_interna.append(df['obs_interna'][dic])

        else:

            if df['status_multi'][dic] in filtrando and df['area_manutencao'][dic] != '':
                data_hora.append(df['data_hora'][dic])
                nome_solicitante.append(df['nome_solicitante'][dic])
                area_manutencao.append(df['area_manutencao'][dic])
                tipo_solicitacao.append(df['tipo_solicitacao'][dic])
                descricao_sucinta.append(df['descricao_sucinta'][dic])
                localizacao.append(df['localizacao'][dic])
                info_adicionais.append(df['info_adicionais'][dic])
                data_solicitacao.append(df['data_solicitacao'][dic])
                urg_ufes.append(df['urg_ufes'][dic])
                urg_multi.append(df['urg_multi'][dic])
                status_multi.append(df['status_multi'][dic])
                data_status.append(df['data_status'][dic])
                alerta_coluna.append(df['alerta_coluna'][dic])
                pontos.append(df['pontos'][dic])
                ordem_servico.append(df['ordem_servico'][dic])
                obs_usuario.append(df['obs_usuario'][dic])
                obs_interna.append(df['obs_interna'][dic])

    if len(data_hora) > 1 and (filtra_os != ''):
        st.markdown(
            alerta + f'<Strong><i>Foram encontradas {len(data_hora)} Ordens de Serviço com este mesmo número, selecione abaixo a solicitação correspondente:</i></Strong></p>',
            unsafe_allow_html=True)
    selecionado = st.selectbox('Nº da OS:', ordem_servico)

    if (len(ordem_servico) > 0):
        n = ordem_servico.index(selecionado)

        # apresentar dados da solicitação
        st.markdown(titulo + '<b>Dados da Solicitação</b></p>', unsafe_allow_html=True)
        # st.text('<p style="font-family:Courier; color:Blue; font-size: 20px;">Nome: '+ nome[n]+'</p>',unsafe_allow_html=True)

        st.markdown(padrao + '<b>Nome</b>: ' + str(nome_solicitante[n]) + '</p>', unsafe_allow_html=True)
        st.markdown(padrao + '<b>Área</b>: ' + str(area_manutencao[n]) + '</p>', unsafe_allow_html=True)
        st.markdown(padrao + '<b>Tipo de solicitação</b>: ' + str(tipo_solicitacao[n]) + '</p>', unsafe_allow_html=True)
        st.markdown(padrao + '<b>Localizacao</b>: ' + str(localizacao[n]) + '</p>', unsafe_allow_html=True)
        st.markdown(padrao + '<b>Data da Solicitação</b>: ' + str(data_hora[n]) + '</p>', unsafe_allow_html=True)
        st.markdown(alerta + '<b>Descrição</b>: ' + str(descricao_sucinta[n]) + '</p>', unsafe_allow_html=True)
        st.markdown(padrao + '<b>Informações adicionais</b>: ' + info_adicionais[n] + '</p>', unsafe_allow_html=True)
        st.markdown(padrao + '<b>Urgência UFES</b>: ' + urg_ufes[n] + '</p>', unsafe_allow_html=True)

        celula = sheet.find(str(ordem_servico[n]))
        # procurando status equivalente na lista
        indice = 0
        cont = 0
        numero = ""
        for j in status:
            if j == status_multi[n]:
                indice = cont
                numero = j
            cont = cont + 1

        cont = 0
        for urg in ['Baixa', 'Média', 'Alta']:
            if urg ==urg_multi[n]:
                i_urg = cont
                break
            cont+=1
        with st.form(key='my_form'):
            status_reg = st.selectbox('Selecione o status:', status, index=indice)
            obs_usr = st.text_area('Observação para o Usuário:', value=obs_usuario[n])
            obs_int = st.text_area('Observação Interna:', value=obs_interna[n])
            urg_m = st.selectbox('Urgência Multi:', ['Baixa','Média','Alta'],index=i_urg)

            s = st.text_input("Senha:", value="", type="password")  # , type="password"

            botao = st.form_submit_button('Registrar')

        if (botao == True and s == a):
            if (sheet.cell(celula.row, 8).value == ordem_servico[n] and sheet.cell(celula.row, celula.row, 8).value != ''):
                with st.spinner('Registrando dados...Aguarde!'):
                    st.markdown(infor + '<b>Registro efetuado!</b></p>', unsafe_allow_html=True)

                    sheet.update_acell('K' + str(celula.row), urg_m)  # Status
                    sheet.update_acell('L' + str(celula.row), status_reg)  # os
                    sheet.update_acell('M' + str(celula.row), obs_usr)  # obs_email
                    sheet.update_acell('N' + str(celula.row), obs_int)  # obs_interna

                    data_hoje = datetime.today()
                    data_reg = datetime.strptime(data_hoje, '%dd/%mm/%YYYY')
                    sheet.update_acell('O' + str(celula.row), data_reg)

                st.success('Registro efetuado!')
            else:
                st.error('Código de OS inválido!')
        elif (botao == True and s != a):
            st.markdown(alerta + '<b>Senha incorreta!</b></p>', unsafe_allow_html=True)
    else:
        st.markdown(infor + '<b>Não há itens na condição ' + pg + '</b></p>', unsafe_allow_html=True)

elif pg == 'Edição em Lote':

    # PÁGINA EDIÇÃO EM LOTE  ******************************************************************************************
    st.markdown(cabecalho, unsafe_allow_html=True)

    st.subheader(pg)
    col1, col2 = st.columns(2)
    filtrando = col1.multiselect('Selecione o Status para Filtrar', status)
    if (filtrando == ['Todas Ativas']):
        filtrando = status_todos
    os_gerais = []
    for dic in df.index:
        if (filtrando != ''):
            if df['ordem_servico'][dic] != '' and df['status_multi'][dic] in filtrando:
                os_gerais.append(df['ordem_servico'][dic])
        else:
            if df['ordem_servico'] != '':
                os_gerais.append(df['ordem_servico'][dic])

    filtra_os = col2.multiselect('Filtrar OS:', os_gerais)
    for dic in df.index:
        print(str(df['ordem_servico'][dic]))
        # print(str(filtra_os))
        if filtra_os != '':
            if df['status_multi'][dic] in filtrando and df['area_manutencao'][dic] != '' and (
                    str(df['ordem_servico'][dic]) in filtra_os) and (str(df['ordem_servico'][dic]) != '') and (
                    str(df['ordem_servico'][dic]) != 0):
                data_hora.append(df['data_hora'][dic])
                nome_solicitante.append(df['nome_solicitante'][dic])
                area_manutencao.append(df['area_manutencao'][dic])
                tipo_solicitacao.append(df['tipo_solicitacao'][dic])
                descricao_sucinta.append(df['descricao_sucinta'][dic])
                localizacao.append(df['localizacao'][dic])
                info_adicionais.append(df['info_adicionais'][dic])
                data_solicitacao.append(df['data_solicitacao'][dic])
                urg_ufes.append(df['urg_ufes'][dic])
                urg_multi.append(df['urg_multi'][dic])
                status_multi.append(df['status_multi'][dic])
                data_status.append(df['data_status'][dic])
                alerta_coluna.append(df['alerta_coluna'][dic])
                pontos.append(df['pontos'][dic])
                ordem_servico.append(df['ordem_servico'][dic])
                obs_usuario.append(df['obs_usuario'][dic])
                obs_interna.append(df['obs_interna'][dic])
        else:
            if df['status_multi'][dic] in filtrando and df['area_manutencao'][dic] != '':
                # print(df['Código da UFT'][dic])
                data_hora.append(df['data_hora'][dic])
                nome_solicitante.append(df['nome_solicitante'][dic])
                area_manutencao.append(df['area_manutencao'][dic])
                tipo_solicitacao.append(df['tipo_solicitacao'][dic])
                descricao_sucinta.append(df['descricao_sucinta'][dic])
                localizacao.append(df['localizacao'][dic])
                info_adicionais.append(df['info_adicionais'][dic])
                data_solicitacao.append(df['data_solicitacao'][dic])
                urg_ufes.append(df['urg_ufes'][dic])
                urg_multi.append(df['urg_multi'][dic])
                status_multi.append(df['status_multi'][dic])
                data_status.append(df['data_status'][dic])
                alerta_coluna.append(df['alerta_coluna'][dic])
                pontos.append(df['pontos'][dic])
                ordem_servico.append(df['ordem_servico'][dic])
                obs_usuario.append(df['obs_usuario'][dic])
                obs_interna.append(df['obs_interna'][dic])
    # if len(n_solicitacao)>1:
    #    st.markdown(alerta + f'<Strong><i>Foram encontradas {len(n_solicitacao)} Ordens de Serviço com este mesmo número, exclua da lista abaixo a solicitação que não for correspondente a que queira editar:</i></Strong></p>',unsafe_allow_html=True)

    selecionado = st.multiselect('Nº da solicitação:', ordem_servico, ordem_servico)
    filtro = selecionado
    dados1 = df[['area_manutencao', 'localizacao', 'data_solicitacao', 'ordem_servico', 'status_multi']]
    filtrar = dados1['ordem_servico'].isin(filtro)
    # print(dados1[filtrar]['Ordem de Serviço'].value_counts())
    # print(dados1[filtrar]['Ordem de Serviço'].value_counts().values)
    lista_repetidos = list(dados1[filtrar]['ordem_servico'].value_counts().values)
    repeticao = 0
    for repetido in lista_repetidos:
        #    valor = dados1['Ordem de Serviço'].value_counts()
        if int(repetido) > 1:
            st.markdown(
                alerta + f'<Strong><i>Foram encontradas Ordens de Serviço com números repetidos, exclua da lista a solicitação que não for correspondente a que queira editar</i></Strong></p>',
                unsafe_allow_html=True)
            repeticao = 1
            break
    st.dataframe(dados1[filtrar].head())
    # selecionado=n_solicitacao
    # print(nome[n_solicitacao.index(selecionado)])
    if (1 > 0):  # len(n_solicitacao)

        # procurando status equivalente na lista
        with st.form(key='my_form'):
            status_reg = st.selectbox('Selecione o status:', status)
            obs_usr = st.text_area('Observação para o Usuário:', value='')
            obs_int = st.text_area('Observação Interna:', value='')
            urg_m = st.selectbox('Urgência Multi:', ['Baixa','Média','Alta'])

            s = st.text_input("Senha:", value="", type="password")  # , type="password"
            botao = st.form_submit_button('Registrar')
            efetuado = 0
        if (botao == True and s == a):
            with st.spinner('Registrando dados...Aguarde!'):
                for selecionado_i in selecionado:
                    celula = sheet.find(str(selecionado_i))
                    # sheet.update_acell('P' + str(celula.row), status)  # Status
                    # print(sheet.cell(celula.row, 20).value)
                    # print(repeticao)
                    # print(selecionado_i)
                    if (sheet.cell(celula.row, 20).value == selecionado_i and sheet.cell(celula.row,
                                                                                         20).value != '' and repeticao == 0):
                        efetuado = 1
                        if urg_m!='':
                            sheet.update_acell('K' + str(celula.row), urg_m) 
                            
                        if (status_reg != ''):
                            sheet.update_acell('L' + str(celula.row), status_reg)      
                            data_hoje = datetime.today()
                            data_reg = datetime.strptime(data_hoje, '%dd/%mm/%YYYY')
                            sheet.update_acell('O' + str(celula.row), data_reg)
                        
                        # sheet.update_acell('R' + str(celula.row), '')  # apagar Sim para enviar e-mail
                        if (obs_usr != ''):
                            # sheet.update_acell('S' + str(celula.row), obsemail)  # obs_email
                            sheet.update_acell('M' + str(celula.row), obs_usr)
                        if (obs_int != ''):
                            # sheet.update_acell('AA' + str(celula.row), obsinterna)  # obs_interna
                            sheet.update_acell('N' + str(celula.row), obs_int)  # obs_interna

                            # st.markdown(infor+'<b>Registro efetuado!</b></p>',unsafe_allow_html=True)
            if (efetuado == 1):
                st.success('Registro efetuado!')
            elif (efetuado == 0 and repeticao == 1):
                st.error('Remova as OS com números repetidos!')
            elif (efetuado == 1 and repeticao == 1):
                st.error('Dados parcialmente cadastrados! As OS com números repetidos não foram registradas!')
        elif (botao == True and s != a):
            st.markdown(alerta + '<b>Senha incorreta!</b></p>', unsafe_allow_html=True)
    else:
        st.markdown(infor + '<b>Não há itens na condição ' + pg + '</b></p>', unsafe_allow_html=True)
elif pg == 'Consulta':

    # PÁGINA DE CONSULTA ************************************************************************************************

    # dados = sheet.get_all_records()  # Get a list of all records
    # df = pd.DataFrame(dados)
    n_solicitacao.append('')
    nome.append('')
    telefone.append('')
    predio.append('')
    sala.append('')
    data.append('')
    observacao.append('')
    os.append('')
    obsemail.append('')
    obsinterna.append('')
    stat.append('')

    for dic in df.index:
        if df['localizacao'][dic] != '':
            # print(df['Código da UFT'][dic])
            data_hora.append(df['data_hora'][dic])
            nome_solicitante.append(df['nome_solicitante'][dic])
            area_manutencao.append(df['area_manutencao'][dic])
            tipo_solicitacao.append(df['tipo_solicitacao'][dic])
            descricao_sucinta.append(df['descricao_sucinta'][dic])
            localizacao.append(df['localizacao'][dic])
            info_adicionais.append(df['info_adicionais'][dic])
            data_solicitacao.append(df['data_solicitacao'][dic])
            urg_ufes.append(df['urg_ufes'][dic])
            urg_multi.append(df['urg_multi'][dic])
            status_multi.append(df['status_multi'][dic])
            data_status.append(df['data_status'][dic])
            alerta_coluna.append(df['alerta_coluna'][dic])
            pontos.append(df['pontos'][dic])
            ordem_servico.append(df['ordem_servico'][dic])
            obs_usuario.append(df['obs_usuario'][dic])
            obs_interna.append(df['obs_interna'][dic])

    st.markdown(cabecalho, unsafe_allow_html=True)
    st.subheader(pg)
    titulos = ['data_hora','nome_solicitante','area_manutencao','tipo_solicitacao','descricao_sucinta','info_adicionais','data_solicitacao','urg_ufes','urg_multi','status_multi','data_status','alerta_coluna','pontos','ordem_servico','obs_usuario','obs_interna']
    with st.form(key='form1'):
        tit_plan = titulos
        coluna_busca = st.selectbox('Coluna para busca por argumento', tit_plan)
        texto = st.text_input('Busca por argumento na coluna selecionada: ')
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)
        filtrar = []

        dados = df[titulos]
        valor = data_solicitacao
        valor = list(dict.fromkeys(valor))  # removendo valores duplicados
        valor = sorted(valor)  # ordenando lista de string
        filtro_data = col1.multiselect('Filtrar por Data:', valor)
        if (len(filtro_data) > 0):
            if (len(filtrar) > 0):
                filtrar = filtrar & dados['data_solicitacao'].isin(filtro_data)
            else:
                filtrar = dados['data_solicitacao'].isin(filtro_data)

        valor = ordem_servico
        valor = list(dict.fromkeys(valor))  # removendo valores duplicados
        valor = sorted(valor)  # ordenando lista de string
        filtro_os = col2.multiselect('Filtrar por Ordem de Serviço:', valor)
        if (len(filtro_os) > 0):
            if (len(filtrar) > 0):
                filtrar = filtrar & dados['ordem_servico'].isin(filtro_os)
            else:
                filtrar = dados['ordem_servico'].isin(filtro_os)
        valor = nome_solicitante
        valor = list(dict.fromkeys(valor))  # removendo valores duplicados
        valor = sorted(valor)  # ordenando lista de string
        filtro_solicitante = col3.multiselect('Filtrar por Nome do Solicitante:', valor)
        if (len(filtro_solicitante) > 0):
            # filtro_solicitante=valor
            if (len(filtrar) > 0):
                filtrar = filtrar & dados['nome_solicitante'].isin(filtro_solicitante)
            else:
                filtrar = dados['nome_solicitante'].isin(filtro_solicitante)

        valor = status_multi
        valor = list(dict.fromkeys(valor))  # removendo valores duplicados
        valor = sorted(valor)  # ordenando lista de string
        filtro_status = col4.multiselect('Filtrar por Status:', valor)
        if (len(filtro_status) > 0):
            if (len(filtrar) > 0):
                filtrar = filtrar & dados['status_multi'].isin(filtro_status)
            else:
                filtrar = dados['status_multi'].isin(filtro_status)

        valor = localizacao
        valor = list(dict.fromkeys(valor))  # removendo valores duplicados
        valor = sorted(valor)  # ordenando lista de string
        filtro_predio = col5.multiselect('Filtrar por localização:', valor)
        if (len(filtro_predio) > 0):
            if (len(filtrar) > 0):
                filtrar = filtrar & dados['localizacao'].isin(filtro_predio)
            else:
                filtrar = dados['localizacao'].isin(filtro_predio)

        btn1 = st.form_submit_button('Filtrar')
        if (len(filtrar) == 0):
            filtrar = titulos
    if (btn1 == True):
        # dados=df[titulos]
        # filtrar=dados[titulo_coluna].isin([filtro])
        # print(filtrar)
        # if(len(filtrar)>0):
        if (texto != '' and coluna_busca != ''):
            dad1 = dados[filtrar][dados[coluna_busca].str.contains(texto, na=False)]
            # dad2 = dados[filtrar][dados['Carimbo de data/hora'].str.contains(texto, na=False)]
            dad = dad1
        else:
            dad = dados[filtrar]
        st.dataframe(dad)  # dados[filtrar].head()
        df_xlsx = to_excel(dad)
        st.download_button(label='📥 Baixar Resultado do Filtro em Excel', data=df_xlsx,
                           file_name='filtro_planilha.xlsx')
        # dados_graf=pd.DataFrame(dados[filtrar],columns=[coluna1,coluna2])
        # fig = px.bar(dados_graf, x=coluna1, y=coluna2, barmode='group', height=400)
        # st.plotly_chart(fig)
        # plost.line_chart(dados_graf, coluna1, coluna2)

        # else:
        #    st.dataframe(df[titulos])
    else:
        st.dataframe(df[titulos])


