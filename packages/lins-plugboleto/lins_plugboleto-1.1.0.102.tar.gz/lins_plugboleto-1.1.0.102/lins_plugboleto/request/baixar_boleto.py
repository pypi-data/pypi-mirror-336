
import json

from .base import Base


class BaixarBoleto(Base):

    def __init__(self, authorize, environment):

        super(BaixarBoleto, self).__init__(authorize)

        self.environment = environment

    def execute(self, baixar_boleto:list):
        response = None
        uri = '%sboletos/baixa/lote' % self.environment.api
        boleto = json.dumps(baixar_boleto.split())

        try:
            response = self.send_request("POST", uri, boleto, baixa_boleto=True)

        except json.JSONDecodeError as error:
            raise Exception('Problema no retorno da plugboleto: {} - Json inválido: {}'.format(error, response))
        except Exception as error:
            raise Exception('Problema no retorno da plugboleto: {} - Response: {}'.format(error, response))

        return response
