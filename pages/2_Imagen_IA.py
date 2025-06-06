st.subheader("🖼️ Resultado(s):")
for i, image_info in enumerate(response["data"]):
    img_url = image_info["url"]
    st.image(img_url, caption=f"Imagen {i+1}", use_column_width=True)
    st.markdown(f"[🔗 Ver imagen en nueva pestaña]({img_url})", unsafe_allow_html=True)

    # Descargar como PNG y JPG
    try:
        import requests
        from PIL import Image
        from io import BytesIO

        # Descargar imagen
        response_img = requests.get(img_url)
        img_bytes = BytesIO(response_img.content)

        # Convertir a formato PIL
        img = Image.open(img_bytes)

        # Preparar descarga PNG
        png_buffer = BytesIO()
        img.save(png_buffer, format="PNG")
        st.download_button(
            label="⬇️ Descargar como PNG",
            data=png_buffer.getvalue(),
            file_name=f"imagen_{i+1}.png",
            mime="image/png"
        )

        # Preparar descarga JPG
        jpg_buffer = BytesIO()
        img.convert("RGB").save(jpg_buffer, format="JPEG")
        st.download_button(
            label="⬇️ Descargar como JPG",
            data=jpg_buffer.getvalue(),
            file_name=f"imagen_{i+1}.jpg",
            mime="image/jpeg"
        )

    except Exception as e:
        st.warning(f"No se pudieron generar botones de descarga: {e}")

    # Registrar en Google Sheets
    if sheet:
        ahora = datetime.now()
        fila = [
            usuario,
            ahora.strftime("%Y-%m-%d"),
            ahora.strftime("%H:%M:%S"),
            prompt,
            resolution,
            img_url
        ]
        sheet.append_row(fila)


