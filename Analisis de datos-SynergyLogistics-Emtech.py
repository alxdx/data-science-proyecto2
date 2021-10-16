#!/usr/bin/env python
# coding: utf-8
# este codigo fue generado por mi jupyter notebook, ver adjunto
# In[2]:


import pandas as pd
import matplotlib as matplt
import squarify
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [15, 7.5]


#  ## Importacion de la base de datos

# In[3]:


data = pd.read_csv("synergy_logistics_database.csv")
data['date'] = pd.to_datetime(data['date'])
data


# ## Info del tipo de datos que pandas detecta
# * no necesita limpieza pq los datos estan completos
# 
# ### Del método *nunique()* podemos observar y plantearnos ciertas preguntas:
# 
#    * **19056 registros** de transporte a lo largo de 6 años
#    * de **6 años de actividades** se operaron 912 dias, lo equivalente a **2 años y medio**, seria interesante revisar las fechas de mas actividad y preguntarnos 
#        + *¿se podran predecir y destinar recursos a ciertas operaciones?*
#    * se han transportado 28 tipos diferentes de productos
#    * se opera para 77 compañias diferentes: 
#        + *¿se podria guiar la estrategia a las compañias que generan mas valor?*
#    <br><br>
#    * En los ultimos seis años se han transportado **$ 215,691,298,000**

# In[4]:


valor_total_hist = data["total_value"].sum()


# In[5]:


data.nunique()


# In[6]:


data['direction'].value_counts()


# In[7]:


print("Valor Importaciones: % {}".format(data['direction'].value_counts().Imports * 100 / 19056))
print("Valor Exportaciones: % {}".format(data['direction'].value_counts().Exports * 100 / 19056))
data['direction'].value_counts().plot(kind='pie',title='Cantidad total de importaciones y exportaciones')


# In[8]:


data.groupby(['direction'])['total_value'].sum()


# In[9]:


print("Valor Importaciones: % {}".format(data.groupby(['direction'])['total_value'].sum().Imports * 100 / valor_total_hist))
print("Valor Exportaciones: % {}".format(data.groupby(['direction'])['total_value'].sum().Exports * 100 / valor_total_hist))
data.groupby(['direction'])['total_value'].sum().plot(kind='pie',title='Porcentaje de rutas mas valiosas por Importacion/Exportacion')


# ### Rutas mas populares
# #### Estas rutas representan el %80 del total de rutas trabajadas en los ultimos 6 años - 85 Rutas

# In[25]:


rutas_populares = data.groupby(['origin','destination'])['register_id'].count().reset_index().sort_values(['register_id'],ascending=False).set_index(["origin","destination"])
rutas_populares.cumsum().loc[rutas_populares.cumsum()['register_id'] < 19056 * .8 ]
rutas_populares.iloc[:85].plot(kind='bar',title='Rutas mas populares (80%)')


# ### Rutas mas valiosas
# #### Estas rutas representan el %80 del total de rutas trabajadas en los ultimos 6 años - 54 rutas 

# In[11]:


data.groupby(['origin','destination'])['total_value'].sum()
rutas_mas_valiosas = data.groupby(['origin','destination'])['total_value'].sum().reset_index().sort_values(['total_value'],ascending=False).set_index(["origin","destination"])
#rutas_mas_valiosas
rutas_mas_valiosas.loc[rutas_mas_valiosas.cumsum()['total_value'] < valor_total_hist * .8 ].plot(kind='bar')


# In[41]:


##-> aqui me quede, hay que acceder a la columna de los paises de origen para obtener una
##lista de los paises en los cuales enfocarse
rutas_mas_valiosas.reset_index().loc[:54,['origin']].value_counts()#.iloc[:11].plot.pie()


# In[43]:


resumen_rutas = pd.concat([rutas_mas_valiosas,rutas_populares],axis=1)#.iloc[:54].plot.bar()
resumen_rutas['% valiosas'] = 100 * resumen_rutas['total_value'] / valor_total_hist 
resumen_rutas['% total'] = 100 * resumen_rutas['register_id'] / 19056 
resumen_rutas.loc[:,['% valiosas','% total']].reset_index().sort_values(['% valiosas'],ascending=False).set_index(["origin","destination"]).iloc[:55].plot(kind='bar',title='RUTAS\nmas valiosas VS mas populares')


# In[14]:


data['product'].value_counts()
squarify.plot(sizes=data['product'].value_counts(), label=data['product'].value_counts().index[:-4])
plt.axis('off')
plt.show()


# In[26]:


data['transport_mode'].value_counts(normalize=True).plot(kind='pie',subplots=True,title='Modos de transporte mas populares \n acorde al 100% de rutas realizadas ')


# In[55]:


data.groupby(['company_name'])['total_value'].sum().sort_values(ascending=False)[data.groupby(['company_name'])['total_value'].sum().sort_values(ascending=False).cumsum()<=valor_total_hist*.8]


# In[52]:


data.groupby(['company_name'])['total_value'].sum().sort_values(ascending=False)[data.groupby(['company_name'])['total_value'].sum().sort_values(ascending=False).cumsum()<=valor_total_hist*.8].plot.bar(title="Empresas que aportan el 80% del valor den las rutas")

