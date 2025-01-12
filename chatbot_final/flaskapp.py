from flask import Flask, render_template, request,session, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error
import bcrypt
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Carpeta para almacenar archivos cargados
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'chatbot_db'
}

# Conectar a la base de datos MySQL
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Pila para almacenar las interacciones
interacciones_pila = []

@app.route('/')
def index():
    mensaje_bienvenida = "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?"
    opciones = [
        "1. Costos",
        "2. Modalidades",
        "3. Niveles de Inglés",
        "4. Cursos y Programas",
        "5. Requisitos de Inscripción",
        "6. Registro para ser contactado por un asesor"
    ]
    ##return render_template('index.html', respuesta=mensaje_bienvenida, opciones=opciones)
    session.clear()  # Limpia el estado de la sesión
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
   
    
    # Recuperar el estado actual de la conversación
    if 'state' not in session:
        session['state'] = 'inicio'
    if 'interacciones_pila' not in session:
        session['interacciones_pila'] = []

    state = session['state']

    # Lógica del chatbot
    if state == 'inicio':
        session['state'] = 'menu'
        respuesta = """¡Hola! ¿En qué puedo ayudarte?<br>
                            1. Costos<br>
                            2. Modalidades<br>
                            3. Niveles de inglés<br>
                            4. Cursos y Programas<br>
                            5. Requisitos de Inscripción<br>
                            6. Registro para ser contactado por un asesor<br>
                            7. Salir<br>
                            Por favor escriba un Número."""
        interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
        return jsonify({'respuesta': respuesta})

    elif state == 'menu':
        if user_input == '1':
            session['state'] = 'costos'
            respuesta = """Nuestros costos son:<br>
                                1. Curso regular: $120/mes<br>
                                2. Curso intensivo: $150/mes<br>
                                ¿Te interesa más información? (1. Sí, 2. No)"""
            interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
            return jsonify({'respuesta': respuesta})
    
        elif user_input == '2':
            session['state'] = 'modalidades'
            respuesta = """Ofrecemos estas modalidades:<br>
                            1. Presencial<br>
                            2. En línea<br>
                            ¿Te interesa más información? (1. Sí, 2. No)"""
            interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
            return jsonify({'respuesta': respuesta})
            
        elif user_input == '3':
            session['state'] = 'niveles'
            respuesta = """Ofrecemos los siguientes niveles:<br>
                            1. Básico<br>
                            2. Intermedio<br>
                            3. Avanzado<br>
                            ¿Te interesa más información? (1. Sí, 2. No)"""
            interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
            return jsonify({'respuesta': respuesta})
            
        elif user_input == '4':
            session['state'] = 'cursos'
            respuesta = """Tenemos los siguientes programas:<br>
                            1. Inglés general<br>
                            2. Inglés para negocios<br>
                            3. Preparación para exámenes internacionales<br>
                            ¿Te interesa más información? (1. Sí, 2. No)"""
            interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
            return jsonify({'respuesta': respuesta})
            
        elif user_input == '5':
            session['state'] = 'requisitos'
            respuesta = """Para inscribirte, necesitas:<br>
                            1. Identificación oficial<br>
                            2. Comprobante de domicilio<br>
                            3. Pago de inscripción<br>
                            ¿Deseas inscribirte deja tus datos para que te contacte un asesor? (1. Sí, 2. No)"""
            interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
            return jsonify({'respuesta': respuesta})
            
        elif user_input == '6':
           respuesta = render_template('registro.html')
           session.clear()  # Limpiar la sesión al finalizar
           return jsonify({'respuesta': respuesta})
        elif user_input == '7':
            respuesta = """"""
            session.clear()
            return jsonify({'respuesta': respuesta})
        else:
            return jsonify({'respuesta': """Opción no válida. Por favor, elige una opción del menú.<br>
                            1. Costos<br>
                            2. Modalidades<br>
                            3. Niveles de inglés<br>
                            4. Cursos y Programas<br>
                            5. Requisitos de Inscripción<br>
                            6. Registro para ser contactado por un asesor<br>
                            7. Salir<br>"""})

    elif state == 'costos':
        if user_input == '1':  # Si el usuario quiere más información
            session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = """El costo incluye materiales y acceso a una plataforma en línea.<br>
                                            Volviendo al menú...<br><br>
                                            ¡Hola de nuevo! ¿En qué más te puedo ayudar? Por favor, elige una opción del menú.<br>
                                            1. Costos<br>
                                            2. Modalidades<br>
                                            3. Niveles de inglés<br>
                                            4. Cursos y Programas<br>
                                            5. Requisitos de Inscripción<br>
                                            6. Registro para ser contactado por un asesor<br>
                                            7. Salir"""
            return jsonify({'respuesta': respuesta})
            
        elif user_input == '2':  # Si el usuario no quiere más información
            respuesta = "Entendido. ¡Gracias por Utilizar el Asistente Virtual!"
            session.clear()
        else:  # Entrada no válida
            respuesta = "Por favor, selecciona 1 o 2."

        interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
        return jsonify({'respuesta': respuesta})

    elif state == 'modalidades':
        if user_input == '1':  # Si el usuario quiere más información
            ##session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = respuesta = """
                        ¡Claro! Aquí tienes más información sobre nuestras modalidades:<br><br>

                        <b>Presencial:</b><br>
                        <ul>
                        <li>Ubicación o sucursales disponibles: Contamos con sucursales en Toluca, en la calle X.</li>
                        <li>Horarios de clases: Ofrecemos los siguientes horarios: turno matutino y sabatino de 7 am a 2 pm.</li>
                        <li>Tamaño de los grupos: Nuestras clases son de grupos reducidos, con un promedio de 10 a 15 estudiantes.</li>
                        <li>Características de las instalaciones: Salones equipados con tecnología moderna, áreas de estudio y recursos adicionales para el aprendizaje.</li>
                        </ul><br>

                        <b>En línea:</b><br>
                        <ul>
                        <li>Herramientas utilizadas: Usamos plataformas como Zoom, Google Meet y nuestro exclusivo sistema LMS.</li>
                        <li>Flexibilidad de horarios: Acceso a clases grabadas y opciones asincrónicas para estudiar a tu ritmo. Turno matutinos y sabatinos de 7 am a 2 pm.</li>
                        <li>Recursos adicionales: Incluye material descargable, grabaciones de las clases, foros de discusión y soporte técnico.</li>
                        <li>Requisitos técnicos: Necesitarás conexión estable a Internet, un dispositivo compatible y, en algunos casos, software específico proporcionado por nosotros.</li>
                         </ul><br><br>
                        Si deseas regresar al menú escribe menu o 2 para salir.<br>"""
            return jsonify({'respuesta': respuesta})
            
        elif user_input == 'menu':  # Si el usuario no quiere más información
            session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = """Volviendo al menú...<br><br>
                            ¡Hola de nuevo! ¿En qué más te puedo ayudar? Por favor, elige una opción del menú.<br>
                            1. Costos<br>
                            2. Modalidades<br>
                            3. Niveles de inglés<br>
                            4. Cursos y Programas<br>
                            5. Requisitos de Inscripción<br>
                            6. Registro para ser contactado por un asesor<br>
                            7. Salir"""

        elif user_input == '2':  # Si el usuario no quiere más información
            respuesta = "Entendido. ¡Gracias por Utilizar el Asistente Virtual!"
            session.clear()
           
        else:  # Entrada no válida
            respuesta = "Por favor, escribe menu o 2 para salir."

        interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
        return jsonify({'respuesta': respuesta})
    
    elif state == 'niveles':
        if user_input == '1':  # Si el usuario quiere más información
            ##session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = respuesta = """
                        ¡Claro! Aquí tienes más información sobre nuestras Niveles:<br><br>

                        <b>Básico:</b><br>
                        <ul>
                        <li>Objetivo: Proporcionar una base sólida en inglés para principiantes.</li>
                        <li>Habilidades trabajadas: Introducción a la gramática, vocabulario básico y habilidades de conversación cotidiana.</li>
                        <li>Duración promedio: 6 meses.</li>
                        <li>Material incluido: Libro de trabajo, ejercicios interactivos y acceso a nuestra plataforma en línea.</li>
                        </ul><br>

                        <b>Intermedio:</b><br>
                        <ul>
                        <li>Objetivo: Ampliar el conocimiento de gramática, vocabulario y habilidades de conversación para contextos más complejos.</li>
                        <li>Habilidades trabajadas: Comprensión auditiva, escritura estructurada y habilidades de debate.</li>
                        <li>Duración promedio: 6 meses</li>
                        <li>Proyectos prácticos: Presentaciones y simulaciones de situaciones reales.</li>
                        </ul><br>

                        <b>Avanzado:</b><br>
                        <ul>
                        <li>Objetivo: Perfeccionar las habilidades lingüísticas para alcanzar un nivel fluido y profesional.</li>
                        <li>Habilidades trabajadas: Redacción formal, fluidez conversacional y preparación para certificaciones internacionales (como TOEFL, IELTS).</li>
                        <li>Duración promedio: 6 meses.</li>
                        <li>Enfoque personalizado: Clases orientadas a metas específicas como negocios, viajes o estudios en el extranjero.</li>
                        </ul><br><br>
                        Si deseas regresar al menú escribe menu o 2 para salir.<br>"""
            return jsonify({'respuesta': respuesta})
            
        elif user_input == 'menu':  # Si el usuario no quiere más información
            session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = """Volviendo al menú...<br><br>
                            ¡Hola de nuevo! ¿En qué más te puedo ayudar? Por favor, elige una opción del menú.<br>
                            1. Costos<br>
                            2. Modalidades<br>
                            3. Niveles de inglés<br>
                            4. Cursos y Programas<br>
                            5. Requisitos de Inscripción<br>
                            6. Registro para ser contactado por un asesor<br>
                            7. Salir"""
        
        elif user_input == '2':  # Si el usuario no quiere más información
            respuesta = "Entendido. ¡Gracias por Utilizar el Asistente Virtual!"
            session.clear()

        else:  # Entrada no válida
            respuesta = "Por favor, escribe menu o 2 para salir."

        interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
        return jsonify({'respuesta': respuesta})

    elif state == 'cursos':
        if user_input == '1':  # Si el usuario quiere más información
            ##session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = respuesta = """
                        ¡Claro! Aquí tienes más información sobre nuestros Cursos:<br><br>

                        <b>Inglés general:</b><br>
                        <ul>
                        <li>Mejora habilidades de comunicación (lectura, escritura, escucha y conversación).</li>
                        <li>Actividades prácticas y cotidianas para ganar confianza.</li>
                        </ul><br>

                        <b>Inglés para negocios:</b><br>
                        <ul>
                        <li>Aprende vocabulario y habilidades clave para el entorno profesional.</li>
                        <li>Practica reuniones, correos formales y presentaciones.</li>
                        </ul><br>

                        <b>Preparación para exámenes internacionales:</b><br>
                        <ul>
                        <li>Prepárate para TOEFL, IELTS, Cambridge y más.</li>
                        <li>Estrategias y simulacros para obtener el mejor puntaje.</li>
                        </ul><br><br>
                        ¿Si te intera algun curso coloca 6 para registrarte y te contante un asesor o 2 para regresar al menu?.<br>"""
            return jsonify({'respuesta': respuesta})
            
        elif user_input == '2':  # Si el usuario no quiere más información
            session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = """Volviendo al menú...<br><br>
                            ¡Hola de nuevo! ¿En qué más te puedo ayudar? Por favor, elige una opción del menú.<br>
                            1. Costos<br>
                            2. Modalidades<br>
                            3. Niveles de inglés<br>
                            4. Cursos y Programas<br>
                            5. Requisitos de Inscripción<br>
                            6. Registro para ser contactado por un asesor<br>
                            7. Salir"""
        elif user_input == '6':  # Si el usuario no quiere más información
            session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = render_template('registro.html')
            session.clear()  # Limpiar la sesión al finalizar
            return jsonify({'respuesta': respuesta})
        

        else:  # Entrada no válida
            respuesta = "Por favor, selecciona 6 o 2 para regresar al menu."

        interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
        return jsonify({'respuesta': respuesta})

    elif state == 'requisitos':
        if user_input == '1':  # Si el usuario quiere más información
            ##session['state'] = 'menu'  # Regresar al estado 'menu'
            session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = render_template('registro.html')
            session.clear()  # Limpiar la sesión al finalizar
            return jsonify({'respuesta': respuesta})
            
        elif user_input == '2':  # Si el usuario no quiere más información
            session['state'] = 'menu'  # Regresar al estado 'menu'
            respuesta = """Volviendo al menú...<br><br>
                            ¡Hola de nuevo! ¿En qué más te puedo ayudar? Por favor, elige una opción del menú.<br>
                            1. Costos<br>
                            2. Modalidades<br>
                            3. Niveles de inglés<br>
                            4. Cursos y Programas<br>
                            5. Requisitos de Inscripción<br>
                            6. Registro para ser contactado por un asesor<br>
                            7. Salir"""

        else:  # Entrada no válida
            respuesta = "Por favor, selecciona 1 o 2."

        interacciones_pila.append({'mensaje_usuario': user_input, 'respuesta_chatbot': respuesta})
        return jsonify({'respuesta': respuesta})

    # Añade más estados para las demás secciones aquí...

    else:
        session['state'] = 'inicio'
        return jsonify({'respuesta': "Ha ocurrido un error. Volvamos al inicio."})
    # Enviar la respuesta como JSON
    ##return jsonify({'respuesta': respuesta})

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    
    # Insertar los datos en la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO clientes (nombre, telefono, correo) VALUES (%s, %s, %s)', (nombre, telefono, correo))
    cliente_id = cursor.lastrowid  # Obtener el ID del cliente recién insertado
    
    connection.commit()
    
    # Guardar las interacciones del cliente en la tabla 'interacciones_chatbot'
    for interaccion in interacciones_pila:
        cursor.execute('INSERT INTO interacciones_chatbot (cliente_id, mensaje_usuario, respuesta_chatbot) VALUES (%s, %s, %s)', 
                       (cliente_id, interaccion['mensaje_usuario'], interaccion['respuesta_chatbot']))
    connection.commit()

    cursor.close()
    connection.close()

     # Limpiar la pila después de registrar al cliente
    interacciones_pila.clear()

    asignar_cliente_personal(cliente_id)

    opciones = [
        "1. Costos",
        "2. Modalidades",
        "3. Niveles de Inglés",
        "4. Cursos y Programas",
        "5. Requisitos de Inscripción",
        "6. Registro para ser contactado por un asesor"
    ]

    session.clear()
    return render_template('index.html', respuesta="¡Gracias! Te contactará un asesor pronto. Ingresa un Número si tienes mas Dudas.", opciones= opciones)

def asignar_cliente_personal(cliente_id):
    try:
        cl_id = cliente_id

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT id FROM usuarios WHERE rol = 'vinculacion' ORDER BY RAND() LIMIT 1"
        cursor.execute(query)
        personal = cursor.fetchone()

        if personal:
                personal_id = personal[0]
                query = "INSERT INTO asignaciones (cliente_id, personal_id) VALUES (%s, %s)"
                cursor.execute(query, (cl_id, personal_id))
                connection.commit()
    except Error as e:
        print(f"Error al asignar cliente: {e}")

##TABLAS ADMIN
@app.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT 
    c.id AS cliente_id,
    c.nombre AS cliente_nombre,
    c.telefono AS cliente_telefono,
    c.correo AS cliente_correo,
    c.timestamp AS cliente_creado,
    COALESCE(u.id, 'Sin asignación') AS usuario_id,
    COALESCE(u.nombre, 'Sin asignación') AS usuario_nombre
FROM 
    clientes c
LEFT JOIN 
    asignaciones a ON c.id = a.cliente_id
LEFT JOIN 
    usuarios u ON a.personal_id = u.id;
""")
        clientes = cursor.fetchall()
        return jsonify(clientes)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para obtener los datos de la tabla 'usuarios'
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, nombre, correo, telefono, rol, timestamp FROM usuarios")
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para obtener los datos de la tabla 'asignaciones'
@app.route('/asignaciones', methods=['GET'])
def get_asignaciones():
    # Obtener el ID y rol desde la sesión
    user_id = session.get('user_id')
    rol = session.get('rol')

    if not (user_id and rol):
        return jsonify({"error": "No estás autenticado"}), 401 # Verificar si el usuario está logueado

    try:
        connection = get_db_connection()
        

        if rol == 'administrador':
            cursor = connection.cursor()
            # Administrador: Ver todas las asignaciones
            query = """
                SELECT 
                    asignaciones.id AS asignacion_id,
                    clientes.id AS cliente_id,
                    clientes.nombre AS nombre_cliente,
                    usuarios.id AS usuario_id,
                    usuarios.nombre AS nombre_usuario,
                    asignaciones.timestamp AS fecha_asignacion
                FROM 
                    asignaciones
                INNER JOIN 
                    clientes ON asignaciones.cliente_id = clientes.id
                INNER JOIN 
                    usuarios ON asignaciones.personal_id = usuarios.id
                ORDER BY 
                    asignaciones.timestamp DESC;
            """
            cursor.execute(query)

        elif rol == 'vinculacion':
            # Vinculación: Ver solo sus asignaciones
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    asignaciones.id AS asignacion_id,
                    clientes.id AS cliente_id,
                    clientes.nombre AS nombre_cliente,
                    asignaciones.timestamp AS fecha_asignacion
                FROM 
                    asignaciones
                INNER JOIN 
                    clientes ON asignaciones.cliente_id = clientes.id
                WHERE 
                    asignaciones.personal_id = %s
                ORDER BY 
                    asignaciones.timestamp DESC;
            """
            cursor.execute(query, (user_id,))

        else:
            return jsonify({"error": "Rol no autorizado"}), 403

        asignaciones = cursor.fetchall()
        return jsonify(asignaciones)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/inscripciones', methods=['GET'])
def get_inscripciones():
    # Obtener el ID y rol desde la sesión
    user_id = session.get('user_id')
    rol = session.get('rol')

    if not (user_id and rol):
        return jsonify({"error": "No estás autenticado"}), 401 # Verificar si el usuario está logueado

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if rol == 'administrador':
            
            # Administrador: Ver todas las asignaciones
            query = """
                SELECT 
                    i.id AS inscripcion_id,
                    c.nombre AS nombre_cliente,
                    i.curso AS curso_inscrito,
                    i.fecha_inscripcion,
                    i.identificacion_oficial_pdf, 
                    i.comprobante_domicilio_pdf, 
                    i.comprobante_pago_pdf
                FROM 
                    inscripciones i
                JOIN 
                    asignaciones a ON i.cliente_id = a.cliente_id
                JOIN 
                    usuarios u ON a.personal_id = u.id
                JOIN 
                    clientes c ON i.cliente_id = c.id
            """
            cursor.execute(query)

        elif rol == 'vinculacion':
            # Vinculación: Ver solo sus asignaciones
            query = """
                SELECT 
                    i.id AS inscripcion_id,
                    c.id AS id_cliente,
                    c.nombre AS nombre_cliente,
                    i.curso AS curso_inscrito,
                    i.fecha_inscripcion,
                    i.identificacion_oficial_pdf, 
                    i.comprobante_domicilio_pdf, 
                    i.comprobante_pago_pdf
                FROM 
                    inscripciones i
                JOIN 
                    asignaciones a ON i.cliente_id = a.cliente_id
                JOIN 
                    usuarios u ON a.personal_id = u.id
                JOIN 
                    clientes c ON i.cliente_id = c.id
                WHERE 
                    u.id = %s;
            """
            cursor.execute(query, (user_id,))

        else:
            return jsonify({"error": "Rol no autorizado"}), 403

        asignaciones = cursor.fetchall()
        return jsonify(asignaciones)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para registrar una inscripción
@app.route('/inscripcion', methods=['POST'])
def registrar_inscripcion():
    data = request.form
    cliente_id = data.get('cliente_id')
    curso = data.get('curso')
    fecha_inscripcion = data.get('fecha_inscripcion')
    
    # Verificar que los campos obligatorios están presentes
    if not (cliente_id and curso and fecha_inscripcion):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Obtener los archivos
    identificacion_oficial_pdf = request.files.get('identificacion_oficial_pdf')
    comprobante_domicilio_pdf = request.files.get('comprobante_domicilio_pdf')
    comprobante_pago_pdf = request.files.get('comprobante_pago_pdf')

    # Verificar que los archivos necesarios están presentes
    if not (identificacion_oficial_pdf and comprobante_domicilio_pdf):
        return jsonify({"error": "Faltan archivos obligatorios"}), 400

    # Guardar los archivos
    try:
        identificacion_oficial_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(identificacion_oficial_pdf.filename))
        comprobante_domicilio_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(comprobante_domicilio_pdf.filename))

        identificacion_oficial_pdf.save(identificacion_oficial_pdf_path)
        comprobante_domicilio_pdf.save(comprobante_domicilio_pdf_path)

        # Si se subió comprobante de pago, guardarlo también
        if comprobante_pago_pdf:
            comprobante_pago_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(comprobante_pago_pdf.filename))
            comprobante_pago_pdf.save(comprobante_pago_pdf_path)
        else:
            comprobante_pago_pdf_path = None

        # Conexión a la base de datos y ejecución de la consulta
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
                INSERT INTO inscripciones (cliente_id, curso, fecha_inscripcion, identificacion_oficial_pdf, 
                                           comprobante_domicilio_pdf, comprobante_pago_pdf)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        cursor.execute(query, (cliente_id, curso, fecha_inscripcion, identificacion_oficial_pdf_path, 
                               comprobante_domicilio_pdf_path, comprobante_pago_pdf_path))

        connection.commit()
        return jsonify({"message": "Inscripción registrada con éxito"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al registrar inscripción: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para actualizar el comprobante de pago de una inscripción
@app.route('/actualizar_comprobante_pago', methods=['POST'])
def actualizar_comprobante_pago():
    data = request.form
    cliente_id = data.get('cliente_id')
    inscripcion_id = data.get('inscripcion_id')
    
    # Verificar que los campos obligatorios están presentes
    if not (cliente_id and inscripcion_id):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Obtener el nuevo comprobante de pago (opcional)
    comprobante_pago_pdf = request.files.get('comprobante_pago_pdf')

    if not comprobante_pago_pdf:
        return jsonify({"error": "Debe proporcionar el comprobante de pago"}), 400

    try:
        # Guardar el archivo
        comprobante_pago_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(comprobante_pago_pdf.filename))
        comprobante_pago_pdf.save(comprobante_pago_pdf_path)

        # Conexión a la base de datos y ejecución de la consulta para actualizar
        connection = get_db_connection()
        cursor = connection.cursor()

        # Verificar si la inscripción existe y si pertenece al cliente indicado
        cursor.execute("SELECT * FROM inscripciones WHERE id = %s AND cliente_id = %s", (inscripcion_id, cliente_id))
        inscripcion = cursor.fetchone()

        if not inscripcion:
            return jsonify({"error": "Inscripción no encontrada o no pertenece a este cliente"}), 404

        # Actualizar el comprobante de pago
        query = """
                UPDATE inscripciones
                SET comprobante_pago_pdf = %s
                WHERE id = %s
                """
        cursor.execute(query, (comprobante_pago_pdf_path, inscripcion_id))

        connection.commit()
        return jsonify({"message": "Comprobante de pago actualizado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el comprobante de pago: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()


# Ruta para obtener los datos de la tabla 'interacciones_chatbot'
@app.route('/interacciones', methods=['GET'])
def get_interacciones():
    # Obtener el ID y rol desde la sesión
    user_id = session.get('user_id')
    rol = session.get('rol')
    if not (user_id and rol):
        return jsonify({"error": "No estás autenticado"}), 401  # Verificar si el usuario está logueado
    
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        if rol == 'administrador':
                # Administrador: Ver todas las interacciones
                query=("""SELECT 
                    interacciones_chatbot.id AS interaccion_id,
                    clientes.id AS id_cliente,
                    clientes.nombre AS nombre_cliente,
                    interacciones_chatbot.mensaje_usuario,
                    interacciones_chatbot.respuesta_chatbot,
                    interacciones_chatbot.timestamp
                FROM 
                    interacciones_chatbot
                INNER JOIN 
                    clientes
                ON 
                    interacciones_chatbot.cliente_id = clientes.id
                ORDER BY 
                    interacciones_chatbot.timestamp DESC;
                """)
                cursor.execute(query)

        elif rol == 'vinculacion':
            # Vinculación: Ver solo sus interacciones
                query=("""SELECT 
                        a.cliente_id AS id_cliente_asignado,
                        c.nombre AS nombre_cliente,
                        i.id AS interaccion_id,
                        i.mensaje_usuario,
                        i.respuesta_chatbot,
                        i.timestamp
                    FROM 
                        asignaciones a
                    LEFT JOIN 
                        clientes c ON a.cliente_id = c.id
                    LEFT JOIN 
                        interacciones_chatbot i ON a.cliente_id = i.cliente_id
                    WHERE 
                        a.personal_id = %s;  -- Sustituye <user_id> por el ID del usuario actual
                """)
                cursor.execute(query,  (user_id,))

        interacciones = cursor.fetchall()
        return jsonify(interacciones)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para registrar interacciones con vinculacion
@app.route('/seguimiento', methods=['POST'])
def registrar_interaccion():
    data = request.json
    cliente_id = data['cliente_id']
    tipo_interaccion = data['tipo_interaccion']
    resultado = data['resultado']

    if not (cliente_id and tipo_interaccion and resultado):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
                INSERT INTO seguimiento_clientes (cliente_id, tipo_interaccion, resultado)
                VALUES (%s, %s, %s)
                """
        cursor.execute(query, (cliente_id, tipo_interaccion, resultado))
        connection.commit()
        return jsonify({"message": "Seguimiento creado con éxito"}), 201
    finally: 
        cursor.close()
        connection.close()

#Ruta para visualizar el seguimiento con vinculacion
@app.route('/seguimiento', methods=['GET'])
def obtner_seguimiento():
    # Obtener el ID desde la sesión
    user_id = session.get('user_id')
    rol = session.get('rol')

    if not (user_id and rol):
        return jsonify({"error": "No estás autenticado"}), 401  # Verificar si el usuario está logueado
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        if rol == 'administrador':
            query = """
                    SELECT 
                    a.id AS asignacion_id,
                    c.id AS cliente_id,
                    c.nombre AS nombre_cliente,
                    c.telefono,
                    c.correo,
                    s.tipo_interaccion,
                    COUNT(s.tipo_interaccion) AS cantidad_interacciones,
                    s.resultado,
                    viabilidad.situacion AS viabilidad,
                    a.timestamp AS fecha_asignacion
                FROM 
                    asignaciones a
                INNER JOIN 
                    clientes c ON a.cliente_id = c.id
                LEFT JOIN 
                    seguimiento_clientes s ON s.cliente_id = c.id
                LEFT JOIN (
                    SELECT
                        cliente_id,
                        CASE
                            WHEN COUNT(CASE WHEN tipo_interaccion = 'llamada' AND resultado = 'respondido' THEN 1 END) > 3 THEN 'Potencial'
                            WHEN COUNT(CASE WHEN tipo_interaccion IN ('correo', 'mensaje_texto') AND resultado = 'respondido' THEN 1 END) > 2 THEN 'Neutral'
                            ELSE 'No Potencial'
                        END AS situacion
                    FROM
                        seguimiento_clientes
                    GROUP BY cliente_id
                ) AS viabilidad ON c.id = viabilidad.cliente_id
                GROUP BY 
                    a.id, c.id, c.nombre, c.telefono, c.correo, s.tipo_interaccion, viabilidad.situacion, a.timestamp
                ORDER BY 
                    a.timestamp DESC;"""
            cursor.execute(query)

        elif rol == 'vinculacion':
            query = """
                SELECT 
                        a.id AS asignacion_id,
                        c.id AS cliente_id,
                        c.nombre AS nombre_cliente,
                        c.telefono,
                        c.correo,
                        s.tipo_interaccion,
                        COUNT(s.tipo_interaccion) AS cantidad_interacciones,
                        s.resultado,
                        viabilidad.situacion AS viabilidad,
                        a.timestamp AS fecha_asignacion
                    FROM 
                        asignaciones a
                    INNER JOIN 
                        clientes c ON a.cliente_id = c.id
                    LEFT JOIN 
                        seguimiento_clientes s ON s.cliente_id = c.id
                    LEFT JOIN (
                        SELECT
                            cliente_id,
                            CASE
                                WHEN COUNT(CASE WHEN tipo_interaccion = 'llamada' AND resultado = 'respondido' THEN 1 END) > 3 THEN 'Potencial'
                                WHEN COUNT(CASE WHEN tipo_interaccion IN ('correo', 'mensaje_texto') AND resultado = 'respondido' THEN 1 END) > 2 THEN 'Neutral'
                                ELSE 'No Potencial'
                            END AS situacion
                        FROM
                            seguimiento_clientes
                        GROUP BY cliente_id
                    ) AS viabilidad ON c.id = viabilidad.cliente_id
                    WHERE 
                        a.personal_id = %s
                    GROUP BY 
                        a.id, c.id, c.nombre, c.telefono, c.correo, s.tipo_interaccion, viabilidad.situacion, a.timestamp
                    ORDER BY 
                        a.timestamp DESC;"""
            cursor.execute(query,  (user_id,))
        seguimiento = cursor.fetchall()
        return jsonify(seguimiento)
    except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
    finally:
            cursor.close()
            connection.close()



@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    rol = data.get('rol')
    contrasena = data.get('contrasena')

    if not (nombre and correo and rol and contrasena):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO usuarios (nombre, correo, telefono, rol, contraseña)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, correo, telefono, rol, contrasena))
        connection.commit()
        return jsonify({"message": "Usuario creado con éxito"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()    


@app.route('/asignaciones', methods=['POST'])
def add_cliente():
    data = request.json
    clienteID = data.get('clienteID')
    personalID = data.get('personalID')
    
    if not (clienteID and personalID):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO asignaciones (cliente_id, personal_id)
            VALUES (%s, %s)
        """
        cursor.execute(query, (clienteID, personalID))
        connection.commit()
        return jsonify({"message": "Asignacion de cliente creado con éxito"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()    


##PAGINA LOGIN 

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    if not (correo and contrasena):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, rol FROM usuarios WHERE correo = %s AND contraseña = %s"
        cursor.execute(query, (correo, contrasena))
        usuario = cursor.fetchone()

        if usuario and usuario['rol'] in ['vinculacion', 'administrador']:
            session['user_id'] = usuario['id']
            session['rol'] = usuario['rol']
            return jsonify({"rol": usuario['rol']})  # Devolver el rol en la respuesta
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# Ruta para página de vinculación
@app.route('/vinculacion', methods=['GET'])
def vinculacion_pagina():
    return render_template('vinculacion.html')

# Ruta para página de administrador
@app.route('/administrador', methods=['GET'])
def administrador_pagina():
    return render_template('admin.html')

@app.route('/login', methods=['GET'])
def login_pagina():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Eliminar el ID de la sesión
    session.pop('rol', None)  # Eliminar el rol de la sesión
    return render_template('login.html')


if __name__ == '__main__':
    app.run()  # Escucha en todas las interfaces
