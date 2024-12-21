from pages.usuario import listar_usuarios,insertar_usuario
usuarios=listar_usuarios()
print (usuarios)

nombre = input("Nombre: ")
apellido = input("Apellido: ")
nombre_usuario = input("Nombre_Usuario: ")
email = input("E-mail: ")
insertar_usuario(nombre, apellido,nombre_usuario,email)