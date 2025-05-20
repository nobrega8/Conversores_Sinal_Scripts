# 🤝 Contribuir para o Projeto

Obrigado por considerares contribuir para a Calculadora de Conversores de Sinal da FCT Nova! 🎓  
Este projeto foi criado com o objetivo de apoiar a comunidade académica e pode ser facilmente expandido para suportar mais modelos de calculadora.

## 🧩 Como Contribuir

### 1. Adapta o Código Base

O ficheiro [`source.py`](https://github.com/nobrega8/Conversores_Sinal_Scripts/blob/main/source.py), localizado na raiz do repositório, contém a implementação genérica das funcionalidades da calculadora.

Podes usá-lo como base para adaptar o código a um novo modelo de calculadora. Por exemplo, ajustar a forma de input/output, limitar funcionalidades ou modificar a interface consoante as restrições do dispositivo.

### 2. Cria o Script Adaptado

Depois de adaptares o `source.py`, deves criar um novo ficheiro Python na pasta correspondente ao fabricante e modelo da calculadora:

```
calculadoras/
│
├── texas/
│   ├── tinspirecxiit.py  ← Exemplo: Texas Nspire CX II-T
│
├── casio/
│   ├── casiofxcg50.py    ← Exemplo: Casio FX-CG50
```

Usa nomes descritivos e coerentes com os já existentes.

### 3. Testa o Script

Garante que:

- Todas as funcionalidades relevantes funcionam corretamente no modelo escolhido.
- Estão descritas eventuais limitações específicas no cabeçalho do ficheiro.
- O script segue o estilo do repositório.

### 4. Atualiza a Tabela no README

Se adicionares suporte para uma nova calculadora, não te esqueças de atualizar a tabela principal no `README.md`, indicando:

- Nome do modelo
- Estado de compatibilidade (✅ / ⚠️ / ❌)
- Problemas conhecidos
- Versão mais recente

### 5. Submete o Pull Request

- Cria um *fork* do repositório.
- Faz as alterações no teu *fork*.
- Cria um *pull request* com uma breve descrição do modelo e das alterações feitas.

---

## 📬 Contacto

Se tiveres dúvidas, sugestões ou ideias para funcionalidades novas, podes abrir um *issue* ou contactar diretamente os desenvolvedores.

---

**Juntos conseguimos tornar esta ferramenta mais completa e útil para todos!** 🙌  
