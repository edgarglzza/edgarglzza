#Import everithing I need
import sqlite3
import sqlalchemy
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#____________________________________________________________

#Rescticciónes del programa:
#1.- Registrar nuevos profesores y cursos.
#2.- Un alumno se asigna a un curso.
#3.- Un curso se puede asociar a mas de 1 profesor.
#4.- Los profesores tienen un horario cada que están asignados
#    a un curso
#5.- Horario asocia a un curso y un profesor para 1 día de la 
#    semana (Lu a Do)
#6.- Se puede exportar: alumnos del curso, horario de 
#  y horario del curso

#Conexión a la base de datos
engine = create_engine('sqlite:///BaseDeDatosEscuela.db')
Session = sessionmaker(bind = engine)
session = Session()

#Clases: generación de tablas
Base = sqlalchemy.orm.declarative_base()

class Alumnos(Base):
    __tablename__ = 'alumnos'
    id = Column(
        Integer,
        primary_key = True)
    nombre = Column(String)
    
    cursos = relationship(
        'Curso', 
        secondary = 'inscripcion')

class Profesor(Base):
    __tablename__ = 'profesores'
    id = Column(
        Integer,
        primary_key = True)
    nombre = Column(String)
    horario = Column(String)

class Curso(Base):
    __tablename__ = "cursos"
    id = Column(
        Integer, primary_key = True)
    nombre = Column(String)
    dia= Column(String)
    horario = Column(String)
    profesor_id = Column(Integer, ForeignKey('profesores.id'))

    profesor = relationship('Profesor', backref ='cursos')
    
class Inscripcion(Base):
    __tablename__ = 'inscripcion'
    alumno_id = Column(Integer, ForeignKey('alumnos.id'),
        primary_key = True)
    curso_id  = Column(Integer, ForeignKey('cursos.id'),
    primary_key = True)

class CursoProfesor(Base):
    __tablename__ = 'curso_profesor'
    id = Column(Integer, primary_key = True)
    curso_id = Column(Integer, ForeignKey('cursos.id'))
    profesor_id= Column(Integer,ForeignKey('profesores.id'))

#Creación de la base de datos
Base.metadata.create_all(engine)

#Creación de conexión a sqlite
conn = sqlite3.connect("C:\\Users\Edgar\\Downloads\\SQL COURSERA\\BaseDeDatosEscuela.db") #Ruta de base de datos / Database Route
cursor = conn.cursor()

#Creación de funciones para la formación del sistema

def Inicio():
    print('Bienvenido a tu sistema de inscripción')
    print('¿qué quieres hacer?')
    ent= int(input('1. Registrar nuevos alumnos \n2. Registrar profesor \n3. Registrar curso\n4. Ver mi horario como alumno\n5. Salir\n>> '))
    if ent == 1:
        registrar_alumni()
    elif ent == 2:
        registrar_prof()
    elif ent == 3:
        registrar_curso()
    elif ent == 4:
        descargar_horario()
    elif ent == 5:
        print('¡Nos vemos pronto!')
        exit()
    else:
        print('ingresa un número del 1 al 3 y presiona ENTER')

def registrar_alumni():
    nombre_alumno = input('Ingresa el nombre del alumno:\n>> ')
    add_alumno = Alumnos(nombre = nombre_alumno)
    session.add(add_alumno)
    session.commit()
    print('Alumno registrado...')

    #Muestra lso cursos que están disponibles ahora
    cursos_disponibles = session.query(Curso).all()
    print('Cursos disponibles:')
    for curso in cursos_disponibles:
        print(f'{curso.id}. {curso.nombre}')

    curso_id = int(input('Seleccione el ID del curso al que desea inscribirse:\n>> '))
    
    # Validación del ID del curso
    curso_seleccionado = session.query(Curso).get(curso_id)
    if curso_seleccionado:
        inscripcion = Inscripcion(alumno_id=add_alumno.id, curso_id=curso_id)
        session.add(inscripcion)
        session.commit()
        print(f'El alumno {nombre_alumno} se ha inscrito en el curso {curso_seleccionado.nombre}.')
    else:
        print('El ID del curso seleccionado no existe.')

    Inicio()

def registrar_curso():
    nuevo_curso = input('Ingresa el nombre del curso:\n>> ')
    dia_curso = input('Ingresa el día que se imparte el curso:\n>> ')
    horario_curso = input('Ingresa el horario del curso\n>> ')
    profesor_curso= input('Ingresa el nombre del profesor que imparte el curso:\n>> ')
    
    profesor = session.query(Profesor).filter_by(nombre = profesor_curso).first()

    if profesor:
        add_curso = Curso(nombre= nuevo_curso, horario = horario_curso, dia = dia_curso, profesor = profesor)
        session.add(add_curso)
        session.commit()
        print('Se ha registrado adecuadamente')
    else:
        print('El profesor no existe en los registros')

    Inicio()

def registrar_prof():
    nuevo_prof = input('Ingresa el nombre del profesor:\n>> ')
    horario_prof = input('Ingresa el horario del profesor:\n>> ')
    
    add_profe = Profesor(nombre =nuevo_prof, horario =horario_prof)
    session.add(add_profe)
    session.commit()
    print('Profesor registrado exitosamente.')

    Inicio()

def descargar_horario():
    curso_dwn = input('¿Qué curso quieres descargar?\n>> ')
    curso = session.query(Curso).filter_by(nombre=curso_dwn).first()
    if curso:
        print('Descargando curso de: ', curso.nombre)
        contenido_curso = f"Nombre del curso: {curso.nombre}\nHorario: {curso.horario}\nDía: {curso.dia}\nProfesor: {curso.profesor.nombre}"
        nombre_archivo = f"{curso.nombre}.txt"
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(contenido_curso)
            print(f"El curso '{curso.nombre}' se ha descargado en el archivo '{nombre_archivo}'")

    else:
        print('el curso no existe.')
    Inicio()

Inicio()