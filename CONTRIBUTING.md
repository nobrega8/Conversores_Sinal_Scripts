# Contribuir para o Projeto

Contribuições para a Calculadora de Conversores de Sinal da FCT Nova são bem-vindas. O projeto foi criado para apoiar a comunidade académica e pode ser expandido para suportar mais modelos de calculadora.

## Como Contribuir

### 1. Adaptar o Código Base

O ficheiro [`source.py`](https://github.com/nobrega8/Conversores_Sinal_Scripts/blob/main/source.py), na raiz do repositório, contém a implementação genérica das funcionalidades. Use-o como base para adaptar o código a um novo modelo, ajustando input/output, limitando funcionalidades ou modificando a interface consoante as restrições do dispositivo.

### 2. Criar o Script Adaptado

Crie um novo ficheiro Python na pasta correspondente ao fabricante e modelo:

```
calculadoras/
│
├── texas/
│   ├── tinspirecxiit.py  ← Exemplo: Texas Nspire CX II-T
│
├── casio/
│   ├── casiofxcg50.py    ← Exemplo: Casio FX-CG50
```

Use nomes descritivos e coerentes com os já existentes.

### 3. Testar o Script

Certifique-se de que:

- Todas as funcionalidades relevantes funcionam corretamente no modelo escolhido.
- Eventuais limitações específicas estão descritas no cabeçalho do ficheiro.
- O script segue o estilo do repositório.

### 4. Atualizar a Tabela no README

Se adicionar suporte para uma nova calculadora, atualize a tabela no `README.md` com:

- Nome do modelo
- Estado de compatibilidade
- Problemas conhecidos
- Versão mais recente

### 5. Submeter o Pull Request

- Faça fork do repositório.
- Aplique as alterações no seu fork.
- Abra um pull request com uma breve descrição do modelo e das alterações feitas.

---

## Contacto

Para dúvidas, sugestões ou novas funcionalidades, abra um *issue* ou contacte diretamente os desenvolvedores.
