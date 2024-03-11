from flask import flash, Flask,session, render_template, request,Response ,jsonify, redirect, url_for
from controllers.datab import dbConnection as dbase
from modules.asistencia import Asistencia
from modules.labores import Labores
from modules.usuario import Usuario
from modules.ventas import Ventas
from datetime import datetime, timedelta
from collections import defaultdict
from babel.dates import format_date #pip install babel


db = dbase()

app = Flask(__name__)
app.secret_key = 'modatatis'

# ---- Ruta para Index Admin 
@app.route('/',methods=['GET','POST'])
def principal():
    return render_template('index.html')

@app.route('/logout')
def logout():
    # Elimina el usuario de la sesión si está presente
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/index',methods=['GET','POST'])
def index():
    if request.method =='POST':
        usuari = request.form['usuario']
        contra = request.form['password']
        usuario_found = db.admin.find_one({'usuario':usuari,'password':contra})
        usuario_found2= db.usuario.find_one({'usuario':usuari,'password':contra})#Este modulo es para el usuario para ingresar a la otra pagina 
        if usuario_found:
            session["username"]= usuario_found["usuario"]
            session['usuario'] = usuari #*Se tiene que importar session para manejar las sesiones de los usuarios
            return redirect(url_for('registrar'))
        elif usuario_found2:
            session["username"]= usuario_found2["usuario"]
            session['usuario'] = usuari
            return redirect(url_for('u_asistencia'))
        else:
            flash('Usuario o contraseña incorrectas')
            return redirect(url_for('index'))
    else:
        return render_template('index.html')


#Admin Funcion de Registrar Usuario
@app.route('/admin/usuario',methods=['GET','POST'])
def registrar():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    if 'usuario' in session and session['usuario'] == 'admin':  # Comprobamos si el usuario ha iniciado sesión
        if request.method == 'POST':
            registro = db["usuario"]
            usuari = request.form['usuario']
            cedula = request.form['cedula']
            correo = request.form['correo']
            password = request.form['password']
            if usuari and cedula and correo and password:
                regis = Usuario(usuari, cedula, correo, password)
                registro.insert_one(regis.usuDBCollection())
                print("No hay nada")
                flash('Guardado en la base de datos')
                return redirect(url_for('registrar'))
            else:
                flash('Llena todos los campos')
                return redirect(url_for('registrar'))
        else:
            return render_template('admin/usuario.html')
    else:
        flash('Debes iniciar sesión para ver esta página.')
        return redirect(url_for('index'))  # Redirigimos al usuario a la página de inicio de sesión si no ha iniciado sesión

#Admin Vista Usuario

@app.route('/admin/vis_usua',methods=['GET','POST'])
def visusuarios():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    usuarios =db['usuario'].find()
    return render_template('admin/vis_usua.html',usuario=usuarios)

#Admin Editar Usuario 
@app.route('/edit_cli/<string:usu_name>',methods=['GET','POST'])
def adedusua(usu_name):
    usuario = db['usuario']
    usuarios=request.form["usuario"]
    cedula=request.form["cedula"]
    correo=request.form["correo"]
    password=request.form["password"]
    if usuarios and cedula and correo and password:
        usuario.update_one({'usuario':usu_name},{'$set':{'usuario':usuarios,'cedula':cedula,'correo':correo,'password':password }})
        return redirect(url_for("visusuarios"))  
    return render_template('admin/vis_usua.html')

#Admin Eliminar Usuario
@app.route('/delete_cli/<string:usu_name>', methods=['GET','POST'])
def elimiusu(usu_name):
    usuarios =db['usuario']
    usuarios.delete_one({'usuario':usu_name})
    return redirect(url_for('visusuarios'))

#Admin Asistencia para ingresar la asistencia select
@app.route('/admin/asistencia',methods=['GET','POST'])
def visasi():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method =='POST':
        asistencia = db["asistencia"]
        empleado = request.form['empleado']
        fecha = request.form['fecha']
        horas = request.form['hora']
        comentarios = request.form["comentario"]
        if empleado and fecha and horas and comentarios:
            asi = Asistencia(empleado,fecha,horas,comentarios)
            asistencia.insert_one(asi.asisDBCollection())
            flash('Guardado exitosamente')
            return redirect(url_for('visasi'))
        else:
            flash('Llena todos los campos')
        
    return render_template('admin/asistencia.html',usuario=adasi())
def adasi():
    usuarios = db.usuario.find({}, {"usuario": 1})
    return [usuario['usuario'] for usuario in usuarios]
# Admin labores y Select 
@app.route('/admin/labores',methods=['GET','POST'])
def labores():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method =='POST':
        labor = db["labores"]
        empleado = request.form['empleado']
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        if  empleado and fecha and descripcion:
            lal= Labores(empleado,fecha,descripcion)
            labor.insert_one(lal.laboDBCollection())
            flash('Guardado exitosamente')
            return redirect(url_for('labores'))
        else:
            flash('Llena todos los campos')
    
    return render_template('admin/labores.html',usuario=adla())

def adla():
    usuarios = db.usuario.find({}, {"usuario": 1})
    return [usuario['usuario'] for usuario in usuarios]

#Admin reporte

@app.route('/admin/reporte',methods=['GET','POST'])
def reporte():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    reportes = list(db.ventas.find())
    fechas_formateadas, sumas_como_cadenas = formatear_fecha(reportes)
    return render_template('admin/reporte.html', ventas=reportes, fechas=fechas_formateadas, sumas=sumas_como_cadenas)


def formatear_fecha(reportes):
    # Almacena los meses y años que ya has procesado
    meses_procesados = set()
    fechas_formateadas = []
    sumas = {}

    # Diccionario para mapear los nombres de los meses en inglés a español
    meses_en_español = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }

    for reporte in reportes:
        try:
            # Intenta obtener la fecha del reporte
            fecha = reporte['fecha']
            # Intenta convertir la venta a un flotante
            venta = float(reporte['venta'])
        except KeyError:
            # Si no hay un campo 'fecha' o 'venta', continuar con el siguiente reporte
            continue
        print("Fecha: ", fecha)  # Imprimir la fecha
        print("Venta: ", venta)  # Imprimir la venta

        # Convertir la fecha a un objeto datetime
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")

        # Formatear la fecha al formato deseado (en inglés)
        fecha_formateada = fecha_dt.strftime("%B %Y")  # Esto dará "December 2023"

        # Traducir el nombre del mes al español
        mes, año = fecha_formateada.split()
        fecha_formateada = meses_en_español[mes] + " " + año  # Esto dará "Diciembre 2023"

        # Si el mes y año ya han sido procesados, sumar el valor de 'venta' al total para este mes y año
        if fecha_formateada in meses_procesados:
            sumas[fecha_formateada] += venta
        else:
            # Si el mes y año no han sido procesados, inicializar la suma de 'venta' para este mes y año
            sumas[fecha_formateada] = venta
            # Agregar el mes y año a los meses procesados
            meses_procesados.add(fecha_formateada)
            # Agregar la fecha formateada a la lista de fechas formateadas
            fechas_formateadas.append(fecha_formateada)

    return fechas_formateadas, sumas



#Admin ventas y funcion para el Select

@app.route('/admin/ventas',methods=['GET','POST'])
def ventas():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method =='POST':
        ventas = db["ventas"]
        vendedor = request.form['vendedor']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        fecha=request.form['fecha']
        venta =request.form['venta']
        if vendedor and categoria and cantidad and fecha and venta:
            vent = Ventas(vendedor,categoria,cantidad,fecha,venta)
            ventas.insert_one(vent.ventDBCollection())
            flash('Guardado exitosamente')
            return redirect(url_for('ventas'))
        else:
            flash('Llena todos los campos')
    return render_template('admin/ventas.html',usuario=adve())

def adve():
    usuarios = db.usuario.find({}, {"usuario": 1})
    return [usuario['usuario'] for usuario in usuarios]


#Admin Editar ventas
@app.route('/admin/e_ventas',methods=['GET','POST'])
def e_ventas():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    ventas =db['ventas'].find()
    return render_template('admin/e_ventas.html',ventas=ventas)   

#Admin Editar venta 
@app.route('/edit_venta/<string:ven_name>',methods=['GET','POST'])
def ediven(ven_name):
    vendedor = db['ventas']
    usuarios=request.form["vendedor"]
    categoria=request.form["categoria"]
    cantidad=request.form["cantidad"]
    fecha=request.form["fecha"]
    venta=request.form["venta"]

    if usuarios and categoria and cantidad and fecha and venta:
        vendedor.update_one({'vendedor':ven_name},{'$set':{'usuario':usuarios,'categoria':categoria,'cantidad':cantidad,'fecha':fecha,'venta':venta}})
        return redirect(url_for("e_ventas"))  
    return render_template('admin/e_ventas.html')

#Admin Eliminar Venta
@app.route('/delete_venta/<string:ven_name>', methods=['GET','POST'])
def eliven(ven_name):
    vendedor =db['ventas']
    vendedor.delete_one({'vendedor':ven_name})
    return redirect(url_for('e_ventas'))



#Admin Reporte de ventas
@app.route('/admin/r_venta',methods=['GET','POST'])
def reporventa():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    # Obtener todas las ventas de la colección 'ventas'
    ventas = db.ventas.find()

    # Crear un diccionario para almacenar las ventas por usuario
    ventas_por_usuario = {}

    # Iterar sobre las ventas y sumar las cantidades por usuario
    for venta in ventas:
        usuario = venta['vendedor']
        cantidad = float(venta['venta'])  # Convertir el valor de 'cambio' a float
        fecha = venta['fecha']  # Obtener la fecha de la venta

        # Convertir la fecha a formato español
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_es = format_date(fecha, 'MMMM yyyy', locale='es_ES')

        # Verificar si el usuario ya está en el diccionario
        if usuario in ventas_por_usuario:
            ventas_por_usuario[usuario]['ventas'] += cantidad
            ventas_por_usuario[usuario]['fecha'] = fecha_es
        else:
            ventas_por_usuario[usuario] = {'ventas': cantidad, 'fecha': fecha_es}

    # Ordenar los usuarios por la cantidad de ventas en orden descendente
    usuarios_ordenados = sorted(ventas_por_usuario.items(), key=lambda x: x[1]['ventas'], reverse=True)

    # Renderizar la plantilla 'admin/r_venta.html' con los datos necesarios
    return render_template('admin/r_venta.html', usuarios_ordenados=usuarios_ordenados)

#Admin reporte diario de ventas
@app.route('/admin/r_diario')
def repodia(): 
        if 'username' not in session:
            flash("Inicia sesion con tu usuario y contraseña")
            return redirect(url_for('index'))     

        # Obtener todas las ventas de la colección 'ventas'
        ventas = db.ventas.find()
        
        # Crear un diccionario para almacenar las ventas por usuario
        ventas_por_usuario = {}
        
        # Iterar sobre las ventas y sumar las cantidades por usuario
        for venta in ventas:
            usuario = venta['vendedor']
            cantidad = float(venta['venta'])
            fecha = venta ["fecha"]  
        
            # Convertir la fecha a formato español
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_es = format_date(fecha, 'EEEE d MMMM yyyy', locale='es_ES')
        
            # Verificar si el usuario ya está en el diccionario
            if usuario in ventas_por_usuario:
                # Verificar si la fecha ya está en el diccionario del usuario
                if fecha_es in ventas_por_usuario[usuario]:
                    ventas_por_usuario[usuario][fecha_es] += cantidad
                else:
                    ventas_por_usuario[usuario][fecha_es] = cantidad
            else:
                ventas_por_usuario[usuario] = {fecha_es: cantidad}
        
        # Ordenar los usuarios por la cantidad de ventas en orden descendente
        usuarios_ordenados = sorted(ventas_por_usuario.items(), key=lambda x: sum(x[1].values()), reverse=True)

        # Renderizar la plantilla 'admin/r_diario.html' con los datos necesarios
        return render_template('admin/r_diario.html', usuarios_ordenados=usuarios_ordenados)


# Admin Ventas semanales 
@app.route('/admin/r_semanal')
def reposemana(): 
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    # Obtener todas las ventas de la colección 'ventas'
    ventas = db.ventas.find()
    
    # Crear un diccionario para almacenar las ventas por usuario
    ventas_por_usuario = {}
    
    # Iterar sobre las ventas y sumar las cantidades por usuario
    for venta in ventas:
        usuario = venta['vendedor']
        cantidad = float(venta['venta'])
        fecha = venta["fecha"]  
        
        # Convertir la fecha a formato español
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        
        # Calcular el inicio de la semana para la fecha
        inicio_semana = fecha - timedelta(days=fecha.weekday())
        inicio_semana_es = format_date(inicio_semana, 'EEEE d MMMM yyyy', locale='es_ES')
        
        # Verificar si el usuario ya está en el diccionario
        if usuario in ventas_por_usuario:
            # Verificar si la semana ya está en el diccionario del usuario
            if inicio_semana_es in ventas_por_usuario[usuario]:
                ventas_por_usuario[usuario][inicio_semana_es] += cantidad
            else:
                ventas_por_usuario[usuario][inicio_semana_es] = cantidad
        else:
            ventas_por_usuario[usuario] = {inicio_semana_es: cantidad}
    
    # Ordenar los usuarios por la cantidad de ventas en orden descendente
    usuarios_ordenados = sorted(ventas_por_usuario.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # Renderizar la plantilla 'admin/r_semanal.html' con los datos necesarios
    return render_template('admin/r_semanal.html', usuarios_ordenados=usuarios_ordenados)

#Admin  Tareas 

@app.route('/admin/tareas',methods=['GET','POST'])
def tareas():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    asistencia =db['asistencia'].find()
    labores =db['labores'].find()
    return render_template('admin/tareas.html',asistencia=asistencia,labores=labores)   


#Admin  vista y elimincacion y editacion de labores 

@app.route('/admin/vi_labores',methods=['GET','POST'])
def vi_labores():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    labores = db['labores'].find()
    return render_template('admin/vi_labores.html',labores=labores)
    
@app.route('/edit_la/<string:lab_name>',methods=['GET','POST'])
def edilab(lab_name):
    labores = db['labores']
    empleado = request.form["empleado"]
    fecha = request.form['fecha']
    descripcion = request.form["descripcion"]

    if empleado and fecha and descripcion:
        labores.update_one({'empleado':lab_name},{'$set':{'empleado':empleado,'fecha':fecha,'descripcion':descripcion}})
        return redirect(url_for("vi_labores"))
    return render_template("admin/vi_labores.html")

@app.route('/delete_lab/<string:lab_name>', methods=['GET','POST'])
def elilab(lab_name):
    labores =db['labores']
    labores.delete_one({'empleado':lab_name})
    return redirect(url_for('vi_labores'))


#Admin editar asistencia  
@app.route('/admin/vis_asistencia',methods=['GET','POST'])
def r_asistencia():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    asistencia = db['asistencia'].find()
    return render_template('admin/vis_asistencia.html',asistencia=asistencia)

@app.route('/edit_asi/<string:asi_name>',methods=['GET','POST'])
def ediasi(asi_name):
    asistencia = db['asistencia']
    empleado = request.form["empleado"]
    fecha = request.form['fecha']
    hora = request.form["hora"]
    comentarios = request.form["comentario"]
    if empleado and fecha and hora and comentarios:
        asistencia.update_one({'empleado':asi_name},{'$set':{'empleado':empleado,'fecha':fecha,'hora':hora,'comentario':comentarios}})
        return redirect(url_for("r_asistencia"))


@app.route('/delete_asi/<string:asi_name>', methods=['GET','POST'])
def eliasi(asi_name):
    asi =db['asistencia']
    asi.delete_one({'empleado':asi_name})
    return redirect(url_for('r_asistencia'))





#  ------------------- Carpeta Usuario ------------------------------------------------------------

@app.route('/usuario/venta',methods=['GET','POST'])
def u_usuario():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if 'usuario' in session:
        if request.method =='POST':
            ventas = db["ventas"]
            vendedor = request.form['vendedor']
            categoria = request.form['categoria']
            cantidad = request.form['cantidad']
            fecha=request.form['fecha']
            venta =request.form['venta']
            if vendedor and categoria and cantidad and fecha and venta:
                vent = Ventas(vendedor,categoria,cantidad,fecha,venta)
                ventas.insert_one(vent.ventDBCollection())
                flash('Guardado exitosamente')
                return redirect(url_for('u_usuario'))
            else:
                flash('Llena todos los campos')
        return render_template('usuario/venta.html', usuario=session['usuario'])    
    else:
        return render_template('usuario/venta.html',usuario=usve())

def usve():
    usuarios = db.usuario.find({}, {"usuario": 1})
    return [usuario['usuario'] for usuario in usuarios]


# * Usuario Asistencia
@app.route('/usuario/asistencia', methods=['GET', 'POST'])
def u_asistencia():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if 'usuario' in session:
        if request.method == 'POST':
            asistencia = db["asistencia"]
            empleado = request.form['empleado']
            fecha = request.form['fecha']
            horas = request.form['hora']
            comentarios = request.form["comentario"]
            if empleado and fecha and horas and comentarios:
                asi = Asistencia(empleado, fecha, horas, comentarios)
                asistencia.insert_one(asi.asisDBCollection())
                flash('Guardado exitosamente')
                return redirect(url_for('u_asistencia'))
            else:
                flash('Llena todos los campos')
        return render_template('usuario/asistencia.html', usuario=session['usuario'])
    else:
        return redirect(url_for('index'))

# * Usuario Tareas
@app.route('/usuario/v_tarea',methods=['GET','POST'])
def u_tareas():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    asistencia =db['asistencia'].find()
    labores =db['labores'].find()
    return render_template('usuario/v_tarea.html',asistencia=asistencia,labores=labores)   


if __name__ == '__main__':
    app.run(debug=True, port=4000)