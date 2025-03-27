""" 
MIT License

Copyright (c) 2024 Pedro Luka Oliveira

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Original Repository: 
     GitHub: https://github.com/LukaOliveira/sispagtoolkit
     GitLab: https://gitlab.com/lukaoliveira/sispagtoolkit
"""


from .lotes.liquidacao_boletos_qrcode.segmentos.head_lote import HeadLote
from .lotes.liquidacao_boletos_qrcode.segmentos.segmento_j import SegmentoJ
from .lotes.liquidacao_boletos_qrcode.segmentos.segmento_j52 import SegmentoJ52
from .lotes.liquidacao_boletos_qrcode.segmentos.trailer_lote import TrailerLote

from .utils.objetos.cod_barras import codBarras
from .utils.break_line import break_line

class LoteLiquidacaoBoleto():
    def __init__(self, info_usuario, forma_pagamento='31'):
        self.head            = HeadLote()
        self.trailer         = TrailerLote()
        self.segmentos       = []
        self.info_usuario    = info_usuario
        self.forma_pagamento = forma_pagamento
        
        self.setHeadInfo()
        
        
    def novoSegmento(self, boleto):
        segmento = LiquidacaoBoletos(boleto, self.info_usuario)
        segmento.atualizarSequencia(len(self.segmentos)+1)
        
        self.segmentos.append(segmento)
        
    def setHeadInfo(self):
        self.head.setBanco(self.info_usuario.banco)
        self.head.setTipoPagamento('98')

        self.head.setFormaPagamento(self.forma_pagamento)
            
        self.head.setInfoEmpresa(self.info_usuario)
        self.head.setInfoBanco(self.info_usuario.banco)
        self.head.setEndereco(self.info_usuario.endereco)
        
    def setTrailerInfo(self, valor_total):   
        self.trailer.setBanco(self.info_usuario.banco)
        self.trailer.setTotalRegistros(len(self.segmentos)*2+2)
        self.trailer.setValorTotal(valor_total)
        
    def getQuantidadeRegistros(self):
        return len(self.segmentos)*2+2
    
    def setSequenciaLote(self, lote):
        self.head.setLote(lote)
        self.trailer.setLote(lote)
    
        for segmento in self.segmentos:
            segmento.atualizarLote(lote)
            
        
    def getLote(self):
        
        lote_final = ''
        valor_tt   = 0
        
        lote_final += f'{self.head.getSegmento()}{break_line}'
        
        for segmento in self.segmentos:
            lote_final += f'{segmento.getSegmento()}{break_line}'
            valor_tt   += segmento.valor
            
        valor_tt = (format(valor_tt, ".2f"))
        self.setTrailerInfo(str(valor_tt).replace('.', ''))
        
        lote_final += f'{self.trailer.getSegmento()}{break_line}'
            
        return lote_final



class LiquidacaoBoletos():
    def __init__(self,  boleto, info_usuario):
        self.segmentoj    = SegmentoJ()
        self.segmentoj52  = SegmentoJ52()
        self.info_usuario = info_usuario
        
        self.defSegmentoJ(  boleto)
        self.defSegmentoJ52(boleto)

    def defSegmentoJ(self, boleto):
        cod_barras = codBarras(boleto.cod_barras)
        
        self.valor = float(f'{cod_barras.valor[:-2]}.{cod_barras.valor[-2:]}')
        
        self.segmentoj.setBanco(self.info_usuario.banco)
        self.segmentoj.setCodigoDeBarras(cod_barras)
        self.segmentoj.setNomeFavorecido(boleto.favorecido.nome)
        self.segmentoj.setVencimentoNominal(cod_barras.vencimento_nominal)
        self.segmentoj.setValores(cod_barras.valor, 0, 0)
        self.segmentoj.setPagamento(boleto.data_pagamento, cod_barras.valor)
        self.segmentoj.setSeuNumero(boleto.seu_numero)
        
    def defSegmentoJ52(self, boleto):
        self.segmentoj52.setBanco(self.info_usuario.banco)
        self.segmentoj52.setInfoSacado(self.info_usuario)
        self.segmentoj52.setInfoCedente(boleto.favorecido.identificador, boleto.favorecido.nome)
        self.segmentoj52.setInfoSacador(boleto.favorecido.identificador, boleto.favorecido.nome)
        
        
    def atualizarSequencia(self, sequencia):
        self.segmentoj.setNumRegistro(sequencia)
        self.segmentoj52.setNumRegistro(sequencia)
        
    def atualizarLote(self, lote):
        self.segmentoj52.setLote(lote)
        self.segmentoj.setLote(lote)
        
    def getSegmento(self):
        return f'{self.segmentoj.getSegmento()}{break_line}{self.segmentoj52.getSegmento()}'