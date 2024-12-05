import os
import platform
import subprocess
import json
os.system('clear')
# Cores ANSI para estilizar o texto
COR_INFO = "\33[1;32m"   # Verde (informação)
COR_ALERTA = "\33[1;33m"  # Amarelo (alerta)
COR_VULNERAVEL = "\33[1;31m"  # Vermelho (vulnerável)
COR_ERRO = "\33[1;31m"    # Vermelho (erro)
COR_RESET = "\33[0m"      # Reset de cor

# Arquivo para salvar o relatório
ARQUIVO_RELATORIO = "relatorio_exploracao.txt"

def salvar_relatorio(conteudo):
    """Salva o conteúdo em um arquivo de relatório."""
    with open(ARQUIVO_RELATORIO, "a") as f:
        f.write(conteudo + "\n")

def detectar_sistema():
    """Identifica o sistema operacional e exibe informações básicas."""
    so = platform.system()
    kernel = platform.release()
    arquitetura = platform.architecture()[0]
    usuario = os.getlogin()

    conteudo = f"\n {COR_INFO}[INFO]{COR_RESET} Sistema operacional detectado:"
    conteudo += f"   {COR_INFO}Sistema:{COR_RESET} {so}\n"
    conteudo += f"   {COR_INFO}Kernel:{COR_RESET} {kernel}\n"
    conteudo += f"   {COR_INFO}Arquitetura:{COR_RESET} {arquitetura}\n"
    conteudo += f"   {COR_INFO}Usuário atual:{COR_RESET} {usuario}\n"
    
    salvar_relatorio(conteudo)
    print(conteudo)  # Também exibe no terminal
    return so

# ====================
# FUNCIONALIDADES LINUX
# ====================
def verificar_servicos_linux():
    """Verifica serviços do systemd para vulnerabilidades."""
    conteudo = f" {COR_ALERTA}[*]{COR_RESET} Verificando configurações de serviços (systemd)..."
    salvar_relatorio(conteudo)
    print(conteudo)

    servicos_vulneraveis = []
    try:
        saida = subprocess.getoutput("systemctl list-units --type=service --state=running")
        servicos = saida.split("\n")[1:]  # Ignorar cabeçalho
        for servico in servicos:
            if ".service" in servico:
                nome_servico = servico.split()[0]
                detalhes = subprocess.getoutput(f"systemctl show {nome_servico} --property=ExecStart,User")
                if "root" in detalhes or "User=" not in detalhes:  # Verifica se executa como root
                    servicos_vulneraveis.append((nome_servico, detalhes))
        for nome, detalhes in servicos_vulneraveis:
            conteudo = f"   {COR_VULNERAVEL}[VULNERÁVEL]{COR_RESET} Serviço: {nome}\n"
            conteudo += f"     {COR_VULNERAVEL}Detalhes:{COR_RESET} {detalhes}"
            salvar_relatorio(conteudo)
            print(conteudo)  # Também exibe no terminal
    except Exception as e:
        conteudo = f" {COR_ERRO}[ERRO]{COR_RESET} Não foi possível verificar serviços: {e}"
        salvar_relatorio(conteudo)
        print(conteudo)  # Também exibe no terminal

def verificar_variaveis_ambiente():
    """Audita variáveis de ambiente para possíveis manipulações."""
    conteudo = f"\n {COR_ALERTA}[*]{COR_RESET} Auditando variáveis de ambiente..."
    salvar_relatorio(conteudo)
    print(conteudo)

    path = os.environ.get("PATH", "").split(":")
    for diretorio in path:
        if os.path.isdir(diretorio):
            permissoes = subprocess.getoutput(f"ls -ld {diretorio}")
            if "w" in permissoes and not permissoes.startswith("drwxr-xr-x"):
                conteudo = f"   {COR_ALERTA}[ALERTA]{COR_RESET} Diretório manipulável: {diretorio}"
                salvar_relatorio(conteudo)
                print(conteudo)  # Também exibe no terminal

def verificar_firewall_linux():
    """Lista regras do firewall e verifica exposições."""
    conteudo = f"\n {COR_ALERTA}[*]{COR_RESET} Verificando configurações de firewall..."
    salvar_relatorio(conteudo)
    print(conteudo)

    try:
        regras = subprocess.getoutput("iptables -L -n")
        linhas = regras.split("\n")
        for linha in linhas:
            if "ACCEPT" in linha and ("0.0.0.0/0" in linha or "anywhere" in linha):
                conteudo = f"   {COR_ALERTA}[ALERTA]{COR_RESET} Regra permissiva: {linha}"
                salvar_relatorio(conteudo)
                print(conteudo)  # Também exibe no terminal
    except Exception as e:
        conteudo = f" {COR_ERRO}[ERRO]{COR_RESET} Não foi possível verificar firewall: {e}"
        salvar_relatorio(conteudo)
        print(conteudo)  # Também exibe no terminal

def explorar_linux():
    """Executa verificações específicas para Linux."""
    conteudo = f" {COR_INFO}[INFO]{COR_RESET} Iniciando exploração em Linux...\n"
    salvar_relatorio(conteudo)
    print(conteudo)

    verificar_servicos_linux()
    verificar_variaveis_ambiente()
    verificar_firewall_linux()

# ======================
# FUNCIONALIDADES WINDOWS
# ======================
def verificar_processos_windows():
    """Lista os processos em execução no Windows."""
    conteudo = f"\n {COR_ALERTA}[*]{COR_RESET} Verificando processos em execução no Windows..."
    salvar_relatorio(conteudo)
    print(conteudo)

    try:
        saida = subprocess.getoutput("tasklist")
        salvar_relatorio(saida)
        print(saida)
    except Exception as e:
        conteudo = f" {COR_ERRO}[ERRO]{COR_RESET} Não foi possível listar processos: {e}"
        salvar_relatorio(conteudo)
        print(conteudo)

def explorar_windows():
    """Executa verificações específicas para Windows."""
    conteudo = f" {COR_INFO}[INFO]{COR_RESET} Iniciando exploração em Windows...\n"
    salvar_relatorio(conteudo)
    print(conteudo)

    verificar_processos_windows()

# ============================
# FUNÇÃO PRINCIPAL
# ============================
def main():
    print(f" ==== {COR_INFO}Explorador de Privilégios{COR_RESET} ====")
    sistema = detectar_sistema()

    if sistema == "Linux":
        explorar_linux()
    elif sistema == "Windows":
        explorar_windows()
    else:
        conteudo = f" {COR_ERRO}[ERRO]{COR_RESET} Sistema não suportado."
        salvar_relatorio(conteudo)
        print(conteudo)

if __name__ == "__main__":
    main()
