# -*- coding: utf-8 -*-
from webservice_interface import *
from usuario import Usuario
from resposta_calcula_preco_prazo import RespostaCalculaPrecoPrazo


class WebserviceCalculaPrecoPrazo(WebserviceInterface):

    _opcao = {
        True: 'S',
        False: 'N'
    }

    _FORMATO_CAIXA_PACOTE = 1
    _FORMATO_ROLO_PRISMA = 2
    _FORMATO_ENVELOPE = 3

    _nCdFormato = {
        '001': _FORMATO_ENVELOPE,
        '002': _FORMATO_CAIXA_PACOTE,
        '003': _FORMATO_ROLO_PRISMA,
    }

    _URL = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL'

    def __init__(self, obj_usuario):
        if not isinstance(obj_usuario, Usuario):
            raise TypeError

        self.obj_usuario = obj_usuario
        super(WebserviceCalculaPrecoPrazo, self).__init__(
            WebserviceCalculaPrecoPrazo._URL)

    @property
    def url(self):
        return WebserviceCalculaPrecoPrazo._URL

    def calcula_prazo(self):
        pass

    def calcula_preco(self):
        pass

    def calcula_preco_prazo(self, obj_servico_postagem, cep_origem,
                            cep_destino, peso, obj_dimensao, usar_mao_propria,
                            valor_declarado, aviso_recebimento):

        ncdservico = WebserviceCalculaPrecoPrazo._nCdFormato[
            obj_dimensao.tipo_objeto.codigo]
        scdmaopropria = WebserviceCalculaPrecoPrazo._opcao[usar_mao_propria]
        scdavisorecebimento = \
            WebserviceCalculaPrecoPrazo._opcao[aviso_recebimento]


        try:
            servicos = self._service.CalcPrecoPrazo(
                self.obj_usuario.codigo_admin, self.obj_usuario.senha,
                obj_servico_postagem.codigo, cep_origem, cep_destino, peso,
                ncdservico, obj_dimensao.comprimento, obj_dimensao.altura,
                obj_dimensao.largura, obj_dimensao.diametro, scdmaopropria,
                valor_declarado, scdavisorecebimento)

            result = []

            for servico in servicos.Servicos.cServico:
                result.append(RespostaCalculaPrecoPrazo(servico))

            return result

        except WebFault as exc:
            print '[ERRO] Em calcula_preco_prazo(). ' + exc.message
            return None
