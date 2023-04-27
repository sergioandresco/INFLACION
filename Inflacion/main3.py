#Se debe tener instalado estas 2 librerias
#En caso de no tener instalado las librerias, puede instalarlas con los siguientes comandos:
#pip install pandas
#pip install matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Cargar archivo CSV que esta dentro de la carpeta del proyecto
df = pd.read_csv('datos_productos.csv')

# Convertir 'ano' y 'mes' a formato fecha
df['fecha'] = pd.to_datetime(df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-01', format='%Y-%m-%d')

# Calcular inflación mensual y anual por producto
df['inflacion_mensual'] = df.groupby('producto')['precio'].pct_change() * 100
df['inflacion_anual'] = df.groupby(['producto', df['fecha'].dt.year])['precio'].pct_change(periods=11) * 100

# Crear figura y subgráficos
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

# Graficar inflación mensual en el primer subgráfico
for producto in df['producto'].unique():
    df_producto = df[df['producto'] == producto]
    ax1.plot(df_producto['fecha'], df_producto['inflacion_mensual'], label=producto)

ax1.set_xlabel('Fecha')
ax1.set_ylabel('Inflación (%)')
ax1.set_title('Inflación mensual de productos')
ax1.legend()

# Graficar inflación anual en el segundo subgráfico
for producto in df['producto'].unique():
    df_producto = df[df['producto'] == producto]
    ax2.bar(df_producto['fecha'].dt.year.unique(), df_producto.groupby(df['fecha'].dt.year)['inflacion_anual'].mean(), label=producto)

ax2.set_xlabel('Año')
ax2.set_ylabel('Inflación (%)')
ax2.set_title('Inflación anual de productos')
ax2.legend()

# Crear gráfico de cajas en el tercer subgráfico
ax3.boxplot([df[df['producto'] == producto]['precio'] for producto in df['producto'].unique()])
ax3.set_xticklabels(df['producto'].unique())
ax3.set_xlabel('Producto')
ax3.set_ylabel('Precio')
ax3.set_title('Distribución de precios por producto')

# Ajustar espacio entre subgráficos y mostrar figura
fig.subplots_adjust(hspace=0.5)
plt.show()
