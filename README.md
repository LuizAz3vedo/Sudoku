## **🧩 Visualizando a Lógica do Sudoku com Grafos e Animação! 🎥**

Você já parou para pensar como um **Sudoku** é resolvido? 🤔 Ele pode ser visto como um **problema de grafos**, onde cada célula do tabuleiro é um nó, e as restrições (linhas, colunas e blocos) são arestas que conectam esses nós.

🎯 **Neste projeto, criei uma animação que mostra o Sudoku sendo resolvido enquanto o grafo de restrições se reorganiza!**

✅ **O que esse projeto faz?**  
🔹 Gera o grafo do Sudoku, conectando as células que possuem restrições entre si.  
🔹 Mostra o preenchimento das células do Sudoku de forma dinâmica.  
🔹 Destaca tentativas erradas em vermelho antes da correção.  
🔹 Usa um solver eficiente com heurísticas para resolver rapidamente o tabuleiro.

🚀 **Tecnologias usadas:**  
📌 Python (Matplotlib, NetworkX)  
📌 Algoritmos de backtracking com heurísticas  
📌 Animação interativa para visualizar o processo

### **1️⃣ Construção do Grafo de Restrições**

- Cada célula do Sudoku é um **nó** do grafo.
- As **arestas** conectam células que compartilham **linha, coluna ou bloco 3x3**.
- O grafo começa com um layout circular e depois se ajusta para um layout em grade 9x9.

### **2️⃣ Resolução do Sudoku (Backtracking com heurísticas)**

A solução do Sudoku é feita com **Backtracking otimizado**:

✅ **Escolha da melhor célula** → Em vez de preencher aleatoriamente, usamos **heurísticas** para escolher a célula com menos opções possíveis. Isso reduz drasticamente o número de tentativas.

✅ **Tentativas de valores errados** → Para deixar a animação mais interessante, o solver **às vezes erra propositalmente** antes de corrigir, gerando erros visuais em vermelho.

✅ **Backtracking eficiente** → Se um número não funcionar, ele é removido e a busca continua.

### **3️⃣ Animação**

- O código mostra a transição do **grafo circular** para a **grade 9x9**.
- Cada número novo aparece na célula correspondente.
- Números errados aparecem **em vermelho** antes de serem corrigidos.
- O grafo exibe conexões coloridas:
    - **Linhas (vermelho)**
    - **Colunas (azul)**
    - **Blocos 3x3 (verde)**


## **🎓 Educação e Ensino**

1. **Visualização de Restrições**
    
    - O grafo ajuda a **entender as regras do Sudoku** de forma intuitiva.
    - Mostra visualmente como **células influenciam umas às outras**, facilitando o aprendizado.
2. **Treinamento de Algoritmos de Busca**
    
    - Demonstra o **backtracking otimizado** na prática.
    - Pode ser usado para ensinar **heurísticas e otimização de busca**.
3. **Animação Didática**
    
    - Útil para professores e estudantes de **ciência da computação** e **inteligência artificial**.
