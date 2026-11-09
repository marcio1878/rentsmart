# ==========================================================
#  RentSmart - Sistema de Orçamento de Locação
#  R.M Imóveis
#  Aluno: Marcio Rodrigues de Jesus
#
#  Como executar:  python rentsmart.py
# ==========================================================

import csv


# ----------------------------------------------------------
# Funções auxiliares (formatação e leitura com validação)
# ----------------------------------------------------------

def formatar_reais(valor):
    """Mostra um valor no formato brasileiro. Ex.: 1234.5 -> R$ 1.234,50"""
    texto = f"{abs(valor):,.2f}"                     # 1,234.50
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    if valor < 0:
        return "- R$ " + texto
    return "R$ " + texto


def ler_texto(pergunta):
    """Lê um texto e não aceita resposta vazia."""
    while True:
        resposta = input(pergunta).strip()
        if resposta != "":
            return resposta
        print("  Campo obrigatório. Tente novamente.")


def ler_numero(pergunta, minimo, maximo):
    """Lê um número inteiro e só aceita valores entre minimo e maximo."""
    while True:
        try:
            numero = int(input(pergunta))
            if minimo <= numero <= maximo:
                return numero
            print(f"  Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("  Valor inválido. Digite apenas números.")


def ler_sim_nao(pergunta):
    """Lê uma resposta 's' ou 'n' e devolve True ou False."""
    while True:
        resposta = input(pergunta + " (s/n): ").strip().lower()
        if resposta == "s":
            return True
        if resposta == "n":
            return False
        print("  Responda apenas com 's' ou 'n'.")


# ----------------------------------------------------------
# Classes dos imóveis
# ----------------------------------------------------------

class Imovel:
    """Classe base (classe mãe) de todos os imóveis."""

    def __init__(self, tipo, aluguel_base):
        self.tipo = tipo
        self.aluguel_base = aluguel_base

    def calcular_adicionais(self):
        # Cada tipo de imóvel define seus próprios adicionais.
        # Devolve uma lista de pares (descrição, valor).
        return []

    def calcular_descontos(self, subtotal):
        # Por padrão o imóvel não tem desconto.
        return []

    def descricao(self):
        return self.tipo

    def montar_itens(self):
        """Monta as linhas do aluguel: base, adicionais e descontos."""
        itens = [("Aluguel-base (" + self.tipo + ")", self.aluguel_base)]
        itens.extend(self.calcular_adicionais())

        # O desconto é calculado DEPOIS dos adicionais
        subtotal = 0
        for descricao, valor in itens:
            subtotal += valor
        itens.extend(self.calcular_descontos(subtotal))
        return itens

    def valor_mensal(self):
        """Soma todas as linhas e devolve o aluguel mensal final."""
        total = 0
        for descricao, valor in self.montar_itens():
            total += valor
        return round(total, 2)


class ImovelResidencial(Imovel):
    """Parte comum de casas e apartamentos: quartos e vaga de garagem."""

    VALOR_GARAGEM = 300

    def __init__(self, tipo, aluguel_base, adicional_dois_quartos, quartos, tem_garagem):
        super().__init__(tipo, aluguel_base)
        self.adicional_dois_quartos = adicional_dois_quartos
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def calcular_adicionais(self):
        adicionais = []
        if self.quartos == 2:
            adicionais.append(("Adicional por 2 quartos", self.adicional_dois_quartos))
        if self.tem_garagem:
            adicionais.append(("Vaga de garagem", self.VALOR_GARAGEM))
        return adicionais

    def descricao(self):
        texto = f"{self.tipo} de {self.quartos} quarto"
        if self.quartos == 2:
            texto += "s"
        if self.tem_garagem:
            texto += ", com vaga de garagem"
        else:
            texto += ", sem vaga de garagem"
        return texto


class Apartamento(ImovelResidencial):
    PERCENTUAL_DESCONTO = 0.05   # 5% para quem não tem crianças

    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__("Apartamento", 700, 200, quartos, tem_garagem)
        self.tem_criancas = tem_criancas

    def calcular_descontos(self, subtotal):
        if self.tem_criancas:
            return []
        desconto = round(subtotal * self.PERCENTUAL_DESCONTO, 2)
        return [("Desconto de 5% (sem crianças)", -desconto)]

    def descricao(self):
        if self.tem_criancas:
            return super().descricao() + ", com crianças"
        return super().descricao() + ", sem crianças"


class Casa(ImovelResidencial):
    def __init__(self, quartos, tem_garagem):
        super().__init__("Casa", 900, 250, quartos, tem_garagem)


class Estudio(Imovel):
    VALOR_PACOTE = 250        # pacote inicial com 2 vagas
    VALOR_VAGA_EXTRA = 60     # cada vaga além das 2 do pacote

    def __init__(self, tem_estacionamento, vagas_extras):
        super().__init__("Estúdio", 1200)
        self.tem_estacionamento = tem_estacionamento
        self.vagas_extras = vagas_extras

    def calcular_adicionais(self):
        adicionais = []
        if self.tem_estacionamento:
            adicionais.append(("Pacote de estacionamento (2 vagas)", self.VALOR_PACOTE))
            if self.vagas_extras > 0:
                valor = self.vagas_extras * self.VALOR_VAGA_EXTRA
                adicionais.append((f"Vagas extras ({self.vagas_extras} x R$ 60,00)", valor))
        return adicionais

    def descricao(self):
        if self.tem_estacionamento:
            total_vagas = 2 + self.vagas_extras
            return f"Estúdio com estacionamento ({total_vagas} vagas)"
        return "Estúdio sem estacionamento"


# ----------------------------------------------------------
# Taxa contratual (separada do aluguel)
# ----------------------------------------------------------

class TaxaContratual:
    VALOR_TOTAL = 2000
    MAXIMO_PARCELAS = 5

    def __init__(self, parcelas):
        self.parcelas = parcelas

    def valores_das_parcelas(self):
        """Divide os R$ 2.000,00 nas parcelas.
        A última parcela ajusta os centavos para a soma dar exatamente 2000.
        Ex.: 3 parcelas -> 666,67 + 666,67 + 666,66
        """
        valor_parcela = round(self.VALOR_TOTAL / self.parcelas, 2)
        valores = []
        for numero in range(1, self.parcelas):
            valores.append(valor_parcela)
        ultima = round(self.VALOR_TOTAL - valor_parcela * (self.parcelas - 1), 2)
        valores.append(ultima)
        return valores

    def parcela_do_mes(self, mes):
        """Quanto da taxa é pago no mês informado (0 depois da última parcela)."""
        if mes <= self.parcelas:
            return self.valores_das_parcelas()[mes - 1]
        return 0


# ----------------------------------------------------------
# Orçamento: junta cliente, imóvel e taxa
# ----------------------------------------------------------

class Orcamento:
    def __init__(self, cliente, imovel, taxa):
        self.cliente = cliente
        self.imovel = imovel
        self.taxa = taxa

    def projecao_12_meses(self):
        """Lista com os 12 meses: aluguel + parcela da taxa de cada mês."""
        aluguel = self.imovel.valor_mensal()
        meses = []
        for mes in range(1, 13):
            parcela = self.taxa.parcela_do_mes(mes)
            meses.append({
                "mes": mes,
                "aluguel": aluguel,
                "taxa": parcela,
                "total": round(aluguel + parcela, 2),
            })
        return meses

    def total_primeiro_ano(self):
        total = 0
        for linha in self.projecao_12_meses():
            total += linha["total"]
        return round(total, 2)

    def mostrar_resumo(self):
        print("\n" + "=" * 60)
        print("RESUMO DO ORÇAMENTO".center(60))
        print("=" * 60)
        print("Cliente:", self.cliente)
        print("Imóvel :", self.imovel.descricao())

        print("\nALUGUEL MENSAL")
        for descricao, valor in self.imovel.montar_itens():
            print(f"  {descricao:<42}{formatar_reais(valor):>15}")
        print("  " + "-" * 57)
        print(f"  {'Aluguel mensal':<42}{formatar_reais(self.imovel.valor_mensal()):>15}")

        print("\nTAXA CONTRATUAL (paga à parte, não faz parte do aluguel)")
        print(f"  {'Valor total':<42}{formatar_reais(self.taxa.VALOR_TOTAL):>15}")
        print(f"  {'Parcelamento':<42}{str(self.taxa.parcelas) + 'x':>15}")
        numero = 1
        for valor in self.taxa.valores_das_parcelas():
            print(f"  {'Parcela ' + str(numero):<42}{formatar_reais(valor):>15}")
            numero += 1

        print("\nPROJEÇÃO DOS 12 PRIMEIROS MESES")
        print(f"  {'Mês':<5}{'Aluguel':>15}{'Taxa':>15}{'Total do mês':>18}")
        for linha in self.projecao_12_meses():
            print(f"  {linha['mes']:<5}{formatar_reais(linha['aluguel']):>15}"
                  f"{formatar_reais(linha['taxa']):>15}{formatar_reais(linha['total']):>18}")
        print(f"  {'Total pago no 1º ano':<35}{formatar_reais(self.total_primeiro_ano()):>18}")
        print("=" * 60)

    def salvar_csv(self, nome_arquivo):
        """Grava a projeção dos 12 meses em um arquivo CSV.
        Usa ';' e vírgula nos decimais para abrir certinho no Excel.
        """
        with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mês", "Aluguel (R$)", "Parcela da taxa contratual (R$)", "Total do mês (R$)"])
            for linha in self.projecao_12_meses():
                escritor.writerow([
                    linha["mes"],
                    f"{linha['aluguel']:.2f}".replace(".", ","),
                    f"{linha['taxa']:.2f}".replace(".", ","),
                    f"{linha['total']:.2f}".replace(".", ","),
                ])
            escritor.writerow(["Total 1º ano", "", "", f"{self.total_primeiro_ano():.2f}".replace(".", ",")])


# ----------------------------------------------------------
# Perguntas ao usuário e programa principal
# ----------------------------------------------------------

def criar_imovel():
    """Pergunta o tipo de imóvel e as opções, e devolve o objeto criado."""
    print("\nTipos de imóvel:")
    print("  1 - Apartamento (R$ 700,00)")
    print("  2 - Casa (R$ 900,00)")
    print("  3 - Estúdio (R$ 1.200,00)")
    opcao = ler_numero("Escolha o tipo de imóvel (1, 2 ou 3): ", 1, 3)

    if opcao == 1:
        quartos = ler_numero("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+ R$ 300,00)?")
        criancas = ler_sim_nao("O cliente possui crianças?")
        return Apartamento(quartos, garagem, criancas)

    if opcao == 2:
        quartos = ler_numero("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+ R$ 300,00)?")
        return Casa(quartos, garagem)

    estacionamento = ler_sim_nao("Deseja o pacote de estacionamento com 2 vagas (+ R$ 250,00)?")
    vagas_extras = 0
    if estacionamento:
        vagas_extras = ler_numero("Quantas vagas extras além das 2 (R$ 60,00 cada, 0 a 10)? ", 0, 10)
    return Estudio(estacionamento, vagas_extras)


def main():
    print("=" * 60)
    print("RentSmart - Orçamento de Locação | R.M Imóveis".center(60))
    print("=" * 60)

    continuar = True
    while continuar:
        cliente = ler_texto("\nNome do cliente: ")
        imovel = criar_imovel()
        parcelas = ler_numero("Parcelar a taxa contratual de R$ 2.000,00 em quantas vezes (1 a 5)? ", 1, 5)

        orcamento = Orcamento(cliente, imovel, TaxaContratual(parcelas))
        orcamento.mostrar_resumo()

        nome_arquivo = "projecao_" + cliente.lower().replace(" ", "_") + ".csv"
        orcamento.salvar_csv(nome_arquivo)
        print("Arquivo CSV gerado:", nome_arquivo)

        continuar = ler_sim_nao("\nDeseja fazer outro orçamento?")

    print("Obrigado por usar o RentSmart!")


if __name__ == "__main__":
    main()
