import argparse
import logging

import fgts_pdf_dados

def prepare_logging(level=logging.INFO):
    # Switch between INFO/DEBUG while running in production/developping:

    # Configure logging for PanModel

    FORMATTER = logging.Formatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s")
    HANDLER = logging.StreamHandler()
    HANDLER.setFormatter(FORMATTER)

    loggers=[
        logging.getLogger('__main__'),
    ]

    for logger in loggers:
        logger.addHandler(HANDLER)
        logger.setLevel(level)

    return loggers[0]



def prepare_args():
    parser = argparse.ArgumentParser(
        prog='fgts-pdf-dados',
        description='Extrai dados de PDFs do FGTS e grava tudo em arquivo CSV pronto para usar com o Inverstorzilla.'
    )

    parser.add_argument('-o', dest='output', required=False,
        default='FGTS.csv',
        help='Nome do arquivo de saída. Usa "FGTS.csv" se omitido.')

    parser.add_argument('--nickname', '--nick', '-n',
        nargs=2,
        action='append',
        dest='nicknames',
        default=[],
        help='Define apelidos para nomes das empresas. Passe 2 argumentos: o nome como aparece no FGTS e o apelido bonito. Use múltiplas vezes.')

    parser.add_argument('--debug', dest='DEBUG', action=argparse.BooleanOptionalAction,
        default=False,
        help='Be more verbose and output messages to console.')

    parsed = parser.parse_args()

    return parsed.__dict__



def main():
    # Read environment and command line parameters
    args=prepare_args()

    # Setup logging
    global logger
    if args['DEBUG']:
        logger=prepare_logging(logging.DEBUG)
    else:
        logger=prepare_logging()

    args['nicknames']={
        item[0]: item[1]
        for item in args['nicknames']
    }

    (
        fgts_pdf_dados.extract(nicknames=args['nicknames'])
        .to_csv(args['output'], index=False)
    )



if __name__ == "__main__":
    main()
