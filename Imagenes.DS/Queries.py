from io import BytesIO
from matplotlib import pyplot as plt
import psycopg2
from PIL import Image

#Conexión con la base de datos
def create_connection():
    conn = psycopg2.connect(dbname='myDB', user='postgres', password='admin',
                            host='localhost', port='5432')
    curr = conn.cursor()
    return conn, curr

#Inserta un registro en la tabla imagen
def INSERT(clave, file_path, descripcion):
    try:
        imagen = open(file_path, 'rb').read()
        conn, cursor = create_connection()
        try:
            cursor.execute("INSERT INTO imagen "
                           "(clave, descripcion, imagen) "
                           "VALUES(%s,%s,%s)",
                           (clave, descripcion, psycopg2.Binary(imagen)))
            conn.commit()
            print("\n**Registro guardado**\n")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting data in imagen table", error)
        finally:
            conn.close()
    finally:
        pass

#Recupera y muestra la imagen de la db junto con descripción
def SELECT(clave):
    try:
        conn, cursor = create_connection()
        try:
            cursor.execute("SELECT descripcion, imagen FROM imagen WHERE clave=%s", (clave,))
            result = cursor.fetchone()
            if result:
                image = Image.open(BytesIO(result[1]))
                plt.imshow(image)
                plt.show()
                return result[0]
            else:
                print("Image not found.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while selecting data in imagen table", error)
        finally:
            conn.close()
    finally:
        pass



if __name__ == "__main__":
    print("Programa principal")
    opcion = int(input("1. Insertar\n2. Leer\nDigite la opcion: "))
    if opcion == 1:
        file_path = input("Escriba la ruta de la imagen: ")
        descripcion = input("Escriba la descripcion de la imagen: ")
        clave = input("Digite la clave de la imagen: ")
        INSERT(clave, file_path, descripcion)
    if opcion == 2:
        clave = input("Digite la clave: ")
        SELECT(clave)