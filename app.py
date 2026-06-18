import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

class DataAnalyzer:
    """Clase encargada de procesar, clasificar y generar análisis del dataset."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._preprocesar_datos()

    def _preprocesar_datos(self):
        """Preprocesa los datos, incluyendo la conversión de días a años."""
        # Solución a tu consulta previa: Convertimos la edad de días a años enteros
        if 'age_in_days' in self.df.columns:
            self.df['age_in_years'] = self.df['age_in_days'] // 365.25
            
        # Limpieza rápida para asegurar que los gráficos categóricos se lean bien
        if 'renewal' in self.df.columns:
            self.df['renewal'] = self.df['renewal'].astype(str).str.strip()

    def clasificar_variables(self):
        """Item 2: Clasifica las variables de manera automática en numéricas y categóricas."""
        numericas = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categoricas = self.df.select_dtypes(include=[object, 'category']).columns.tolist()
        return numericas, categoricas

    def obtener_info_buffer(self):
        """Item 1: Captura el output de df.info() para mostrarlo en Streamlit."""
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def obtener_faltantes(self):
        """Item 4: Cuenta valores nulos por columna."""
        df_nulls = pd.DataFrame({
            'Valores Nulos': self.df.isnull().sum(),
            'Porcentaje (%)': (self.df.isnull().sum() / len(self.df)) * 100
        })
        return df_nulls[df_nulls['Valores Nulos'] > 0]

st.set_page_config(page_title="Insurance Analytics App", layout="wide", page_icon="📊")

st.sidebar.image("Logo_IC.png")

st.sidebar.title("🔍 Navegación")
opcion_menu = st.sidebar.radio(
    "Selecciona un Módulo:",
    ["Módulo 1: Home", "Módulo 2: Carga de Datos", "Módulo 3: EDA (Análisis Exploratorio)"]
)

if 'raw_data' not in st.session_state:
    st.session_state['raw_data'] = None


if opcion_menu == "Módulo 1: Home":
    st.title("📊 Aplicación Interactiva para el Análisis de Seguros")
    st.markdown("---")
    
    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        st.subheader("🎯 Objetivo del Proyecto")
        st.write(
            "Esta herramienta analítica tiene como fin explorar y comprender las características "
            "demográficas y de comportamiento de los clientes de una aseguradora. El foco principal "
            "es identificar los patrones asociados con la **renovación de pólizas (columna `renewal`)**."
        )
        
        st.subheader("📋 Sobre el Dataset (InsuranceCompany.csv)")
        st.write(
            "Contiene registros históricos de asegurados, incluyendo variables críticas como ingresos mensuales, "
            "historial de retrasos de pagos en ventanas de tiempo (3, 6 y 12 meses), canal de captación del cliente, "
            "puntuación de evaluación del cliente, monto de la prima y su estatus final de renovación."
        )

    with col_der:
        st.info("👤 **Información del Autor**\n\n"
                "**Nombre:** Alia Ortega Alvarado\n\n"
                "**Especialización:** Python for Analytics\n\n"
                "**Año:** 2026")
        
        st.success("🛠️ **Tecnologías Utilizadas**\n"
                   "- Python \n- Streamlit\n- Pandas & NumPy\n- Matplotlib & Seaborn")

elif opcion_menu == "Módulo 2: Carga de Datos":
    st.title("📂 Gestión e Ingreso de Datos")
    st.markdown("---")
    
    archivo_cargado = st.file_uploader("Sube el archivo CSV del caso de estudio (InsuranceCompany.csv)", type=["csv"])
    
    if archivo_cargado is not None:
        try:
            # Leer el archivo y guardarlo en el session_state
            df_input = pd.read_csv(archivo_cargado)
            st.session_state['raw_data'] = df_input
            st.toast("¡Archivo cargado con éxito!", icon="✅")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            
    # Validar si el archivo ya fue cargado
    if st.session_state['raw_data'] is not None:
        df = st.session_state['raw_data']
        st.success("Dataset activo en la memoria del aplicativo.")
        
        # Mostrar Dimensiones
        col_filas, col_cols = st.columns(2)
        col_filas.metric("Total de Filas (Registros)", df.shape[0])
        col_cols.metric("Total de Columnas (Variables)", df.shape[1])
        
        # Vista previa (Head)
        st.subheader("👀 Vista previa de los datos superiores (Head)")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.warning("⚠️ Por favor, carga un archivo CSV en este módulo para habilitar los análisis del EDA.")

elif opcion_menu == "Módulo 3: EDA (Análisis Exploratorio)":
    st.title("🔬 Core Analítico: Exploración en Profundidad")
    st.markdown("---")
    
    if st.session_state['raw_data'] is None:
        st.error("🛑 Bloqueado: Primero debes cargar el archivo CSV en el **Módulo 2: Carga de Datos**.")
    else:
        # Instanciar nuestra clase POO con los datos cargados
        analizador = DataAnalyzer(st.session_state['raw_data'])
        df_procesado = analizador.df
        num_cols, cat_cols = analizador.clasificar_variables()
        
        # Definición de pestañas (Tabs) para ordenar los 10 ítems exigidos
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 1 a 3: Estructura y Resumen",
            "🔍 4 a 6: Faltantes y Distribución",
            "🔀 7 y 8: Relaciones Bivariadas",
            "🎛️ 9: Filtro Paramétrico",
            "💡 10: Hallazgos Clave"
        ])
        
        # ----------------------------------------------------------------------
        # TAB 1: ÍTEMS 1, 2 Y 3 (Estructura Base)
        # ----------------------------------------------------------------------
        with tab1:
            st.header("Ítem 1: Información General del Dataset")
            col_info_txt, col_info_tabla = st.columns(2)
            with col_info_txt:
                st.text_area("Estructura interna (df.info())", analizador.obtener_info_buffer(), height=250)
            with col_info_tabla:
                st.write("Tipos de datos detectados:")
                st.dataframe(df_procesado.dtypes.astype(str).to_frame(name="Tipo de Dato"), use_container_width=True)
                
            st.markdown("---")
            st.header("Ítem 2: Clasificación de Variables mediante Funciones POO")
            col_c1, col_c2 = st.columns(2)
            col_c1.info(f"**Variables Numéricas ({len(num_cols)}):** \n {', '.join(num_cols)}")
            col_c2.success(f"**Variables Categóricas ({len(cat_cols)}):** \n {', '.join(cat_cols)}")
            
            st.markdown("---")
            st.header("Ítem 3: Estadísticas Descriptivas Globales")
            st.write("Análisis estadístico de tendencia central y dispersión (.describe()):")
            st.dataframe(df_procesado.describe(), use_container_width=True)
            st.caption("💡 Tip analítico: Revisa los valores máximos y mínimos para notar presencia de anomalías.")

        # ----------------------------------------------------------------------
        # TAB 2: ÍTEMS 4, 5 Y 6 (Distribuciones Univariadas)
        # ----------------------------------------------------------------------
        with tab2:
            st.header("Ítem 4: Análisis de Valores Faltantes (Nulos)")
            df_nulos = analizador.obtener_faltantes()
            if not df_nulos.empty:
                st.dataframe(df_nulos, use_container_width=True)
                st.warning("Se detectaron celdas vacías. Esto requiere una estrategia de imputación antes de entrenar modelos.")
            else:
                st.success("🎉 ¡Perfecto! El dataset no contiene registros nulos en ninguna columna.")
                
            st.markdown("---")
            st.header("Ítem 5: Distribución de Variables Numéricas")
            # Widget Selectbox para cambiar el gráfico dinámicamente
            var_num_select = st.selectbox("Elige una variable numérica para ver su histograma:", num_cols, key="item5_select")
            
            fig, ax = plt.subplots(figsize=(7, 3))
            sns.histplot(df_procesado[var_num_select], kde=True, color="skyblue", ax=ax)
            ax.set_title(f"Distribución de la Variable: {var_num_select}")
            st.pyplot(fig)
            st.write(f"**Media:** {df_procesado[var_num_select].mean():.2f} | **Mediana:** {df_procesado[var_num_select].median():.2f}")
            
            st.markdown("---")
            st.header("Ítem 6: Análisis de Variables Categóricas")
            var_cat_select = st.selectbox("Elige una variable categórica para analizar:", cat_cols, key="item6_select")
            col_g1, col_g2 = st.columns([1, 2])
            with col_g1:
                conteo_cat = df_procesado[var_cat_select].value_counts()
                proporcion_cat = df_procesado[var_cat_select].value_counts(normalize=True) * 100
                resumen_cat = pd.DataFrame({"Frecuencia": conteo_cat, "Porcentaje (%)":
                                            proporcion_cat})
                st.dataframe(resumen_cat, use_container_width=True)
            with col_g2:
                fig2, ax2 = plt.subplots(figsize=(6, 3))
                sns.countplot(data=df_procesado, x=var_cat_select, palette="Set2", ax=ax2)
                st.pyplot(fig2)

        # ----------------------------------------------------------------------
        # TAB 2: ÍTEMS 4, 5 Y 6 (Distribuciones Univariadas)
        # ----------------------------------------------------------------------
        with tab3:
            st.header("Ítem 7: Análisis Bivariado (Numérico vs Categórico Target)")
            st.write("Comportamiento de métricas cuantitativas segmentadas por si el cliente renovó o no (renewal).")
            col_analisis_biv = 'age_in_years' if 'age_in_years' in df_procesado.columns else
            num_cols[0]
            var_biv_num = st.selectbox("Selecciona la métrica numérica:", num_cols +
            (['age_in_years'] if 'age_in_years' in df_procesado.columns else []), index=len(num_cols)
            if 'age_in_years' in df_procesado.columns else 0)
            
            if 'renewal' in df_procesado.columns:
            fig3, ax3 = plt.subplots(figsize=(7, 3.5))
            sns.boxplot(data=df_procesado, x='renewal', y=var_biv_num, palette="PRGn", ax=ax3)
            ax3.set_title(f"Diagrama de Caja de {var_biv_num} según Renovación")
            st.pyplot(fig3)

            else:
            st.error("No se encontró la columna objetivo 'renewal' en tus datos para realizar esta
            segmentación.")
            
            
                

