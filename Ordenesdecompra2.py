import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Órdenes sin Compra de Terceros", layout="wide")

st.title("📊 Órdenes sin Orden de Compra de Terceros")

uploaded_file = st.file_uploader("📂 Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Limpiar las columnas
    df.columns = df.columns.str.replace(r'^="|"$', '', regex=True)
    df = df.applymap(lambda x: str(x).strip('="') if isinstance(x, str) else x)

    # Identificar órdenes sin "Orden de Compra de Terceros"
    order_summary = df.groupby("Order")["Transaction Type"].apply(lambda x: "Orden de Compra Terceros" in x.values)
    df_no_purchase = order_summary[order_summary == False].index
    df_filtered = df[df["Order"].isin(df_no_purchase)]

    # Excluir Ultratug Chile S.A.
    df_filtered = df_filtered[df_filtered["Resource Owner"] != "Ultratug Chile S.A."]

    # Agrupar resultados
    df_grouped = df_filtered.groupby("Order")[["Resource", "Resource Owner"]].agg(list).reset_index()
    df_grouped["Resource"] = df_grouped["Resource"].apply(lambda x: ", ".join(set(x)))
    df_grouped["Resource Owner"] = df_grouped["Resource Owner"].apply(lambda x: ", ".join(set(x)))

    st.write("### 📋 Resultados Filtrados")
    st.dataframe(df_grouped, use_container_width=True)

    st.success(f"🔍 Se encontraron {len(df_grouped)} órdenes sin compra de terceros.")

# Instrucciones de uso en la app
st.markdown("### ℹ️ Instrucciones de Uso")
st.markdown("1️⃣ Sube un archivo CSV con los datos de órdenes.")
st.markdown("2️⃣ El sistema filtrará automáticamente las órdenes sin 'Orden de Compra de Terceros'.")
st.markdown("3️⃣ Se excluirán las órdenes de 'Ultratug Chile S.A.'.")
st.markdown("4️⃣ Los resultados se mostrarán en una tabla interactiva.")

st.markdown("---")
st.markdown("📌 **Desarrollado por [Tu Empresa]**")
