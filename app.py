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
        st.info("👤 **Información del Autor**\n"
                "**Nombre:** Alia Ortega Alvarado\n"
                "**Especialización:** Python for Analytics\n"
                "**Año:** 2026")
        
        st.success("🛠️ **Tecnologías Utilizadas**\n"
                   "- Python \n- Streamlit\n- Pandas & NumPy\n- Matplotlib & Seaborn")
