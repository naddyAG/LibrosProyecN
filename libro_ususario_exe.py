from libro_ususariobcp import listar_libros_por_usuario, insertar_libro_usuario

## Proporciona el id_usuario 
id_usuario = input("ID_USUARIO: ")
libros_usuarios = listar_libros_por_usuario(id_usuario)
for libro in libros_usuarios:
    print(libro)

## id_libro e id_usuario para insertar relación libro-usuario
id_libro = input("ID_LIBRO: ")
##id_libro_usuario= input("ID_LIBRO_USUARIO: ")
insertar_libro_usuario(id_libro, id_usuario)