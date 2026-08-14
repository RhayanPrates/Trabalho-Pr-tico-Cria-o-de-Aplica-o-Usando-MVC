from flask import jsonify, request

from services.chamado_service import ChamadoService


class ChamadoController:

    @staticmethod
    def valida_dados(dados, exigir_usuario_id=True):
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        if len(dados.get("titulo", "").strip()) < 5:
            return jsonify({"erro": "Título deve ter pelo menos 5 caracteres"}), 400
        if len(dados.get("descricao", "").strip()) < 10:
            return jsonify({"erro": "Descrição deve ter pelo menos 10 caracteres"}), 400
        if exigir_usuario_id and not dados.get("usuario_id"):
            return jsonify({"erro": "usuario_id é obrigatório"}), 400
        return True

    @staticmethod
    def listar():
        chamados = ChamadoService.consulta_chamados()
        return jsonify(chamados)

    @staticmethod
    def listar_abertos():
        chamados = ChamadoService.consulta_abertos()
        return jsonify(chamados)

    @staticmethod
    def listar_prioridade_alta():
        chamados = ChamadoService.consulta_prioridade_alta()
        return jsonify(chamados)

    @staticmethod
    def cadastrar():
        dados = request.json
        valido = ChamadoController.valida_dados(dados)
        if valido is not True:
            return valido

        chamado, erro = ChamadoService.cadastra_chamado(dados)
        if erro:
            return jsonify({"erro": erro}), 400

        return jsonify({
            "mensagem": "Chamado cadastrado",
            "id": chamado.id
        }), 201

    @staticmethod
    def atualizar(id):
        dados = request.json
        valido = ChamadoController.valida_dados(dados, exigir_usuario_id=False)
        if valido is not True:
            return valido

        chamado, erro = ChamadoService.atualiza_chamado(id, dados)
        if erro:
            return jsonify({"erro": erro}), 400
        if not chamado:
            return jsonify({"erro": "Chamado não encontrado"}), 404

        return jsonify({
            "mensagem": "Chamado atualizado",
            "id": chamado.id
        })

    @staticmethod
    def excluir(id):
        chamado, erro = ChamadoService.exclui_chamado(id)
        if erro:
            return jsonify({"erro": erro}), 400
        if not chamado:
            return jsonify({"erro": "Chamado não encontrado"}), 404

        return jsonify({
            "mensagem": "Chamado excluído",
            "id": chamado.id
        })

    @staticmethod
    def iniciar(id):
        chamado, erro = ChamadoService.inicia_atendimento(id)
        if erro:
            return jsonify({"erro": erro}), 400
        if not chamado:
            return jsonify({"erro": "Chamado não encontrado"}), 404

        return jsonify({
            "mensagem": "Atendimento iniciado",
            "id": chamado.id
        })

    @staticmethod
    def encerrar(id):
        chamado, erro = ChamadoService.encerra_atendimento(id)
        if erro:
            return jsonify({"erro": erro}), 400
        if not chamado:
            return jsonify({"erro": "Chamado não encontrado"}), 404

        return jsonify({
            "mensagem": "Chamado encerrado",
            "id": chamado.id
        })

    @staticmethod
    def estatisticas():
        dados = ChamadoService.gera_estatisticas()
        return jsonify(dados)
