from repositories.chamado_repository import ChamadoRepository
from repositories.usuario_repository import UsuarioRepository

PRIORIDADES_VALIDAS = ("Baixa", "Média", "Alta")




PRIORIDADE_LIMITADA = "Alta"
LIMITE_ABERTOS = 5


class ChamadoService:
   

    @staticmethod
    def _serializa(chamado):
        return {
            "id": chamado.id,
            "titulo": chamado.titulo,
            "descricao": chamado.descricao,
            "prioridade": chamado.prioridade,
            "status": chamado.status,
            "tecnico": chamado.tecnico,
            "data_abertura": chamado.data_abertura.strftime("%d/%m/%Y %H:%M"),
            "usuario_id": chamado.usuario_id,
        }

    @staticmethod
    def consulta_chamados():
        chamados = ChamadoRepository.consulta_tudo()
        return [ChamadoService._serializa(c) for c in chamados]

    @staticmethod
    def consulta_abertos():
        chamados = ChamadoRepository.consulta_abertos()
        return [ChamadoService._serializa(c) for c in chamados]

    @staticmethod
    def consulta_prioridade_alta():
        chamados = ChamadoRepository.consulta_por_prioridade("Alta")
        return [ChamadoService._serializa(c) for c in chamados]

    @staticmethod
    def cadastra_chamado(dados):
        if dados["prioridade"] not in PRIORIDADES_VALIDAS:
            return None, "Prioridade inválida. Use Baixa, Média ou Alta"

        usuario = UsuarioRepository.consulta_um(dados["usuario_id"])
        if not usuario:
            return None, "O usuário informado não existe"

        if dados["prioridade"] == PRIORIDADE_LIMITADA:
            total_abertos = ChamadoRepository.conta_abertos_por_prioridade_e_usuario(
                dados["usuario_id"], PRIORIDADE_LIMITADA
            )
            if total_abertos >= LIMITE_ABERTOS:
                return None, (
                    f"Este usuário já possui {LIMITE_ABERTOS} chamados de prioridade "
                    f"{PRIORIDADE_LIMITADA} em aberto"
                )

        chamado = ChamadoRepository.cadastrar(dados)
        return chamado, None

    @staticmethod
    def atualiza_chamado(chamado_id, dados):
        chamado = ChamadoRepository.consulta_um(chamado_id)
        if not chamado:
            return None, None

        if dados["prioridade"] not in PRIORIDADES_VALIDAS:
            return None, "Prioridade inválida. Use Baixa, Média ou Alta"

        chamado = ChamadoRepository.atualizar(chamado, dados)
        return chamado, None

    @staticmethod
    def exclui_chamado(chamado_id):
        chamado = ChamadoRepository.consulta_um(chamado_id)
        if not chamado:
            return None, None

        ChamadoRepository.excluir(chamado)
        return chamado, None

    @staticmethod
    def inicia_atendimento(chamado_id):
        return ChamadoService._transiciona(chamado_id, "Aberto", "Em atendimento")

    @staticmethod
    def encerra_atendimento(chamado_id):
        return ChamadoService._transiciona(chamado_id, "Em atendimento", "Encerrado")

    @staticmethod
    def _transiciona(chamado_id, status_esperado, novo_status):
        chamado = ChamadoRepository.consulta_um(chamado_id)
        if not chamado:
            return None, None

        if chamado.status != status_esperado:
            return None, (
                f"Transição inválida: o chamado está '{chamado.status}', "
                f"era esperado '{status_esperado}'"
            )

        chamado = ChamadoRepository.alterar_status(chamado, novo_status)
        return chamado, None

    @staticmethod
    def gera_estatisticas():
        return {
            "usuarios": UsuarioRepository.conta_total(),
            "chamados": ChamadoRepository.conta_total(),
            "abertos": ChamadoRepository.conta_por_status("Aberto"),
            "em_atendimento": ChamadoRepository.conta_por_status("Em atendimento"),
            "encerrados": ChamadoRepository.conta_por_status("Encerrado"),
        }
