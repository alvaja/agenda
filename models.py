import db
from sqlalchemy import Column, Integer, String, Boolean, Date


class Tarea(db.Base):
    __tablename__ = "tarea"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contenido = Column(String(200), nullable=False)
    fecha = Column(Date, nullable=False)
    hecha = Column(Boolean)

    def __init__(self, contenido, fecha, hecha):
        self.contenido = contenido
        self.fecha = fecha
        self.hecha = hecha

    def __repr__(self):
        return "Tarea {}: {} ({}) Fecha Limite: {}".format(self.id, self.contenido, self.hecha, self.fecha)

    def __str__(self):
        return "Tarea {}: {} ({}) Fecha Limite: {}".format(self.id, self.contenido, self.hecha, self.fecha)
