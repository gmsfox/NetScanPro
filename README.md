O erro que você está encontrando indica que o arquivo `requirements.txt` não está presente no diretório onde você está tentando instalá-lo. Vamos garantir que o arquivo de dependências está corretamente configurado. Aqui estão os passos para resolver esse problema:

### Passo a Passo para Resolver o Problema

1. **Criar o Arquivo `requirements.txt`**
   - No diretório do seu projeto, crie um arquivo chamado `requirements.txt` com o seguinte conteúdo:

     ```txt
     socket
     subprocess
     sys
     time
     os
     datetime
     platform
     webbrowser
     ```

2. **Verificar a Estrutura do Projeto**
   - Certifique-se de que o arquivo `requirements.txt` está no mesmo diretório que o arquivo `netscan_pro.py`.

3. **Instalar as Dependências**
   - Execute o comando para instalar as dependências listadas no `requirements.txt`:
     ```sh
     pip3 install -r requirements.txt
     ```

### Estrutura do Projeto

Certifique-se de que a estrutura do seu projeto está parecida com esta:

```
NetScanPro/
├── netscan_pro.py
├── requirements.txt
```

### Script Completo de Instalação e Execução

Para garantir que tudo está correto, aqui está um script que você pode usar para configurar seu ambiente no Kali Linux:

```sh
# Atualizar pacotes
sudo apt update

# Instalar Python 3 e pip
sudo apt install python3 python3-pip -y

# Instalar Git
sudo apt install git -y

# Clonar o repositório
git clone https://github.com/SeuUsuario/NetScanPro.git
cd NetScanPro

# Criar o arquivo requirements.txt
echo -e "socket\nsubprocess\nsys\ntime\nos\ndatetime\nplatform\nwebbrowser" > requirements.txt

# Instalar as dependências
pip3 install -r requirements.txt

# Executar a ferramenta
python3 netscan_pro.py
```

### README Atualizado

Aqui está o README atualizado, incluindo os passos para criar o `requirements.txt` se ele não estiver presente:

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

5. **Criar o Arquivo `requirements.txt`**
   - Se o arquivo `requirements.txt` não estiver presente, crie-o com:
     ```sh
     echo -e "socket\nsubprocess\nsys\ntime\nos\ndatetime\nplatform\nwebbrowser" > requirements.txt
     ```

6. **Instalar Dependências**
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

### Notas de Atualização - v1.0.0-beta
- **Melhoria na Exibição de Resultados**
  - Resultados organizados e feedback contínuo durante a varredura.
- **Relatório de Resultados**
  - Geração automática de relatório em formato `.txt` na área de trabalho.
  - Mensagem de confirmação exibida no terminal.
- **Navegação Aprimorada**
  - Adição de opção de idioma.
  - Menu atualizado com a opção de saída.
- **Opção de Sair**
  - Novo menu para sair do programa de forma limpa e segura.
- **Correções de Bugs**
  - Correção de erros na geração e salvamento de arquivos de relatório.
  - Melhorias na validação de entrada e manipulação de erros.

### Contribuição
Sinta-se à vontade para contribuir com melhorias e correções. Envie suas pull requests no GitHub.

### Licença
Este projeto está licenciado sob a [Apache-2.0 License](LICENSE).

Para mais informações e feedback, visite nosso repositório no GitHub.

**NetScan Pro Team**
