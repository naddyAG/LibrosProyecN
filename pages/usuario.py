from conexion import obtener_conexion
import mysql.connector
from mysql.connector import Error

import streamlit as st
import pandas as pd

# Insertar usuario
def insertar_usuario(nombre, apellido, nombre_usuario, email):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = """
        INSERT INTO usuario (nombre, apellido, nombre_usuario, email)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(consulta, (nombre, apellido, nombre_usuario, email))
    conexion.commit()
    cursor.close()
    conexion.close()
    print("Usuario insertado correctamente.")

# Modificar usuario
def modificar_usuario(id_usuario, nombre=None, apellido=None, nombre_usuario=None, email=None):
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
    if nombre_usuario:
        campos.append("nombre_usuario = %s")
        valores.append(nombre_usuario)
    if email:
        campos.append("email = %s")
        valores.append(email)

    if campos:
        consulta = f"UPDATE usuario SET {', '.join(campos)} WHERE id_usuario = %s"
        valores.append(id_usuario)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Usuario modificado correctamente.")
    else:
        print("No se proporcionaron datos para modificar.")

    cursor.close()
    conexion.close()

# Eliminar usuario
def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "DELETE FROM usuario WHERE id_usuario = %s"
    cursor.execute(consulta, (id_usuario,))
    conexion.commit()
    cursor.close()
    conexion.close()
    print("Usuario eliminado correctamente.")

# Buscar usuarios por nombre de usuario
def buscar_usuarios_por_nombre_usuario(nombre_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT * FROM usuario WHERE nombre_usuario LIKE %s"
    cursor.execute(consulta, (f"%{nombre_usuario}%",))
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return usuarios

# Listar todos los usuarios
def listar_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT * FROM usuario"
    cursor.execute(consulta)
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return usuarios



# Función principal para gestión de usuarios
def main_usuario():
    st.title("Gestión de Usuarios")
    menu = ["Ver Usuarios", "Registrar Usuario", "Editar Usuario", "Eliminar Usuario"]
    opcion = st.sidebar.selectbox("Menú", menu)

    if opcion == "Ver Usuarios":
        st.subheader("Lista de Usuarios")
        usuarios = listar_usuarios()
        if usuarios:
            usuarios = pd.DataFrame(usuarios)
            st.write(usuarios)
        else:
            st.info("No hay usuarios registrados.")

    elif opcion == "Registrar Usuario":
        st.subheader("Registrar Nuevo Usuario")
        with st.form(key="form_registro_usuario"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            nombre_usuario = st.text_input("Nombre de Usuario")
            email = st.text_input("Correo Electrónico")
            submit_button = st.form_submit_button("Registrar")

            if submit_button:
                if nombre and apellido and nombre_usuario and email:
                    insertar_usuario(nombre, apellido, nombre_usuario, email)
                    st.success("Usuario registrado exitosamente.")
                else:
                    st.error("Por favor, completa todos los campos obligatorios.")

    elif opcion == "Editar Usuario":
        st.subheader("Editar Usuario")
        usuarios = listar_usuarios()
        usuario_ids = [usuario["id_usuario"] for usuario in usuarios]
        id_usuario = st.selectbox("Selecciona un usuario para editar", usuario_ids)

        usuario_seleccionado = next((usuario for usuario in usuarios if usuario["id_usuario"] == id_usuario), None)
        if usuario_seleccionado:
            with st.form(key="form_edicion_usuario"):
                nombre = st.text_input("Nombre", value=usuario_seleccionado["nombre"])
                apellido = st.text_input("Apellido", value=usuario_seleccionado["apellido"])
                nombre_usuario = st.text_input("Nombre de Usuario", value=usuario_seleccionado["nombre_usuario"])
                email = st.text_input("Correo Electrónico", value=usuario_seleccionado["email"])
                submit_button = st.form_submit_button("Actualizar")

                if submit_button:
                    modificar_usuario(id_usuario, nombre, apellido, nombre_usuario, email)
                    st.success("Usuario actualizado exitosamente.")

    elif opcion == "Eliminar Usuario":
        st.subheader("Eliminar Usuario")
        usuarios = listar_usuarios()
        usuario_ids = [usuario["id_usuario"] for usuario in usuarios]
        id_usuario = st.selectbox("Selecciona un usuario para eliminar", usuario_ids)

        if st.button("Eliminar"):
            eliminar_usuario(id_usuario)
            st.success("Usuario eliminado exitosamente.")

# Ejecutar la app
if __name__ == "__main__":
    main_usuario()
