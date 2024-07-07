Para atualizar o README do seu projeto NetScan Pro com base no último código, aqui está a versão atualizada:

---

## NetScan Pro

### Visão Geral
NetScan Pro é uma ferramenta avançada para escaneamento de rede e engenharia social, desenvolvida para facilitar a identificação de vulnerabilidades e a execução de técnicas de engenharia social de forma eficiente.

### Funcionalidades Principais
- **Ferramentas de Rede:**
  - Escaneamento de redes
  - Escaneamento de rede local
  - Escaneamento de vulnerabilidades

- **Ferramentas de Engenharia Social:**
  - Informações de números de telefone
  - Phishing (incluindo Páginas de Logins Falsas)

- **Atualização Automática:**
  - Atualização direta do GitHub, com notificações de novos arquivos ou atualizações de código.

### Requisitos
- Python 3.6 ou superior

### Instalação

#### Windows
1. **Instalação do Python:**
   - Baixe e instale Python 3.x em [python.org](https://www.python.org/downloads/).
   - Marque a opção "Add Python to PATH" durante a instalação.

2. **Clonar o Repositório:**
   - Abra o Prompt de Comando (CMD) e execute:
     ```sh
     git clone https://github.com/WeverttonBruno/NetScanPro
     cd NetScanPro
     ```

3. **Instalar Dependências:**
   - Instale as dependências listadas no arquivo `requirements.txt`:
     ```sh
     pip install -r requirements.txt
     ```

#### Linux (Kali, Ubuntu, etc.)
1. **Instalar Python e pip:**
   - Verifique e instale Python 3 e pip com os comandos:
     ```sh
     sudo apt update
     sudo apt install python3 python3-pip
     ```

2. **Instalar Git (se necessário):**
   - Se o Git não estiver instalado:
     ```sh
     sudo apt install git
     ```

3. **Clonar o Repositório e Instalar Dependências:**
   - Clone o repositório e instale as dependências:
     ```sh
     git clone https://github.com/WeverttonBruno/NetScanPro
     cd NetScanPro
     pip3 install -r requirements.txt
     ```

### Executando o NetScan Pro
1. **Executar o Script:**
   - No diretório do projeto, execute:
     ```sh
     python3 netscan_pro.py
     ```

2. **Escolha de Idioma:**
   - Ao iniciar, escolha o idioma (1 para Inglês, 2 para Português).

3. **Menu Principal:**
   - Escolha entre as opções de ferramentas de rede e engenharia social, ou atualize diretamente do GitHub.

4. **Atualização Automática:**
   - A opção "Atualizar Ferramenta do GitHub" verifica novos arquivos ou código atualizado, exibindo o progresso e reiniciando após a atualização.

### Contribuição
- Contribuições são bem-vindas! Envie suas pull requests no [GitHub](https://github.com/WeverttonBruno/NetScanPro).

### Licença
Este projeto é licenciado sob a [Apache-2.0 License](LICENSE).

Para mais informações e feedback, visite nosso repositório no [GitHub](https://github.com/WeverttonBruno/NetScanPro).

**NetScan Pro Team**