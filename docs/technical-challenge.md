<h1 align="center">
  Desafio Técnico

  (Monitor de Disponibilidade de Servidores)  
</h1>

### Contexto

Considere um ecossistema de software que depende de diversos serviços distribuídos, cada um desempenhando um papel fundamental na estabilidade operacional desse sistema.

Garantir a alta disponibilidade desses servidores é crucial. Portanto, qualquer instabilidade deve ser detectada e reportada em tempo real aos administradores responsáveis.

## O Desafio

Seu objetivo é desenvolver um programa em **Python (`3.9.x`)** chamado **Monitor de Disponibilidade de Servidores**, cujo propósito é monitorar a saúde de uma lista de servidores críticos.

Este programa deve ser executado via linha de comando e receber, como argumento, o caminho (`path`) de um arquivo que contenha a lista dos servidores de interesse a serem monitorados.

O programa deve identificar quando um servidor fica offline e, posteriormente, quando ele retorna ao estado online, enviando notificações por e-mail em ambos os casos para administradores previamente cadastrados.

Deve ser possível testar seu programa através de uma simulação de falhas. Por exemplo, lidar com cenários onde você altera manualmente o estado dos servidores cadastrados, editando os IPs com endereços válidos e inválidos, forçando a alternância entre status online e offline para validar se o envio de e-mails está funcionando corretamente.

## Requisitos Técnicos

### 1. Configuração do Monitor de Disponibilidade de Servidores

O arquivo `monitorConfig.json` deve conter as seguintes informações:

- Configurações do servidor SMTP
- Demais configurações que você julgar necessário

O arquivo `userInfo.json` deve conter as seguintes informações:

- Destinatários que serão notificados
- Cada usuário deve ser cadastrado no formato:

```json
{
  "username": "nome",
  "email": "email_address"
}
```

O arquivo `servers_config.json` deve conter as seguintes informações:

- Mapeamento de todos os servidores que podem ser monitorados
- Cada servidor deve ser cadastrado no formato:

```json
{
  "hostname": "nome",
  "ip": "0.0.0.0",
  "port": 0000
}
```

O arquivo `monitor_list.txt` deve conter as seguintes informações:

- Hostnames dos servidores que serão monitorados em cada execução

Você pode criar outros arquivos de configuração, caso julgue necessário.

### 2. Monitoramento

A execução do monitor deve ser feita via linha de comando, informando o `path` do arquivo `monitor_list.txt`.

O programa deve realizar verificações periódicas (ex.: a cada 60 segundos) sobre a conectividade de cada servidor que será monitorado.

O intervalo entre cada verificação deve ser configurável.

### 3. Notificações

Ao detectar um servidor offline, enviar um e-mail de alerta.

Continuar notificando os administradores cadastrados, a cada N segundos, até que todos os servidores fiquem online novamente.

Ao detectar que um servidor retornou, enviar um e-mail específico informando o restabelecimento da conexão e, neste mesmo e-mail, informar também a lista dos servidores que ainda estão offline.

### 4. Logs

Crie um pacote Python com um módulo específico para registrar os logs das execuções e facilitar eventuais debugs.

O programa deve exibir, na saída padrão, somente os logs do tipo `ERROR`.

Ainda assim, o tipo `ERROR` e os demais tipos, principalmente `DEBUG` e `INFO`, devem ser registrados em um arquivo de log para facilitar futuras análises.

O arquivo de log deve ser rotacionado a cada 24 horas.

## Instruções de Entrega

1. O código deve ser entregue via repositório Git ou arquivo compactado.

2. Inclua um arquivo `README.md` com instruções de instalação das dependências e como executar o monitor.

3. Todos os arquivos descritos em “_Configuração do Monitor de Disponibilidade de Servidores_” devem ser fornecidos como um modelo de teste.
