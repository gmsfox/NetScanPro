## NetScan Pro - README

### Visão Geral
NetScan Pro é uma ferramenta avançada de escaneamento de rede, projetada para identificar portas abertas e fechadas em uma rede especificada. Esta ferramenta é fácil de usar e oferece uma interface de linha de comando intuitiva.

### Funcionalidades
- Varredura de redes e portas
- Relatórios detalhados em formato .txt
- Opção de escolha de idioma
- Feedback contínuo durante a varredura

### Requisitos
- Python 3.6 ou superior

### Instalação

#### Windows
1. **Instalar Python**
   - Baixe e instale Python 3.x em [python.org](https://www.python.org/downloads/).
   - Durante a instalação, certifique-se de marcar a opção "Add Python to PATH".

2. **Clonar o Repositório**
   - Abra o Prompt de Comando (CMD) e execute:
     ```sh
     git clone https://github.com/SeuUsuario/NetScanPro.git
     cd NetScanPro
     ```

3. **Instalar Dependências**
   - Execute o seguinte comando para instalar as dependências necessárias:
     ```sh
     pip install -r requirements.txt
     ```

#### Linux (Kali, Ubuntu, etc.)
1. **Instalar Python**
   - A maioria das distribuições Linux já vem com Python instalado. Verifique se o Python 3 está instalado executando:
     ```sh
     python3 --version
     ```
   - Se o Python 3 não estiver instalado, instale-o com o seguinte comando:
     ```sh
     sudo apt update
     sudo apt install python3
     ```

2. **Instalar pip**
   - Certifique-se de que o `pip` (gerenciador de pacotes do Python) está instalado:
     ```sh
     sudo apt install python3-pip
     ```

3. **Instalar Git**
   - Se o Git não estiver instalado, instale-o com:
     ```sh
     sudo apt install git
     ```

4. **Clonar o Repositório**
   - Abra um terminal e execute:
     ```sh
     git clone https://github.com/SeuUsuario/NetScanPro.git
     cd NetScanPro
     ```

5. **Instalar Dependências**
   - Execute o seguinte comando para instalar as dependências necessárias:
     ```sh
     pip3 install -r requirements.txt
     ```

### Executando o NetScan Pro
1. **Executar o Script**
   - No diretório onde o NetScan Pro foi clonado, execute:
     ```sh
     python3 netscan_pro.py
     ```

### Uso
1. **Escolha de Idioma**
   - Ao iniciar a ferramenta, você será solicitado a escolher o idioma (1 para Português, 2 para Inglês).

2. **Menu Principal**
   - Escolha a opção desejada:
     1. Varredura de rede
     2. Varredura de portas
     3. Varredura completa (rede e portas)
     4. Visitar Instagram
     5. Sair

3. **Relatório de Resultados**
   - Após a varredura, um arquivo de relatório `.txt` será gerado automaticamente na área de trabalho com os resultados detalhados.


### Contribuição
Sinta-se à vontade para contribuir com melhorias e correções. Envie suas pull requests no GitHub.

### Licença
Este projeto está licenciado sob a [Apache-2.0 License](LICENSE).

Para mais informações e feedback, visite nosso repositório no GitHub.

**NetScan Pro Team**
