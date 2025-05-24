import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SumItUp",    
    page_icon="💰", 
    layout="wide",                 
)

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'Name': [],
        'Kategorie': [],
        'Anzahl': [],
        'Preis': [],
        'Kosten': []
    })

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

st.title("SumItUp...")

def update():
    st.session_state.df = st.session_state.df.drop(table['selection']['rows'][0] if table['selection']['rows'] else "Keine Auswahl")

col1, col2 = st.columns([2, 1])

with col1:

    if not st.session_state.file_uploaded:
        uploaded_file = st.file_uploader("CSV-Datei hochladen", type="csv")
        if uploaded_file is not None:
            try:
                df_upload = pd.read_csv(uploaded_file)
                required_columns = {'Name', 'Kategorie', 'Anzahl', 'Preis'}

                if required_columns.issubset(df_upload.columns):
                    df_upload = df_upload[list(required_columns)]
                    df_upload['Kosten'] = df_upload['Anzahl'] * df_upload['Preis']
                    st.session_state.df = pd.concat([st.session_state.df, df_upload], ignore_index=True)
                    st.session_state.file_uploaded = True
                    st.rerun()
                else:
                    st.error(f"CSV muss die Spalten enthalten: {', '.join(required_columns)}")
            except Exception as e:
                st.error(f"Fehler beim Einlesen der CSV: {e}")        

    if st.session_state.file_uploaded:
        st.success("CSV erfolgreich importiert!")
        st.session_state.file_uploaded = None

    with st.form(key='input_form'):
        name = st.text_input("Was genau?")
        kategorie = st.selectbox("Kategorie", options=['Wohnen', 'Kochen', 'Lebensmittel'], placeholder="Auswählen oder hinzufügen", index= None, accept_new_options=True)
        anzahl = st.number_input("Anzahl", min_value=0, step=1)
        preis = st.number_input("Preis", min_value=0.0, step=0.01, format="%.2f")
        submit_button = st.form_submit_button(label='Hinzufügen')

    if submit_button:
        if name and kategorie and anzahl and preis is not None:
            new_row = pd.DataFrame({
                'Name': [name],
                'Kategorie': [kategorie],
                'Anzahl': [anzahl],
                'Preis': [preis]
            })
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.session_state.df['Kosten'] = st.session_state.df['Anzahl'] * st.session_state.df['Preis']
            st.success(f"Eintrag '{name}' hinzugefügt!")

    st.subheader("Tabelle")
    table = st.dataframe(st.session_state.df, hide_index=True, selection_mode='single-row', on_select="rerun")
    delete_button = st.button(label="Löschen", on_click= update)


with col2:
    st.subheader("Gesammtkosten")
    st.markdown(f"# :rainbow[{st.session_state.df['Kosten'].sum():.2f}] €") # 
    if not st.session_state.df.empty:
        fig = px.pie(
            st.session_state.df,
            values='Kosten',
            names='Kategorie',
            title="Aufteilung nach Kategorie",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig.update_traces(textinfo='label+percent', textposition='inside', pull=0.03)
        fig.update_layout(
            title_x=0.5,
            font=dict(size=14)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Keine Daten für das Diagramm.")
