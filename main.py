import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import plotly.express as px
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split




def grafico(categoria, bebida, coluna):
    st.subheader(categoria)
    array1 = pd.DataFrame(columns=['Categoria', 'Quantidade'])
    m = dfb[coluna].value_counts().to_dict()
    i = 0
    for estilo in m:
        array1.loc[i] = [estilo, m[estilo]]
        i += 1

    fig = px.pie(array1, values='Quantidade', names='Categoria', title=f'{categoria} dos consumidores de {bebida}')
    st.plotly_chart(fig, use_container_width=True)

def opcoes(listagem):
    op = st.selectbox('Escolha', listagem)
    return op

def vetor_unico(valor, categoria, listax, lista_previsao):

    for i in range(len(lista_previsao), len(lista_previsao) + len(df[categoria].unique()) - 1):
        if valor in listax:
            if i == listax.index(valor):
                lista_previsao.append(1)
            else:
                lista_previsao.append(0)
        else:
            lista_previsao.append(0)
    return lista_previsao

def beb_recomendadas(bebidas_recomendadas, precisao):
    st.write(f'Cálculos com {precisao*100:.2f}% de precisão')
    if bebidas_recomendadas != {}:
        for k, value in bebidas_recomendadas.items():
            st.image(bebidas_imagens[k],caption=f'O usuário deve gostar de {k}',width=250)

    else:
        st.write('Atualmente, não há usuários cadastrados suficientes na base de dados para traçar este perfil. Por favor, tente novamente '
                 'mais tarde ou tente um novo perfil')




titulo = Image.open('titulo.png')
ama = Image.open('ama.jpg')
brahma = Image.open('brahma.jpg')
bud = Image.open('bud.jpg')
guarana = Image.open('guarana.jpg')
pepsi = Image.open('pepsi.jpg')
skol = Image.open('skol.jpg')
skolbeats = Image.open('skolbeats.jpg')
stella = Image.open('stella.jpg')




bebidas_imagens = {'Guaraná Artarctica':guarana ,'Brahma': brahma, 'Pepsi':pepsi, 'Skol Beats':skolbeats,
                   'Budweiser': bud, 'Stella Artois':stella, 'Água Ama': ama,'Cerveja Skol': skol}

dict_btn = {'idade': 'Faixa Etária', 'estado': 'Localidade', 'genero': 'Gênero',
                            'est_civil': 'Estado Civil', 'escolaridade': 'Escolaridade',
                            'renda': 'Renda', 'freq_bares': 'Frequência em bares',
            'freq_dist':'Frequência em Distribuidoras', 'freq_online': 'Frequência de compras de bebidas Online',
            'compras_rotina':'Frequência de compras de bebidas juntamente com compras de rotina', 'distancia':'Distância média que percorre para comprar a bebida',
            'dispositivos': 'Aparelhos eletrônicos que possui','pessoas_mesa':'Média de pessoas com quem costuma dividir a mesa',
            }

st.image(titulo,use_column_width=True)
st.title('DashBoard de Dados')
st.info('Escolha uma opção no menu à esquerda')

df = pd.read_csv('dados.csv')
df = df.rename(columns={'Qual sua faixa etária?': 'idade',
                        'Qual Estado reside?': 'estado',
                        'Qual gênero você se identifica?': 'genero',
                        'Qual seu estado civil?': 'est_civil',
                        'Qual maior grau de escolaridade alcançado até então?': 'escolaridade',
                        'Qual sua renda mensal aproximadamente?': 'renda',
                        'Com que frequência costumava ir à bares?': 'freq_bares',
                        'Com que frequência costuma ir à distribuidoras de bebidas?': 'freq_dist',
                        'Com que frequência costuma comprar bebidas online (aplicativos de entrega, lojas virtuais etc)?': 'freq_online',
                        'Você costuma comprar bebidas junto à compras de rotina no supermercado?': 'compras_rotina',
                        'Qual a distância média que percorre até o local onde costuma comprar suas bebidas?': 'distancia',
                        'Quais aparelhos/dispositivos abaixo você possui (conectados à internet)?': 'dispositivos',
                        'Qual a média de pessoas que divide a mesa com você em bares?': 'pessoas_mesa',
                        'Você costuma interagir com desconhecidos e se relacionar com novas pessoas em bares?': 'desconhecidos',
                        'Você costuma ter problemas ao dividir a conta em bares e restaurantes?': 'dividir_conta',
                        'Você já vivenciou situações de negligência, racismo, homofobia, preconceito ou algum tipo de exclusão no atendimento em bares?': 'preconceito',
                        'Você gostaria de receber uma bebida como presente?': 'receber_presente',
                        'Você gostaria de presentear alguém com uma bebida?': 'dar_presente',
                        'Quais dos fatores abaixo você acha mais importante na hora de escolher um bar? [Atendimento]': 'importante_atendimento',
                        'Quais dos fatores abaixo você acha mais importante na hora de escolher um bar? [Localização]': 'importante_localizacao',
                        'Quais dos fatores abaixo você acha mais importante na hora de escolher um bar? [Preço / Promoções]': 'importante_preco',
                        'Quais dos fatores abaixo você acha mais importante na hora de escolher um bar? [Decoração / Layout / Conforto]': 'importante_decoracao',
                        'Quais dos fatores abaixo você acha mais importante na hora de escolher um bar? [Música ao vivo]': 'importante_musica',
                        'Com que frequência você utiliza de video-chamadas ou teleconferências para falar com seus amigos e familiares?': 'videocham',
                        'Quantas transmissões ao vivo de apresentações artísticas ("lives") você costuma assistir por semana?': 'lives'
                        })
st.sidebar.info('Dados coletados dos usuários do aplicativo TAGalera')
df.drop('Timestamp', inplace=True, axis=1)
df.drop(
    'Você gostaria de responder mais algumas poucas questões específicas sobre suas experiências com serviço e atendimento em bares?',
    inplace=True, axis=1)
df.drop('Outras observações?', inplace=True, axis=1)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
dfr = df.iloc[:, :-2]

dfb = pd.DataFrame(columns=df.columns)

ver = st.sidebar.selectbox('O que deseja fazer?',['','Ver perfis de consumidores de cada bebida','Prever Bebida Preferida do Consumidor', 'Dados Reais',
                                                 'Dados Totais' ])
if ver == 'Ver perfis de consumidores de cada bebida':
    a = st.sidebar.radio('', df.bebida.unique())
    for bebida in df['bebida'].unique():
        if a == bebida:
            st.header(bebida)
            st.image(bebidas_imagens[bebida], width=300)
            for i in range(0, len(df)):
                if df['bebida'][i] == bebida:
                    dfb.loc[len(dfb)] = df.iloc[i, :]


            if st.checkbox(f'Mostrar gráficos com o perfil do consumidor'):

                for keys in dict_btn.keys():
                    grafico(dict_btn[keys], bebida, keys)

            if st.checkbox(f'Mostrar Tabela com dados coletados para a bebida {bebida}'):
                st.write(dfb)





if ver == 'Prever Bebida Preferida do Consumidor':


    ida = int(st.number_input('Idade',min_value=18))
    reg = st.selectbox('Estado',df.estado.unique())
    est = st.selectbox('Estado Civil',df.est_civil.unique())
    mus = st.selectbox('Música mais ouvida',df.musica.unique())
    gen = st.selectbox('Genero', df.genero.unique())
    ren = int(st.number_input('Renda Mensal R$',min_value=0, value=0, step=100))
    df_regressao = df.iloc[:, :5]
    df_regressao = pd.concat([df_regressao, df.musica, df.renda, df.bebida], axis=1)
    df_regressao.drop('escolaridade', inplace=True, axis=1)

    df_regressao.idade = df_regressao.idade.replace(['18 a 24', '25 à 34', '35 à 49','50 ou mais'],[21, 30, 42, 57])
    df_regressao.renda = df_regressao.renda.replace(['Até um salário mínimo (até R$ R$ 1.045,00)','De 1 a 3 salários mínimos (de R$ R$ 1.045,01 a R$ 3.135,00)',
                                                     'De 3 a 6 salários mínimos (de R$ R$ 3.135,00 a R$ 6.270,00)','De 6 a 9 salários mínimos (de R$ 6.270,01 a R$ 9.405,00)',
                                                     'De 9 a 12 salários mínimos (de R$ 9.405,01 a R$ 12.540,00)','Mais de 12 salários mínimos ( mais de R$ 12.540,01)'],
                                                    [522.5, 2090, 4702.5, 7837.5, 10972.5, 15675])


    if st.button('Ver Resultados'):
        bebidas_recomendadas = {}
        for bebida in df_regressao.bebida.unique():

            df_regressao_i = df_regressao.copy()

            for linha, val_bebida in enumerate(df_regressao_i.bebida):
               if val_bebida == bebida:
                   df_regressao_i.bebida[linha] = 1

               else:
                   df_regressao_i.bebida[linha] = 0

            regr = pd.get_dummies(df_regressao_i.estado,drop_first=True)
            estr = pd.get_dummies(df_regressao_i.est_civil,drop_first=True)
            musr = pd.get_dummies(df_regressao_i.musica, drop_first=True)
            genr = pd.get_dummies(df_regressao_i.genero, drop_first=True)
            df_regressao_i_calculo = pd.concat([regr, estr, musr, genr,df_regressao_i.idade, df_regressao_i.renda, df_regressao_i.bebida], axis=1)

            X = df_regressao_i_calculo.drop('bebida',axis=1)
            y = df_regressao_i_calculo['bebida']
            y = y.astype('int')

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=1)


            logmodel = LogisticRegression()
            logmodel.fit(X_train, y_train)
            prections = logmodel.predict(X_test)
            precisao = accuracy_score(y_test, prections)



            lista_previsao = []

            listax = list(X.columns)
            lista_previsao = vetor_unico(reg, 'estado', listax, lista_previsao)
            lista_previsao = vetor_unico(est, 'est_civil', listax, lista_previsao)
            lista_previsao = vetor_unico(mus, 'musica', listax, lista_previsao)
            lista_previsao = vetor_unico(gen, 'genero', listax, lista_previsao)
            lista_previsao.append(ida)
            lista_previsao.append(ren)

            previsao =logmodel.predict([lista_previsao])
            if previsao == 1:
                bebidas_recomendadas[bebida] = True

        beb_recomendadas(bebidas_recomendadas, precisao)


if ver == 'Dados Reais':
    if st.checkbox('Ver tabela com dados reais'):
        st.header('Dados Reais')
        st.write('Dados coletados a partir de pesquisa feita por integrantes do time 30')
        st.write(dfr)

if ver == 'Dados Totais':
    st.info("As colunas música e bebida foram geradas aleatóriamente para simular resultados obtidos através do app")
    if st.checkbox('Ver tabela com todos os dados'):
        st.header('Todos os Dados')
        st.write(df)


