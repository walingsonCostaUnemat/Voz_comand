import streamlit as st
import pytesseract
import pdfplumber
from PIL import Image
import docx2txt
import speech_recognition as sr

st.set_page_config(page_title="Extrator de Texto", page_icon=":books:")
st.title("Extrator de Texto")

st.sidebar.title("Opções")
file_format = st.sidebar.selectbox("Selecione o formato do arquivo", ("PDF", "Imagem", "Word"))

if file_format == "PDF":
    uploaded_file = st.file_uploader("Carregue o arquivo em PDF", type="pdf")
    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            pages = pdf.pages
            text = ""
            for page in pages:
                text += page.extract_text()

elif file_format == "Imagem":
    uploaded_file = st.file_uploader("Carregue o arquivo em imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        text = pytesseract.image_to_string(img)

elif file_format == "Word":
    uploaded_file = st.file_uploader("Carregue o arquivo em Word", type=["docx"])
    if uploaded_file is not None:
        text = docx2txt.process(uploaded_file)

if uploaded_file is not None:
    st.write(text)

    if st.button("Extrair texto por comando de voz"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Fale o comando de voz:")
            audio = r.listen(source)
        try:
            voice_command = r.recognize_google(audio, language="pt-BR")
            if "exibir" in voice_command.lower() or "mostrar" in voice_command.lower():
                st.write(text)
            if "download" in voice_command.lower() or "baixar" in voice_command.lower():
                st.download_button(
                    label="Baixar texto",
                    data=text,
                    file_name="texto_extraido.txt",
                    mime="text/plain"
                )
        except sr.UnknownValueError:
            st.write("Comando de voz não reconhecido")
        except sr.RequestError as e:
            st.write(f"Erro ao processar o comando de voz: {e}")
