from repositories.usuario_repository import UsuarioRepository
from repositories.chamado_repository import ChamadoRepository


class UsuarioService:
    

    @staticmethod
    def consulta_usuarios():
        usuarios = UsuarioRepository.consulta_tudo()
        resultado = []
        for usuario in usuarios:
            resultado.append({
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "setor": usuario.setor,
            })
        return resultado

    @staticmethod
    def cadastra_usuario(dados):
        existe = UsuarioRepository.consulta_email(dados["email"])
        if existe:
            return None, "Já existe um usuário cadastrado com este e-mail"

        usuario = UsuarioRepository.cadastrar(dados)
        return usuario, None

    @staticmethod
    def atualiza_usuario(usuario_id, dados):
        usuario = UsuarioRepository.consulta_um(usuario_id)
        if not usuario:
            return None, None

        outro = UsuarioRepository.consulta_email(dados["email"])
        if outro and outro.id != usuario.id:
            return None, "Já existe um usuário cadastrado com este e-mail"

        usuario = UsuarioRepository.atualizar(usuario, dados)
        return usuario, None

    @staticmethod
    def exclui_usuario(usuario_id):
        usuario = UsuarioRepository.consulta_um(usuario_id)
        if not usuario:
            return None, None

        chamados = ChamadoRepository.consulta_por_usuario(usuario_id)
        if chamados:
            return None, "Não é possível excluir um usuário que possui chamados cadastrados"

        UsuarioRepository.excluir(usuario)
        return usuario, None

    @staticmethod
    def consulta_chamados_do_usuario(usuario_id):
        usuario = UsuarioRepository.consulta_um(usuario_id)
        if not usuario:
            return None

        chamados = ChamadoRepository.consulta_por_usuario(usuario_id)
        resultado = []
        for chamado in chamados:
            resultado.append({
                "id": chamado.id,
                "titulo": chamado.titulo,
                "descricao": chamado.descricao,
                "prioridade": chamado.prioridade,
                "status": chamado.status,
                "tecnico": chamado.tecnico,
                "data_abertura": chamado.data_abertura.strftime("%d/%m/%Y %H:%M"),
                "usuario_id": chamado.usuario_id,
            })
        return resultado
