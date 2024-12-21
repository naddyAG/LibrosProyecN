from conexion import obtener_conexion
import mysql.connector
from mysql.connector import Error
import streamlit as st
import pandas as pd
# Insertar autor
def insertar_autor(nombre, apellido, seudonimo, genero, fecha_nacimiento, pais_origen):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = """
        INSERT INTO autor (nombre, apellido, seudonimo, genero, fecha_nacimiento, pais_origen)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(consulta, (nombre, apellido, seudonimo, genero, fecha_nacimiento, pais_origen))
    conexion.commit()
    cursor.close()
    conexion.close()
    print("Autor insertado correctamente.")

# Modificar autor
def modificar_autor(id_autor, nombre=None, apellido=None, seudonimo=None, genero=None, fecha_nacimiento=None, pais_origen=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    campos = []
    valores = []

    if nombre:
        campos.append("nombre = %s")
        valores.append(nombre)
    if apellido:
        campos.append("apellido = %s")
        valores.append(apellido)
    if seudonimo:
        campos.append("seudonimo = %s")
        valores.append(seudonimo)
    if genero:
        campos.append("genero = %s")
        valores.append(genero)
    if fecha_nacimiento:
        campos.append("fecha_nacimiento = %s")
        valores.append(fecha_nacimiento)
    if pais_origen:
        campos.append("pais_origen = %s")
        valores.append(pais_origen)

    if campos:
        consulta = f"UPDATE autor SET {', '.join(campos)} WHERE id_autor = %s"
        valores.append(id_autor)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Autor modificado correctamente.")
    else:
        print("No se proporcionaron datos para modificar.")

    cursor.close()
    conexion.close()

# Eliminar autor
def eliminar_autor(id_autor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "DELETE FROM autor WHERE id_autor = %s"
    cursor.execute(consulta, (id_autor,))
    conexion.commit()
    cursor.close()
    conexion.close()
    print("Autor eliminado correctamente.")


# Listar todos los autores
def listar_autores():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT *, concat(nombre,' ', apellido) as nombre_autor FROM autor"
    cursor.execute(consulta)
    autores = cursor.fetchall()
    cursor.close()
    conexion.close()
    return autores

def main_autor():
    st.title(":black_nib: Gestion de Autores")
    menu = ["Ver Autores", "Registrar Autor", "Editar Autor", "Eliminar Autor"]
    opcion = st.sidebar.selectbox("Menú", menu)
    if opcion == "Ver Autores":
        st.subheader("Lista de Autores")
        autores =listar_autores()
        if autores:
            autores= pd.DataFrame(autores)
            st.write(autores)
        else:
            st.info("No hay autores registrados...")
    elif opcion == "Registrar Autor":
        st.subheader("Registrar Nuevo Autor")
        with st.form(key="form_registro_autor"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            seudonimo = st.text_input("Seudónimo (opcional)")
            ## SelecBox
            genero = st.selectbox("Género", ["Masculino", "Femenino"])
            if(genero=="Masculino"):
                genero='M'
            else:
                genero='F'
            fecha_nacimiento = st.date_input("Fecha de Nacimiento")
            pais_origen = st.text_input("País de Origen")
            submit_button = st.form_submit_button("Registrar")

            if submit_button:
                if nombre and apellido:
                    insertar_autor(nombre, apellido, seudonimo, genero, fecha_nacimiento, pais_origen)
                    st.success("Autor registrado exitosamente.")
                else:
                    st.error("Por favor, completa todos los campos obligatorios.")
    elif opcion == "Editar Autor":
        st.subheader("Editar Autor")
        autores = listar_autores()
        autor_ids = [autor["id_autor"] for autor in autores]
        id_autor = st.selectbox("Selecciona un autor para editar", autor_ids)

        autor_seleccionado = next((autor for autor in autores if autor["id_autor"] == id_autor), None)
        if autor_seleccionado:
            with st.form(key="form_edicion_autor"):
                nombre = st.text_input("Nombre", value=autor_seleccionado["nombre"])
                apellido = st.text_input("Apellido", value=autor_seleccionado["apellido"])
                seudonimo = st.text_input("Seudónimo", value=autor_seleccionado["seudonimo"])
                if(autor_seleccionado["genero"]=='M'):
                    autor_seleccionado["genero"]='Masculino'
                else:
                    autor_seleccionado["genero"]='Femenino'
                genero = st.selectbox(
                    "Género",
                    ["Masculino", "Femenino"],
                    index=["Masculino", "Femenino"].index(autor_seleccionado["genero"])
                )
                fecha_nacimiento = st.date_input("Fecha de Nacimiento", value=autor_seleccionado["fecha_nacimiento"])
                pais_origen = st.text_input("País de Origen", value=autor_seleccionado["pais_origen"])
                submit_button = st.form_submit_button("Actualizar")

                if submit_button:
                    if(genero=='Masculino'):
                        genero='M'
                    else:
                        genero='F'
                    modificar_autor(id_autor, nombre, apellido, seudonimo, genero, fecha_nacimiento, pais_origen)
                    st.success("Autor actualizado exitosamente.")
    elif opcion == "Eliminar Autor":
        st.subheader("Eliminar Autor")

        autores = listar_autores()
        st.write(pd.DataFrame(autores))
        autor_ids = [autor["id_autor"] for autor in autores]
        id_autor = st.selectbox("Selecciona un autor para eliminar", autor_ids)

        if st.button("Eliminar"):
            eliminar_autor(id_autor)
            st.success("Autor eliminado exitosamente.")

if __name__=="__main__":
    main_autor()
