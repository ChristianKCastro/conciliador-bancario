import os
import csv
import time

DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

PASTA_ENTRADA = os.path.join(DIRETORIO_SCRIPT, 'entrada')
PASTA_PROCESSADOS = os.path.join(DIRETORIO_SCRIPT, 'processados')
PASTA_SAIDA = os.path.join(DIRETORIO_SCRIPT, 'saida')

for pasta in [PASTA_ENTRADA, PASTA_PROCESSADOS, PASTA_SAIDA]:
    os.makedirs(pasta, exist_ok=True)

def mock_consultar_cnpj(cnpj):
    banco_de_dados_cnpj = {
        '01.234.567/0001-89': 'Soluções em Aço S.A.',
        '98.765.432/0001-10': 'Tecnologia Avançada Ltda.',
        '11.222.333/0001-44': 'Imobiliária Morar Bem',
        '55.444.333/0001-22': 'Mercado do Bairro ME',
        }
    return banco_de_dados_cnpj.get(cnpj, 'CNPJ Não Encontrado')

def extrair_codigo_banco(nome_banco):
    banco_para_codigo = {
        'Banco do Brasil S.A.': '001',
        'Banco Bradesco S.A.': '237',
        'Itaú Unibanco S.A.': '341',
        'Caixa Econômica Federal': '104',
        'Nu Pagamentos S.A. - Nubank': '260'
    }
    return banco_para_codigo.get(nome_banco, '000')
      
def processar_extrato(caminho_completo_arquivo):
    print(f"Processando arquivo: {os.path.basename(caminho_completo_arquivo)}...")
    
    try:
        nome_arquivo_saida = f"erp_import_{os.path.basename(caminho_completo_arquivo)}"
        caminho_saida = os.path.join(PASTA_SAIDA, nome_arquivo_saida)

        with open(caminho_completo_arquivo, mode='r', encoding='utf-8') as f_entrada, \
             open(caminho_saida, mode='w', encoding='utf-8', newline='') as f_saida:

            leitor_csv = csv.reader(f_entrada)
            escritor_csv = csv.writer(f_saida)

            next(leitor_csv, None)
            
            cabecalho_erp = ['Data Lançamento', 'Histórico', 'Valor Pago', 
                           'CNPJ Pagador', 'Nome Pagador', 'Banco Origem']
            escritor_csv.writerow(cabecalho_erp)

            for linha in leitor_csv:
                data = linha[0]
                descricao = linha[1]
                cnpj = linha[2]
                banco = linha[3]
                valor = linha[5]
            
                codigo_banco = extrair_codigo_banco(banco)
                nome_pagador = mock_consultar_cnpj(cnpj)
                nome_banco = banco  
                linha_enriquecida = [data, descricao, valor, cnpj, nome_pagador, nome_banco]
                escritor_csv.writerow(linha_enriquecida)

        print(f"Arquivo processado com sucesso! Resultado salvo em: {caminho_saida}")
        return True 

    except Exception as e:
        print(f"Erro ao processar o arquivo {os.path.basename(caminho_completo_arquivo)}: {e}")
        return False

def extrair_codigo_banco(nome_banco):
    banco_para_codigo = {
        'Banco do Brasil S.A.': '001',
        'Banco Bradesco S.A.': '237',
        'Itaú Unibanco S.A.': '341',
        'Caixa Econômica Federal': '104',
        'Nu Pagamentos S.A. - Nubank': '260'
    }
    return banco_para_codigo.get(nome_banco, '000')
    
    try:
        nome_arquivo_saida = f"erp_import_{os.path.basename(caminho_completo_arquivo)}"
        caminho_saida = os.path.join(PASTA_SAIDA, nome_arquivo_saida)

        with open(caminho_completo_arquivo, mode='r', encoding='utf-8') as f_entrada, \
             open(caminho_saida, mode='w', encoding='utf-8', newline='') as f_saida:

            leitor_csv = csv.reader(f_entrada)
            escritor_csv = csv.writer(f_saida)

            cabecalho_erp = ['Data Lançamento', 'Histórico', 'Valor Pago', 'CNPJ Pagador', 'Nome Pagador', 'Banco Origem']
            escritor_csv.writerow(cabecalho_erp)

            next(leitor_csv, None)

            for linha in leitor_csv:
                
                data, descricao, valor, cnpj, cod_banco = linha

                nome_pagador = mock_consultar_cnpj(cnpj)
                nome_banco = mock_consultar_banco(cod_banco)

                linha_enriquecida = [data, descricao, valor, cnpj, nome_pagador, nome_banco]

                escritor_csv.writerow(linha_enriquecida)

        print(f"Arquivo processado com sucesso! Resultado salvo em: {caminho_saida}")
        return True 

    except Exception as e:
        print(f"Erro ao processar o arquivo {os.path.basename(caminho_completo_arquivo)}: {e}")
        return False

if __name__ == "__main__":
    print("Automação iniciada. Monitorando a pasta 'entrada'...")
    print("Pressione CTRL+C para parar o script.")

    while True:
        try:
            arquivos_na_pasta = os.listdir(PASTA_ENTRADA)

            if not arquivos_na_pasta:
                time.sleep(5)
                continue

            for nome_arquivo in arquivos_na_pasta:
                if nome_arquivo.lower().endswith('.csv'):
                    caminho_arquivo_original = os.path.join(PASTA_ENTRADA, nome_arquivo)

                    sucesso = processar_extrato(caminho_arquivo_original)
                    if sucesso:
                        caminho_arquivo_destino = os.path.join(PASTA_PROCESSADOS, nome_arquivo)
                        os.rename(caminho_arquivo_original, caminho_arquivo_destino)
                        print(f"Arquivo '{nome_arquivo}' movido para a pasta 'processados'.")

            time.sleep(5)

        except KeyboardInterrupt:
            print("\nAutomação encerrada pelo usuário.")
            break
        except Exception as ex:
            print(f"Ocorreu um erro inesperado no loop principal: {ex}")
            time.sleep(10)