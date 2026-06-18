import streamlit as pd
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
