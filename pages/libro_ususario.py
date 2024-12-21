import mysql.connector
from mysql.connector import Error
from conexion import obtener_conexion
import streamlit as st
import pandas as pd
#from libro import listar_libros
from pages.usuario import *
from pages.libro import *

# Relacionar libro con usuario
def insertar_libro_usuario(id_libro, id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = """
        INSERT INTO libro_usuario (id_libro, id_usuario)
        VALUES (%s, %s)
    """
    cursor.execute(consulta, (id_libro, id_usuario))
    conexion.commit()
    cursor.close()
    conexion.close()
    print("Relación libro-usuario insertada correctamente.")

# Eliminar relación libro-usuario
def eliminar_libro_usuario(id_libro_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "DELETE FROM libro_usuario WHERE id_libro_usuario = %s"
    cursor.execute(consulta, (id_libro_usuario,))
    conexion.commit()
    cursor.close()
    conexion.close()
    print("Relación libro-usuario eliminada correctamente.")

# Listar todos los libros asociados a un usuario
def listar_libros_por_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    consulta = """
        SELECT l.id AS id_libro, l.titulo, l.fechaPublicacion, l.ventas
        FROM libro_usuario lu
        INNER JOIN libro l ON lu.id_libro = l.id
        WHERE lu.id_usuario = %s
    """
    cursor.execute(consulta, (id_usuario,))
    libros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return libros

# Listar todos los usuarios asociados a un libro
def listar_usuarios_por_libro(id_libro):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    consulta = """
        SELECT u.id_usuario, u.nombre, u.apellido, u.nombre_usuario, u.email
        FROM libro_usuario lu
        INNER JOIN usuario u ON lu.id_usuario = u.id_usuario
        WHERE lu.id_libro = %s
    """
    cursor.execute(consulta, (id_libro,))
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return usuarios


def listar_usuarios_libro():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    consulta = """
        SELECT lu.id_libro_usuario, u.nombre, u.apellido, u.nombre_usuario, u.email,
        l.titulo, concat(a.nombre,' ',a.apellido) as autor
        FROM libro_usuario lu
        INNER JOIN usuario u ON lu.id_usuario = u.id_usuario
        INNER JOIN libro l on l.id_libro = lu.id_libro
        INNER JOIN autor a on l.id_autor =a.id_autor
      
    """
    cursor.execute(consulta)
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return usuarios



def main_libro_usuario():
    st.title("Gestión de Venta")
    menu = ["Ver Relación", "Registrar Relación", "Eliminar Relación"]
    opcion = st.sidebar.selectbox("Menú", menu)

    if opcion == "Ver Relación":
        st.subheader("Lista de Relaciones (Libro-Usuario)")
        relaciones = listar_usuarios_libro()
        if relaciones:
            relaciones = pd.DataFrame(relaciones)
            st.write(relaciones)
        else:
            st.info("No hay relaciones registradas entre libros y usuarios.")

    elif opcion == "Registrar Relación":
        st.subheader("Registrar Nueva Relación")
        with st.form(key="form_registro_relacion"):
            # Obtener libros
            libros = listar_libros()
            opciones_libros = {libro['titulo']: libro['id_libro'] for libro in libros}
            libro_seleccionado = st.selectbox("Libro", options=list(opciones_libros.keys()))
            id_libro = opciones_libros[libro_seleccionado]

            # Obtener usuarios
            usuarios = listar_usuarios()
            opciones_usuarios = {usuario['nombre_usuario']: usuario['id_usuario'] for usuario in usuarios}
            usuario_seleccionado = st.selectbox("Usuario", options=list(opciones_usuarios.keys()))
            id_usuario = opciones_usuarios[usuario_seleccionado]

            submit_button = st.form_submit_button("Registrar")

            if submit_button:
                if id_libro and id_usuario:
                    insertar_libro_usuario(id_libro, id_usuario)
                    st.success("Relación registrada exitosamente.")
                else:
                    st.error("Por favor, selecciona tanto un libro como un usuario.")

    elif opcion == "Eliminar Relación":
        st.subheader("Eliminar Relación")

        # Obtener las relaciones actuales
        relaciones = listar_usuarios_libro()  # Asegúrate de que esta función devuelve una lista con columnas descriptivas.
        if relaciones:
            # Convertir a DataFrame para mostrar la tabla en Streamlit
            relaciones_df = pd.DataFrame(relaciones)
            st.write("Relaciones registradas entre libros y usuarios:")
            st.dataframe(relaciones_df)

            # Crear una lista descriptiva para facilitar la selección
            opciones_relaciones = {
                f"{relacion['titulo']} - {relacion['nombre_usuario']}": relacion['id_libro_usuario']
                for relacion in relaciones
            }

            # Desplegable para seleccionar una relación por su descripción
            relacion_seleccionada = st.selectbox(
                "Selecciona una relación para eliminar",
                options=list(opciones_relaciones.keys())
            )

            # Obtener el ID de la relación seleccionada
            id_libro_usuario = opciones_relaciones[relacion_seleccionada]
            print(id_libro_usuario)
            # Botón para confirmar eliminación
            if st.button("Eliminar Relación"):
                eliminar_libro_usuario(id_libro_usuario)  # Llama a la función para eliminar
                st.success(f"La relación '{relacion_seleccionada}' ha sido eliminada exitosamente.")
        else:
            st.info("No hay relaciones registradas entre libros y usuarios.")
# Ejecutar la app
if __name__ == "__main__":
    main_libro_usuario()
