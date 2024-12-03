from flask import Flask, render_template, request, redirect, url_for, flash
from models import Tarea
from datetime import datetime, timedelta
import db

app = Flask(__name__)
app.secret_key = 'Landa'


@app.route('/')
def home():
    todas_las_tareas = db.session.query(Tarea).all()
    return render_template("index.html", lista_de_tareas=todas_las_tareas, datetime=datetime, timedelta=timedelta)


@app.route('/crear-tarea', methods=['POST'])
def crear():
    contenido_tarea = request.form['contenidoTarea']
    fecha_contenido = request.form['fechaLimite']
    try:
        fecha_obj = datetime.strptime(fecha_contenido, '%Y-%m-%d').date()
    except ValueError:
        flash('Formato de fecha incorrecto. Debe ser dd/mm/yyyy.', 'error')
        return redirect(url_for('home'))
    if contenido_tarea.strip():
        tarea = Tarea(contenido=contenido_tarea, fecha=fecha_obj, hecha=False)
        db.session.add(tarea)
        db.session.commit()
    else:
        mensaje_error = '¡El contenido de la tarea no puede estar vacío!'
        todas_las_tareas = db.session.query(Tarea).all()
        return render_template("index.html", lista_de_tareas=todas_las_tareas, mensaje_error=mensaje_error,
                               datetime=datetime, timedelta=timedelta)
    return redirect(url_for('home'))


@app.route('/editar-tarea/<id>', methods=['POST', 'GET'])
def editar_tarea(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    if request.method == 'POST':
        dato_actualizado = request.form['contenidoEditar']
        fecha_actualizada = request.form['fechaEditar']
        fecha_obj = datetime.strptime(fecha_actualizada, '%Y-%m-%d').date()
        if dato_actualizado.strip():
            tarea.contenido = dato_actualizado
            tarea.fecha = fecha_obj
            db.session.commit()
            return redirect(url_for('home'))
        else:
            mensaje_error = '¡El contenido de la tarea no puede estar vacío!'
            todas_las_tareas = db.session.query(Tarea).all()
            return render_template("index.html", lista_de_tareas=todas_las_tareas, mensaje_error=mensaje_error,
                                   datetime=datetime, timedelta=timedelta)
    return render_template("index.html", lista_de_tareas=db.session.query(Tarea).all(), datetime=datetime, timedelta=timedelta)



@app.route('/tarea-hecha/<id>')
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    tarea.hecha = not tarea.hecha
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/formulario-update/<id>', methods=['POST', 'GET'])
def formulario_update(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    contenido = tarea.contenido
    return render_template('EditarDatos.html', idTarea=id, contenidoTarea=contenido)


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
