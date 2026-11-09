# RentSmart — Orçamento de Locação | R.M Imóveis

Programa em Python que calcula o orçamento de aluguel de imóveis da **R.M Imóveis**. Ele aplica as regras comerciais da imobiliária, mostra um resumo detalhado do orçamento e gera um arquivo **CSV** com a projeção dos 12 primeiros meses.

Trabalho da disciplina *Algorithmic Thinking & Introduction to Object-Oriented Programming*.
**Aluno:** Marcio Rodrigues de Jesus

## O que é preciso

- **Python 3** instalado ([python.org/downloads](https://www.python.org/downloads/))
- Não precisa instalar nenhuma biblioteca extra.

## Como executar

1. Baixe o projeto pelo botão **Code → Download ZIP** aqui no GitHub e descompacte.
2. Abra o terminal (ou Prompt de Comando) dentro da pasta do projeto.
3. Execute:
   ```
   python rentsmart.py
   ```
4. Responda às perguntas. No final, o programa mostra o resumo do orçamento e cria o arquivo CSV na mesma pasta (exemplo: `projecao_ana_souza.csv`).
5. Para fazer outro orçamento, responda `s`. Para sair, responda `n`.

## Exemplo de uso

```
Nome do cliente: Ana Souza
Escolha o tipo de imóvel (1, 2 ou 3): 1
Quantidade de quartos (1 ou 2): 2
Deseja vaga de garagem (+ R$ 300,00)? (s/n): s
O cliente possui crianças? (s/n): n
Parcelar a taxa contratual de R$ 2.000,00 em quantas vezes (1 a 5)? 3

ALUGUEL MENSAL
  Aluguel-base (Apartamento)                      R$ 700,00
  Adicional por 2 quartos                         R$ 200,00
  Vaga de garagem                                 R$ 300,00
  Desconto de 5% (sem crianças)                  - R$ 60,00
  ---------------------------------------------------------
  Aluguel mensal                                R$ 1.140,00

TAXA CONTRATUAL (paga à parte, não faz parte do aluguel)
  Valor total                                   R$ 2.000,00
  Parcelamento                                           3x
  Parcela 1                                       R$ 666,67
  Parcela 2                                       R$ 666,67
  Parcela 3                                       R$ 666,66
```

Na pasta [`exemplos/`](exemplos/) há três arquivos CSV gerados pelo programa: um apartamento, uma casa e um estúdio.

## Regras implementadas

| Imóvel | Aluguel-base | Adicionais | Desconto |
|---|---|---|---|
| Apartamento | R$ 700,00 | 2 quartos: + R$ 200,00 · garagem: + R$ 300,00 | 5% se não tiver crianças (depois dos adicionais) |
| Casa | R$ 900,00 | 2 quartos: + R$ 250,00 · garagem: + R$ 300,00 | — |
| Estúdio | R$ 1.200,00 | pacote de 2 vagas: + R$ 250,00 · vaga extra: + R$ 60,00 cada | — |

- **Taxa contratual:** R$ 2.000,00 em 1 a 5 parcelas, mostrada separada do aluguel. Em 3 parcelas, a última fica com 1 centavo a menos (666,67 + 666,67 + 666,66) para o total dar exatamente R$ 2.000,00.
- **Projeção de 12 meses:** para cada mês, o aluguel, a parcela da taxa (só nos meses em que ela existe) e o total do mês.
- **Validações:** o nome não pode ficar vazio; o tipo de imóvel deve ser 1, 2 ou 3; os quartos, 1 ou 2; as respostas, `s` ou `n`; as vagas extras, de 0 a 10; as parcelas, de 1 a 5. Se o usuário digitar algo errado, o programa avisa e pergunta de novo.

## Classes do programa

| Classe | Função |
|---|---|
| `Imovel` | Classe mãe: guarda o tipo e o aluguel-base e calcula o valor mensal |
| `ImovelResidencial` | Parte comum de casas e apartamentos (quartos e garagem) |
| `Apartamento` | Regras do apartamento, incluindo o desconto de 5% |
| `Casa` | Regras da casa |
| `Estudio` | Regras do estúdio, com o pacote de estacionamento |
| `TaxaContratual` | Taxa de R$ 2.000,00 e suas parcelas |
| `Orcamento` | Junta cliente, imóvel e taxa; mostra o resumo e gera o CSV |

O fluxograma e a explicação completa estão no PDF da parte teórica.
