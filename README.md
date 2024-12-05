# Privium# Privium

<p align="center">
  <a href="https://github.com/cesarneves-security/blooker"><img src="/img/1.png" alt="PRIVIUM"></a>
</p>

**Privium** é uma ferramenta de auditoria e exploração de privilégios para sistemas operacionais Linux e Windows.  
Ela auxilia na identificação de potenciais vulnerabilidades relacionadas a serviços, variáveis de ambiente, configurações de firewall e processos em execução.

## Funcionalidades

### Para Linux:
- Verifica serviços em execução via `systemd` para identificar configurações inseguras.
- Audita variáveis de ambiente, como `PATH`, para detectar diretórios manipuláveis.
- Analisa regras de firewall (iptables) para identificar permissões excessivamente amplas.

### Para Windows:
- Lista processos em execução para auditoria básica.

### Recursos Gerais:
- Gera relatórios detalhados das verificações realizadas em um arquivo (`relatorio_exploracao.txt`).
- Estilização de mensagens no terminal usando cores ANSI para facilitar a leitura.

## Requisitos
- Apenas bibliotecas padrão do Python 3.
- A ferramenta deve ser executada com permissões administrativas para verificar serviços, firewall e variáveis de ambiente.

## Instalação e Uso

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/privium.git
   cd privium
   python3 __main__.py
