# Dados do FGTS
Converta os PDFs fornecidos pela [app do FGTS](https://www.fgts.gov.br/Pages/sou-trabalhador/app-fgts.aspx)
em dados estruturados num CSV prontinho para ser usado com o [Investorzilla](https://github.com/avibrazil/investorzilla).

## Instalação
```shell
pip install fgts_pdf_dados --user
```

## Uso
```shell
shell> cd "Pasta com PDFs do FGTSs"
shell> ls
EXTRATO_EMPRESA_1.pdf
EXTRATO_EMPRESA_2.pdf
EXTRATO_EMPRESA_3.pdf

shell> fgts-pdf-dados
```
Ou converta os nomes das empresas para algo mais bonito:

```shell
shell> cd "Pasta com PDFs do FGTSs"
shell> fgts-pdf-dados \
    --nickname 'C I T SOFTWARE SA' 'CI&T' \
    --nickname 'DIGITAL HOUSE EDUCACAO LTDA' 'Digital House'
```

Todo mês, por volta do dia 21, eu entro na app do FGTS e gravo em PDF o extrato
atualizado de todas as minhas contas ativas. A inativas só preciso fazer uma
vez. Mantenho tudo junto numa pasta onde rodo o comando `fgts-pdf-dados`. Na
verdade, tenho um `Makefile` com o seguinte conteúdo:

```Makefile
all:
        # pip install --user fgts-pdf-dados
        fgts-pdf-dados \
            --nickname 'C I T SOFTWARE SA'             'CI&T' \
            --nickname 'DIGITAL HOUSE EDUCACAO LTDA'   'Digital House' \
            --nickname 'NOME FEIO CONFORME VEM NO PDF' 'Apelido Bonito' \
            --nickname 'OUTRO NOME FEIO'               'Apelido Bonito'
```

Aí, depois de gravar o extrato atualizado da app do FGTS, só preciso rodar `make`.

## Resultado
O arquivo `FGTS.csv` vai conter uma série histórica com todos os dados de cada
empresa ou conta de FGTS e já separa o que é movimentação de entrada e saída
(coluna movement) e o que é juros (coluna interest):
| account                    | time                                |   movement |   interest |     total | desc                                    |
|:---------------------------|:------------------------------------|-----------:|-----------:|----------:|:----------------------------------------|
| FGTS CI&T (472349)         | 2019-07-05 12:00:00.898000-03:00    |     12.52  |            |           | 150-DEPOSITO JUNHO 2019                 |
| FGTS CI&T (472349)         | 2019-07-05 12:00:00.898000001-03:00 |            |            |    12.52  |                                         |
| FGTS CI&T (472349)         | 2019-08-10 12:00:00.900000-03:00    |            |       2.2  |           | CREDITO DE JAM 0,002466                 |
| FGTS CI&T (472349)         | 2019-08-10 12:00:00.900000001-03:00 |            |            |    14.72  |                                         |
| FGTS Digital House (13360) | 2019-04-04 12:00:00.808000-03:00    |     123.45 |            |           | 115-DEPOSITO MARCO 2019                 |
| FGTS Digital House (13360) | 2019-04-04 12:00:00.808000001-03:00 |            |            |    123.45 |                                         |
| FGTS Digital House (13360) | 2021-09-21 12:00:00.895000001-03:00 |            |            |      1.74 |                                         |
| FGTS Digital House (13360) | 2021-09-21 12:00:00.896000-03:00    |      -1.74 |            |           | SAQUE JAM - COD 01                      |
| FGTS Digital House (13360) | 2021-09-21 12:00:00.896000001-03:00 |            |            |      0    |                                         |

## Sobre
Feito por Avi Alkalay para prover dados pessoais ao meu painel de investimentos
do [Investorzilla](https://github.com/avibrazil/investorzilla).