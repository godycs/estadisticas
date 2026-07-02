import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import plotly.express as px

# import calmap
##################################
# LECTURA DE LOS ARCHIVOS
##################################

try:
    sheet_url1 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQA8Myx6exmmDQBzrTUAsh669fAI8K3i_PGmwKfJTrXINaZJ8FZV5blmk8ZShVSTyzm97oq1ZZxsFnF/pub?gid=0&single=true&output=csv'

    df = pd.read_csv(sheet_url1,index_col=0)

except Exception as e: 
    print(f"ERROR importando archivo1 {e}")

try:
    sheet_url2 = 'https://docs.google.com/spreadsheets/d/1MfYXz8lKmjvb9kK9eD1bONuLL4nKbw07YwfEUop47js/export?format=csv&gid=498017106'

    # Leer el contenido directamente en un DataFrame
    df = pd.read_csv(sheet_url2)

except Exception as e: 
    print(f"ERROR importando     archivo2 {e}")


##################################
# ESTILOS
##################################

# Cambiar el color de fondo usando CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000691;  /* Cambia este valor al color que desees */
    }
    </style>
    """,
    unsafe_allow_html=True
)

##################################
# MUESTREO DE LOS DATOS
##################################

st.title('Requerimientos Godycs')
st.write('Lista de Requerimientos')
# Crear nueva columna unificada
# df['Nombre_Responsable'] = df['Nombre y Apellido:'].combine_first(df['Nombre y Apellido:.1'])
df.drop(columns=['Nombre y Apellido:'])
# Cambiar el nombre de una columna
df.rename(columns={'Nombre y Apellido:.1': 'Nombre_Responsable'}, inplace=True)
st.write(df)
st.write('Requerimientos por DG')

# Obtener la columna de interés
columna_dg = '¿A qué área pertenece?'

# Contar ocurrencias de cada área
conteo_dg = df[columna_dg].value_counts()

# Separar en mayores o iguales a 10 y menores a 10
conteo_filtrado = conteo_dg[conteo_dg >= 10]
conteo_otras = conteo_dg[conteo_dg < 10]

# Agregar la suma de las categorías pequeñas como "Otras"
conteo_final = conteo_filtrado.copy()
conteo_final['Otras'] = conteo_otras.sum()


# Mostrar datos
st.write("Conteo por área:")
st.write(conteo_final)


# Crear gráfico de torta
fig, ax = plt.subplots()
fig.patch.set_facecolor('#f0f2f6')  # color del fondo de la figura
ax.pie(conteo_final, labels=conteo_final.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Para que el gráfico sea un círculo
st.pyplot(fig)


# st.write("Pedidos por fecha")

# # Asegurarse de que la columna de fecha esté en formato datetime
# df['Marca temporal'] = pd.to_datetime(df['Marca temporal'], errors='coerce', dayfirst=True)

# # Agrupar por fecha (sin horas)
# df['fecha'] = df['Marca temporal'].dt.date
# # st.write(df['fecha'])
# # fechas = df['fecha'] 
# conteo_fecha = df['fecha'].value_counts()
# requerimientos_por_fecha = df.groupby('fecha').size()

# # Ordenar por fecha
# requerimientos_por_fecha = requerimientos_por_fecha.sort_index()
# st.write(requerimientos_por_fecha)

# Graficar
# fig, ax = plt.subplots()
# fig.patch.set_facecolor('#f0f2f6')
# ax.plot(requerimientos_por_fecha.index, requerimientos_por_fecha.values, marker='o', linestyle='-')
# ax.set_title('Cantidad de requerimientos por fecha')
# ax.set_xlabel('Fecha')
# ax.set_ylabel('Cantidad')
# ax.tick_params(axis='x', rotation=45)
# plt.tight_layout()
# st.pyplot(fig)

# df['fecha'] = pd.to_datetime(df['Marca temporal'], errors='coerce')
# df['mes'] = df['fecha'].dt.to_period('M')  # Agrupa por mes
# requerimientos_por_mes = df.groupby('mes').size()


# fig, ax = plt.subplots()
# fig.patch.set_facecolor('#f0f2f6')
# # ax.bar(requerimientos_por_fecha.index, requerimientos_por_fecha.values, color='skyblue')
# # ax.set_title('Cantidad de requerimientos por fecha')
# # ax.set_xlabel('Fecha')
# # ax.set_ylabel('Cantidad')
# # ax.tick_params(axis='x', rotation=45)
# # plt.tight_layout()
# # st.pyplot(fig)

# plt.plot(requerimientos_por_fecha.index, requerimientos_por_fecha.values, linestyle="solid")

# plt.gcf().set_size_inches(8, 6)
# plt.tight_layout()
# plt.show()

# plt.tight_layout()
# st.pyplot(fig)


######################################################################
# st.write("HEATMAP reqs x fecha")


# Asegurate de que la columna de fecha está en datetime
# df['Marca temporal'] = pd.to_datetime(df['Marca temporal'])

# Agrupar la cantidad de requerimientos por fecha (sin hora)
conteo_diario = df['Marca temporal'].dt.date.value_counts()
conteo_diario = conteo_diario.sort_index()

# Convertir a Serie con datetime index
serie_conteo = pd.Series(conteo_diario.values, index=pd.to_datetime(conteo_diario.index))

# Obtener lista de años únicos
años_disponibles = sorted(serie_conteo.index.year.unique(), reverse=True)

# Mostrar selector de año
año_seleccionado = st.selectbox("Seleccioná un año", años_disponibles)

# Filtrar datos del año seleccionado
serie_filtrada = serie_conteo[serie_conteo.index.year == año_seleccionado]

# Mostrar tabla opcional
st.write(f"Requerimientos por fecha en {año_seleccionado}:")
# st.dataframe(serie_filtrada)

# Crear el heatmap estilo GitHub
# fig, ax = plt.subplots(figsize=(12, 4))
# calmap.calendarplot(serie_filtrada, how='sum', cmap='YlGn', fillcolor='lightgray', linewidth=0.5)
# fig = plt.gcf()
# st.pyplot(fig)

# Supongamos que ya tenés una serie con fechas
# serie_filtrada = pd.Series(...)

df = serie_filtrada.reset_index()
print(df)
df.columns = ["date", "value"]

df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.dayofweek
# df["week"] = df["date"].dt.isocalendar().week
# df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

fig = px.density_heatmap(
    df,
    x="month",
    y="day",
    z="value",
    histfunc="sum",
    nbinsx=12,   # 👈 clave
    nbinsy=7,    # 👈 clave
    color_continuous_scale="Blues",
    range_x=[1, 12],

    
)

fig.update_layout(
    yaxis=dict(
        tickmode='array',
        tickvals=[0,1,2,3,4,5,6],
        ticktext=['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=[1,2,3,4,5,6,7,8,9,10,11,12],
        ticktext=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    )
)

st.plotly_chart(fig)

######################################################################


# # Convertir la columna 'timestamp' a tipo datetime
# df['Marca temporal'] = pd.to_datetime(df['Marca temporal'])

# # Extraer día, mes y año en columnas separadas
# df['dia'] = df['Marca temporal'].dt.day
# df['mes'] = df['Marca temporal'].dt.month
# df['anio'] = df['Marca temporal'].dt.year

# # Crear un DataFrame de los requerimientos por fecha
# data = {'dia': df['dia'] ,
#         'mes': df['mes'],
#         'anio': df['anio']
#         }
# dFecha = pd.DataFrame(data)

# # st.write(dFecha)

######################################################################

# conteoFechas = dFecha.value_counts()
# # print(conteoFechas)
# st.write(conteoFechas)

# reqs_x_fecha = df(["dia"],["mes"],["anio"])
# st.write(reqs_x_fecha)

# reqs = sb.load_dataset("conteoFechas").pivot
# reqs = conteoFechas.pivot(index="mes", columns = "dia", values="count")
# glue = sns.load_dataset("glue").pivot(index="Model", columns="Task", values="Score")


# sb.heatmap(conteoFechas)
# ax.set_title('Cantidad de requerimientos por fecha22') 
# ax.set(xlabel="Fecha", ylabel="Cantidad")
# ax.xaxis.tick_top()

