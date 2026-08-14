from datetime import datetime

from database import db


class Chamado(db.Model):
    __tablename__ = "chamados"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    prioridade = db.Column(db.String(10), nullable=False)   # "Baixa" | "Média" | "Alta"
    status = db.Column(db.String(20), nullable=False, default="Aberto")
    tecnico = db.Column(db.String(120), nullable=True)
    data_abertura = db.Column(db.DateTime, default=datetime.now)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario = db.relationship("Usuario", back_populates="chamados")
