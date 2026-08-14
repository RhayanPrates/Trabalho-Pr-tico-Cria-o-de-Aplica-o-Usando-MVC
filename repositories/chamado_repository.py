from models.chamado import Chamado
from database import db


class ChamadoRepository:

    @staticmethod
    def consulta_tudo():
        return Chamado.query.order_by(Chamado.data_abertura.desc()).all()

    @staticmethod
    def consulta_um(chamado_id):
        return Chamado.query.filter_by(id=chamado_id).first()

    @staticmethod
    def consulta_por_usuario(usuario_id):
        return Chamado.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def consulta_abertos():
        return Chamado.query.filter_by(status="Aberto").all()

    @staticmethod
    def consulta_por_prioridade(prioridade):
        return Chamado.query.filter_by(prioridade=prioridade).all()

    @staticmethod
    def conta_abertos_por_prioridade_e_usuario(usuario_id, prioridade):
        return Chamado.query.filter(
            Chamado.usuario_id == usuario_id,
            Chamado.prioridade == prioridade,
            Chamado.status != "Encerrado",
        ).count()

    @staticmethod
    def cadastrar(dados):
        chamado = Chamado(
            titulo=dados["titulo"],
            descricao=dados["descricao"],
            prioridade=dados["prioridade"],
            status="Aberto",
            tecnico=dados.get("tecnico"),
            usuario_id=dados["usuario_id"],
        )
        db.session.add(chamado)
        db.session.commit()
        return chamado

    @staticmethod
    def atualizar(chamado, dados):
        chamado.titulo = dados["titulo"]
        chamado.descricao = dados["descricao"]
        chamado.prioridade = dados["prioridade"]
        chamado.tecnico = dados.get("tecnico", chamado.tecnico)
        db.session.commit()
        return chamado

    @staticmethod
    def excluir(chamado):
        db.session.delete(chamado)
        db.session.commit()
        return chamado

    @staticmethod
    def alterar_status(chamado, novo_status):
        chamado.status = novo_status
        db.session.commit()
        return chamado

    @staticmethod
    def conta_total():
        return Chamado.query.count()

    @staticmethod
    def conta_por_status(status):
        return Chamado.query.filter_by(status=status).count()
