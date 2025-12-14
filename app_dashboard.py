import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Dashboard Produk Interaktif", layout="wide")

# English Translation for Product Categories
CATEGORY_TRANSLATION = {
    'beleza_saude': 'Health & Beauty',
    'informatica_acessorios': 'Computer Accessories',
    'automotivo': 'Automotive',
    'cama_mesa_banho': 'Bed Bath Table',
    'moveis_decoracao': 'Furniture & Decor',
    'esporte_lazer': 'Sports & Leisure',
    'perfumaria': 'Perfumery',
    'utilidades_domesticas': 'Housewares',
    'telefonia': 'Mobile Telephony',
    'relogios_presentes': 'Watches & Gifts',
    'alimentos_bebidas': 'Food & Drinks',
    'bebes': 'Baby Products',
    'papelaria': 'Stationery',
    'tablets_impressao_imagem': 'Tablets & Image Printing',
    'brinquedos': 'Toys',
    'telefonia_fixa': 'Fixed Telephony',
    'ferramentas_jardim': 'Garden Tools',
    'fashion_bolsas_e_acessorios': 'Fashion Bags & Accessories',
    'eletroportateis': 'Small Appliances',
    'consoles_games': 'Consoles & Games',
    'audio': 'Audio & Music',
    'fashion_calcados': 'Fashion Shoes',
    'cool_stuff': 'Cool Stuff',
    'malas_acessorios': 'Luggage & Accessories',
    'climatizacao': 'Air Conditioning',
    'construcao_ferramentas_construcao': 'Construction Tools',
    'moveis_cozinha_area_de_servico_jantar_e_jardim': 'Kitchen Dining Garden Furniture',
    'construcao_ferramentas_jardim': 'Garden Construction Tools',
    'fashion_roupa_masculina': 'Men Fashion Clothing',
    'pet_shop': 'Pet Shop',
    'moveis_escritorio': 'Office Furniture',
    'market_place': 'Marketplace',
    'eletronicos': 'Electronics',
    'eletrodomesticos': 'Home Appliances',
    'artigos_de_festas': 'Party Supplies',
    'casa_conforto': 'Home Comfort',
    'construcao_ferramentas_ferramentas': 'Construction Tools',
    'agro_industria_e_comercio': 'Agro Industry & Commerce',
    'moveis_colchao_e_estofado': 'Furniture Mattress & Upholstery',
    'livros_tecnicos': 'Technical Books',
    'casa_construcao': 'Home Construction',
    'instrumentos_musicais': 'Musical Instruments',
    'moveis_sala': 'Living Room Furniture',
    'construcao_ferramentas_iluminacao': 'Construction Lighting Tools',
    'industria_comercio_e_negocios': 'Industry Commerce & Business',
    'alimentos': 'Food',
    'artes': 'Arts & Crafts',
    'moveis_quarto': 'Bedroom Furniture',
    'livros_interesse_geral': 'General Interest Books',
    'construcao_ferramentas_seguranca': 'Safety Construction Tools',
    'fashion_underwear_e_moda_praia': 'Underwear & Beachwear',
    'fashion_esporte': 'Sport Fashion',
    'sinalizacao_e_seguranca': 'Signaling & Security',
    'pcs': 'Personal Computers',
    'artigos_de_natal': 'Christmas Supplies',
    'fashion_roupa_feminina': 'Women Fashion Clothing',
    'eletrodomesticos_2': 'Home Appliances 2',
    'livros_importados': 'Imported Books',
    'bebidas': 'Beverages',
    'cine_foto': 'Photography & Film',
    'la_cuisine': 'Kitchen Equipment',
    'musica': 'Music',
    'casa_conforto_2': 'Home Comfort 2',
    'portateis_casa_forno_e_cafe': 'Small Appliances Home Oven & Coffee',
    'cds_dvds_musicais': 'CDs & DVDs Music',
    'dvds_blu_ray': 'DVDs & Blu-ray',
    'flores': 'Flowers',
    'artes_e_artesanato': 'Arts & Craftsmanship',
    'fraldas_higiene': 'Diapers & Hygiene',
    'fashion_roupa_infanto_juvenil': 'Children Fashion Clothing',
    'seguros_e_servicos': 'Insurance & Services'
}

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('cleaned_products_data.csv')
        # Terjemahkan kategori ke Bahasa Indonesia
        if 'product_category_name' in data.columns:
            data['product_category_name_translated'] = data['product_category_name'].map(
                CATEGORY_TRANSLATION
            ).fillna(data['product_category_name'])
        return data
    except FileNotFoundError:
        st.error("File 'cleaned_products_data.csv' tidak ditemukan.")
        return None

st.title("📊 Interactive Product Dashboard")
st.markdown("In-depth analysis of product categories, attributes, and data correlations")

data = load_data()

if data is None:
    st.stop()

data.columns = [c.strip() for c in data.columns]

st.sidebar.header("🔍 Filter Data")

total_products = len(data)
total_categories = data['product_category_name'].nunique() if 'product_category_name' in data.columns else 0

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("📦 Total Products", total_products)
with col2:
    st.metric("📂 Total Categories", total_categories)

if 'product_category_name_translated' in data.columns:
    categories = sorted(data['product_category_name_translated'].dropna().unique().tolist())
    selected_categories_translated = st.sidebar.multiselect(
        "Select Product Categories",
        options=categories,
        default=categories[:5] if len(categories) > 5 else categories
    )
    # Map translated names back to original names for filtering
    selected_categories = data[data['product_category_name_translated'].isin(selected_categories_translated)]['product_category_name'].unique().tolist()
else:
    selected_categories_translated = None
    selected_categories = None

filtered_data = data.copy()
if selected_categories and 'product_category_name' in data.columns:
    filtered_data = filtered_data[filtered_data['product_category_name'].isin(selected_categories)]

if 'product_weight_g' in data.columns:
    min_weight = float(data['product_weight_g'].min())
    max_weight = float(data['product_weight_g'].max())
    weight_range = st.sidebar.slider(
        "Product Weight Range (g)",
        min_value=min_weight,
        max_value=max_weight,
        value=(min_weight, max_weight)
    )
    filtered_data = filtered_data[
        (filtered_data['product_weight_g'] >= weight_range[0]) &
        (filtered_data['product_weight_g'] <= weight_range[1])
    ]

if 'product_photos_qty' in data.columns:
    min_photos = int(data['product_photos_qty'].min())
    max_photos = int(data['product_photos_qty'].max())
    photos_range = st.sidebar.slider(
        "Product Photos Range",
        min_value=min_photos,
        max_value=max_photos,
        value=(min_photos, max_photos)
    )
    filtered_data = filtered_data[
        (filtered_data['product_photos_qty'] >= photos_range[0]) &
        (filtered_data['product_photos_qty'] <= photos_range[1])
    ]

st.sidebar.markdown("---")
st.sidebar.info("📌 Use filters above to customize dashboard view according to your needs.")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Category Analysis", "🔗 Correlation", "📋 Data Table"])

with tab1:
    st.subheader("Selected Data Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Products (Filtered)", len(filtered_data))
    with col2:
        if 'product_weight_g' in filtered_data.columns:
            st.metric("Avg Weight (g)", f"{filtered_data['product_weight_g'].mean():.2f}")
    with col3:
        if 'product_photos_qty' in filtered_data.columns:
            st.metric("Avg Photos", f"{filtered_data['product_photos_qty'].mean():.2f}")
    with col4:
        if 'product_category_name' in filtered_data.columns:
            st.metric("Selected Categories", len(filtered_data['product_category_name'].unique()))
    
    st.markdown("---")
    
    with st.expander("👀 Preview Data (First 10 Rows)", expanded=False):
        st.dataframe(filtered_data.head(10), use_container_width=True)

with tab2:
    st.header("📊 Product Category Analysis")
    st.subheader("Top 10 Product Categories")
    
    if 'product_category_name_translated' in data.columns:

        category_counts = filtered_data['product_category_name_translated'].value_counts().head(10)
        
        fig = px.bar(
            x=category_counts.index,
            y=category_counts.values,
            labels={'x': 'Category', 'y': 'Number of Products'},    
            color=category_counts.values,
            color_continuous_scale='Viridis',
            title=f"Top 10 Product Categories"
            
        )
        fig.update_layout(xaxis_tickangle=45, height=500, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("📌 Category Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            most_common = filtered_data['product_category_name_translated'].value_counts().index[0]
            most_common_count = filtered_data['product_category_name_translated'].value_counts().values[0]
            st.info(f"**Most Products:** {most_common} ({most_common_count} products)")
        
        with col2:
            least_common = filtered_data['product_category_name_translated'].value_counts().index[-1]
            least_common_count = filtered_data['product_category_name_translated'].value_counts().values[-1]
            st.info(f"**Least Products:** {least_common} ({least_common_count} products)")

with tab3:
    st.subheader("🔗 Product Attribute Correlation Analysis")
    
    numeric_cols = filtered_data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        st.write("**Numeric Attribute Correlation Heatmap**")
        corr_matrix = filtered_data[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
        ax.set_title('Product Attribute Correlation Matrix', fontsize=14, fontweight='bold')
        st.pyplot(fig, use_container_width=True)
        
        st.write("**Scatter Plot**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_axis = st.selectbox("Select X Axis", numeric_cols, index=0)
        with col2:
            y_axis = st.selectbox("Select Y Axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        with col3:
            color_options = ['None']
            if 'product_category_name_translated' in filtered_data.columns:
                color_options.append('product_category_name_translated')
            color_col = st.selectbox("Select Color (Optional)", color_options)
        
        color_col = color_col if color_col != 'None' else None
        size_col = 'product_photos_qty' if 'product_photos_qty' in filtered_data.columns else None
        
        scatter_fig = px.scatter(
            filtered_data,
            x=x_axis,
            y=y_axis,
            color=color_col,
            size=size_col,
            title=f"Relationship between {x_axis} and {y_axis}"
        )
        st.plotly_chart(scatter_fig, use_container_width=True)
    else:
        st.warning("Not enough numeric columns for correlation analysis.")

with tab4:
    st.subheader("📋 Complete Data Table")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name='filtered_products_data.csv',
            mime='text/csv'
        )
    
    with col2:
        try:
            import openpyxl
            buffer = io.BytesIO()
            filtered_data.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label="📥 Download Excel",
                data=buffer,
                file_name='filtered_products_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except ImportError:
            st.info("💡 To download Excel, install: pip install openpyxl")
    
    with col3:
        st.write(f"**Total Rows:** {len(filtered_data)}")
    
    st.markdown("---")
    
    st.dataframe(filtered_data, use_container_width=True, height=600)

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p style='color: gray; font-size: 12px;'>
        Interactive Product Analysis Dashboard | Built with Streamlit 🚀
    </p>
</div>
""", unsafe_allow_html=True)
