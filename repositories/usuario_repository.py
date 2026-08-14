from models.usuario import Usuario
from database import db


class UsuarioRepository:

    @staticmethod
    def consulta_tudo():
        return Usuario.query.order_by(Usuario.nome).all()

    @staticmethod
    def consulta_um(usuario_id):
        return Usuario.query.filter_by(id=usuario_id).first()

    @staticmethod
    def consulta_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def cadastrar(dados):
        usuario = Usuario(
            nome=dados["nome"],
            email=dados["email"],
            setor=dados.get("setor"),
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def atualizar(usuario, dados):
        usuario.nome = dados["nome"]
        usuario.email = dados["email"]
        usuario.setor = dados.get("setor", usuario.setor)
        db.session.commit()
        return usuario

    @staticmethod
    def excluir(usuario):
        db.session.delete(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def conta_total():
        return Usuario.query.count()
