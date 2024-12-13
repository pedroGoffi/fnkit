
# fnkit - Biblioteca Funcional para Python

## Descrição
O **fnkit** é uma biblioteca Python que implementa o paradigma funcional para facilitar a criação de programas mais limpos, legíveis e reusáveis. Ele fornece uma coleção de ferramentas funcionais para operações como mapeamento, filtragem e redução de dados, além de facilitar o manejo de resultados e erros.

## Funcionalidades
Aqui estão as principais funcionalidades e classes oferecidas pelo **fnkit**:

### 1. `ChainedResult`
- **Descrição**: Classe que representa um resultado encadeado para operações funcionais. Utilizada para gerenciar resultados de funções de forma limpa e legível.
- **Atributos**:
  - `value`: Valor do resultado se a operação foi bem-sucedida.
  - `error`: Erro ocorrido durante a operação, se presente.
- **Métodos**:
  - `map_value(func)`: Aplica uma função ao valor do resultado se existir.
  - `or_else(fallback)`: Executa uma função de fallback se o resultado falhar.
  - `Await()`: Método assíncrono para aguardar a conclusão do resultado.
  - `map_async(func)`: Aplica uma função assíncrona ao valor do resultado se existir.
  
### Exemplo de Uso:
```python
result = ChainedResult(value=42)
result = result.map_value(lambda x: x * 2)
result = result.or_else(lambda r: ChainedResult(error="Fallback"))

if result.error:
    print(f"Erro: {result.error}")
else:
    print(f"Sucesso: {result.value}")
```

### 2. `AsyncResult`
- **Descrição**: Classe que representa um resultado assíncrono. Ideal para operações assíncronas que podem falhar e necessitam ser tratadas corretamente.
- **Atributos**:
  - `computation`: Função assíncrona original que é esperada.
  - `value`: Valor do resultado se a operação foi bem-sucedida.
  - `error`: Erro ocorrido durante a operação, se presente.
- **Métodos**:
  - `Await()`: Método assíncrono para aguardar a conclusão do resultado.
  - `map(func)`: Aplica uma função ao valor do resultado se existir.
  - `map_err(func)`: Aplica uma função ao erro se presente.
  - `or_else(fn)`: Executa uma função de fallback se o resultado falhar.
  - `unwrap()`: Retorna o valor se bem-sucedido, lança uma exceção se falhar.
  - `expect(msg)`: Retorna o valor, lançando uma exceção com uma mensagem se falhar.
  - `map_async(func)`: Aplica uma função assíncrona ao valor do resultado se existir.

### Exemplo de Uso:
```python
async def fetch_data():
    return 42

result = AsyncResult(fetch_data())

processed_result = await result.map_async(lambda x: x * 2)

if processed_result.error:
    print(f"Erro: {processed_result.error}")
else:
    print(f"Sucesso: {processed_result.value}")
```

### 3. Funções Funcionais
- **`chain(result, func)`**: Encadeia uma função a ser aplicada se o resultado for bem-sucedido.
- **`map_value(result, func)`**: Aplica uma função ao valor do resultado se existir.
- **`or_else(result, fallback)`**: Retorna um resultado de fallback se o resultado inicial falhar.

### Exemplo de Uso:
```python
result = ChainedResult(value=42)
result = map_value(result, lambda x: x * 2)
result = or_else(result, lambda r: ChainedResult(error="Fallback"))

if result.error:
    print(f"Erro: {result.error}")
else:
    print(f"Sucesso: {result.value}")
```

## Instalando o fnkit
Para instalar o **fnkit**, você pode utilizar o `pip`:

```bash
pip install fnkit
```

## Contribuindo
Contribuições são bem-vindas! Se tiver ideias, bugs para reportar ou melhorias para sugerir, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).
```

Este README fornece uma visão geral das funcionalidades do **fnkit** e mostra exemplos práticos de como usar as classes e funções implementadas.