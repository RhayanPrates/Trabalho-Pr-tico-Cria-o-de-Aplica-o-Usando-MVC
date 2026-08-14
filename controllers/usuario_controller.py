from flask import jsonify, request

from services.usuario_service import UsuarioService


class UsuarioController:

    @staticmethod
    def valida_dados(dados):
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        if not dados.get("nome", "").strip():
            return jsonify({"erro": "Nome é obrigatório"}), 400
        if not dados.get("email", "").strip():
            return jsonify({"erro": "Email é obrigatório"}), 400
        return True

    @staticmethod
    def listar():
        usuarios = UsuarioService.consulta_usuarios()
        return jsonify(usuarios)

    @staticmethod
    def cadastrar():
        dados = request.json
        valido = UsuarioController.valida_dados(dados)
        if valido is not True:
            return valido

        usuario, erro = UsuarioService.cadastra_usuario(dados)
        if erro:
            return jsonify({"erro": erro}), 400

        return jsonify({
            "mensagem": "Usuário cadastrado",
            "id": usuario.id
        }), 201

    @staticmethod
    def atualizar(id):
        dados = request.json
        valido = UsuarioController.valida_dados(dados)
        if valido is not True:
            return valido

        usuario, erro = UsuarioService.atualiza_usuario(id, dados)
        if erro:
            return jsonify({"erro": erro}), 400
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        return jsonify({
            "mensagem": "Usuário atualizado",
            "id": usuario.id
        })

    @staticmethod
    def excluir(id):
        usuario, erro = UsuarioService.exclui_usuario(id)
        if erro:
            return jsonify({"erro": erro}), 400
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        return jsonify({
            "mensagem": "Usuário excluído",
            "id": usuario.id
        })

    @staticmethod
    def listar_chamados(id):
        chamados = UsuarioService.consulta_chamados_do_usuario(id)
        if chamados is None:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        return jsonify(chamados)
