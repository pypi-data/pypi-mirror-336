import pathlib
import logging
import re
import concurrent.futures
import pdfplumber
import pandas


def extract_single(pdf_file) -> pandas.DataFrame:
    with pdfplumber.open(pdf_file) as pdf:
        words=pandas.DataFrame.from_records(
            pdf.pages[0]
            .extract_words(keep_blank_chars=True)
        )

        employer=(
            words
            .query("x0<211 and top.between(154,160)")
            .text
            .values[0]
        )

        account=(
            words
            .query("x0>381 and top.between(218,250)")
            .text
            .values[0]
            .split()[0]
            .split('/')[1]
        )

        result = None
        for p in range(len(pdf.pages)):
            data=pdf.pages[p].extract_table()

            df=(
                pandas.DataFrame.from_records(data[1:], columns=data[0])
                .assign(
                    employer=employer,
                    account=account,
                )
            )

            if result is None:
                result=df
            else:
                result=pandas.concat([result, df])

    return result




def extract(path=pathlib.Path('.'), nicknames: dict=dict()):
    shift=pandas.to_timedelta('12h')

    # Linhas que representam juros.
    # Linhas diferentes destas são depósitos ou saques, não juros.
    interest="""
        CREDITO DE JAM
        150-JAM RECOLHIDO EMPRESA
        AC AUT JAM CALCULADO PELA CAIXA
        AC AUT JAM RECOLHIMENTO
        CREDITO DE JAM
        JAM MULTA RESCISORIA
        JAM RECOLH VERBAS
        JAM RESCISORIO
        115-JAM RECOLHIDO EMPRESA
    """.split()

    interest="(" + ")|(".join(interest) + ")"

    with concurrent.futures.ThreadPoolExecutor(thread_name_prefix='extractor') as executor:
        tasks=dict()
        for pdf_file in path.glob('*.pdf'):
            tasks[executor.submit(extract_single,pdf_file)]=pdf_file

        result=None
        for task in concurrent.futures.as_completed(tasks):
            logging.info(f'Finished to process {tasks[task]}')
            if result is None:
                result=task.result()
            else:
                result=pandas.concat([result,task.result()])

    return (
        result

        # Preciso do índice como um número sequencial global
        .reset_index(drop=True)

        # Organiza e padroniza nome das colunas
        .rename(columns=dict(
            DATA='time',
            LANÇAMENTO='desc',
            VALOR='value',
            TOTAL='total2'
        ))

        # Acerta dados
        .assign(
            # Converte para data e hora de Brasilia e incorpora cronologia pelo
            # índice
            time=lambda table: (
                pandas.to_datetime(table.time,dayfirst=True)
                .dt.tz_localize(tz='Brazil/East') +
                shift +
                pandas.to_timedelta(table.index, unit='ms')
            ),

            # Limpa texto descritivo
            desc=lambda table: table.desc.str.replace('\n',''),

            # Converte texto numérico em número real
            value=lambda table: (
                table.value.str
                .replace('R$ ','').str
                .replace('.','').str
                .replace(',','.')
                .astype(float)
            ),
            total2=lambda table: (
                table.total2.str
                .replace('R$ ','').str
                .replace('.','').str
                .replace(',','.')
                .astype(float)
            ),

            # Cria a coluna para eventos de pagamento de juros
            interest=lambda table: (
                table
                .apply(
                    lambda row: (
                        row.value
                        if re.match(interest,row.desc)
                        else pandas.NA
                    ),
                    axis=1
                )
            ),

            # Cria a coluna para eventos de entrada e saída (ledger)
            movement=lambda table: (
                table
                .apply(
                    lambda row: (
                        row.value
                        if not re.match(interest,row.desc)
                        else pandas.NA
                    ),
                    axis=1
                )
            ),

            # Converte os nomes feios do FGTS para nomes mais bonitos de empresas
            employer=lambda table: (
                table.employer.replace(nicknames,regex=True)
            ),

            # Consolida empresa e número da conta numa única coluna
            account=lambda table: (
                table
                .apply(
                    lambda row: f"FGTS {row['employer']} ({row['account']})",
                    axis=1
                )
            ),
        )

        # Remove colunas que já foram consolidadas
        .drop(columns=['employer'])

        # Remove linhas sem informação de tempo, geralmente as que são sumarizações
        .dropna(subset='time')

        # Fabrica coluna 'total' (saldo) com tempo de 1 nanosegundo após o
        # evento de movimento ou de juros.
        .pipe(
            lambda table: pandas.concat(
                [
                    table,
                    (
                        table[['account','time','total2']]
                        .rename(columns=dict(total2='total'))
                        .assign(
                            time=lambda table2: (
                                table2.time +
                                pandas.to_timedelta(1, unit='ns')
                            )
                        )
                    )
                ]
            )
        )

        # Ordena por conta de FGTS e tempo
        .sort_values(['account','time',])

        # Fabrica novo índice totalmente limpo e ordenado
        .reset_index(drop=True)

        # Padroniza nulos
        .fillna(pandas.NA)

        # Só as colunas que nos interessam
        [['account','time','movement','interest','total','desc']]

    )

    # result.apply(
    #     lambda row: row['value'] if re.match(interest,row.desc) else pandas.NA,
    #     axis=1
    # )

    result.to_csv('FGTS.csv', index=False)
    # result