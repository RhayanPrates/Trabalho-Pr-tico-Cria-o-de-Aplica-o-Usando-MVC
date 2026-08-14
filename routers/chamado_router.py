from flask import Blueprint

from controllers.chamado_controller import ChamadoController

chamado_bp = Blueprint("chamado_bp", __name__)

chamado_bp.add_url_rule("/chamados", view_func=ChamadoController.listar, methods=["GET"])
chamado_bp.add_url_rule("/chamados", view_func=ChamadoController.cadastrar, methods=["POST"])
chamado_bp.add_url_rule("/chamados/<int:id>", view_func=ChamadoController.atualizar, methods=["PUT"])
chamado_bp.add_url_rule("/chamados/<int:id>", view_func=ChamadoController.excluir, methods=["DELETE"])
chamado_bp.add_url_rule("/chamados/<int:id>/iniciar", view_func=ChamadoController.iniciar, methods=["PATCH"])
chamado_bp.add_url_rule("/chamados/<int:id>/encerrar", view_func=ChamadoController.encerrar, methods=["PATCH"])
chamado_bp.add_url_rule("/chamados/abertos", view_func=ChamadoController.listar_abertos, methods=["GET"])
chamado_bp.add_url_rule("/chamados/prioridade/alta", view_func=ChamadoController.listar_prioridade_alta, methods=["GET"])
chamado_bp.add_url_rule("/estatisticas", view_func=ChamadoController.estatisticas, methods=["GET"])
