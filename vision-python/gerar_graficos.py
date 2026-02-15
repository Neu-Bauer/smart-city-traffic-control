import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("--- INICIANDO ANÁLISE DE DADOS ---")
    
    # 1. Carregar os dados
    try:
        df = pd.read_csv('dados_tcc_trafego.csv', sep=';')
        print("✅ Dados carregados com sucesso!\n")
    except FileNotFoundError:
        print("❌ Arquivo 'dados_tcc_trafego.csv' não encontrado. Rode o main.py primeiro.")
        return

    coluna_v1 = 'Fila_Via_1'
    coluna_v2 = 'Fila_Via_2'

    # ==========================================
    # GRÁFICO 1: LINHAS (EVOLUÇÃO DAS FILAS)
    # ==========================================
    plt.figure(figsize=(10, 5))
    
    plt.plot(df.index, df[coluna_v1], label='Via 1 (Amarelo)', color='orange', marker='o', linestyle='-')
    plt.plot(df.index, df[coluna_v2], label='Via 2 (Magenta)', color='purple', marker='x', linestyle='-')

    plt.title('Evolução do Volume de Carros por Via', fontsize=14, fontweight='bold')
    plt.xlabel('Interações (Tempo Real)', fontsize=12)
    plt.ylabel('Quantidade de Veículos na Fila', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # NOVA LINHA: Trava o eixo Y no zero (remove números negativos)
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    
    # Salvar Gráfico 1
    nome_imagem1 = 'grafico_filas.png'
    plt.savefig(nome_imagem1, dpi=300)
    print(f"✅ Gráfico 1 (Linhas) salvo como: {nome_imagem1}")

    # ==========================================
    # GRÁFICO 2: PIZZA (TEMPO DE SINAL VERDE)
    # ==========================================
    # O Pandas vai contar quantas vezes a IA decidiu dar prioridade para cada via
    contagem_v1 = df['Decisao_Tomada'].astype(str).str.contains('Via 1').sum()
    contagem_v2 = df['Decisao_Tomada'].astype(str).str.contains('Via 2').sum()
    
    plt.figure(figsize=(8, 8))
    labels = ['Via 1 (Sinal Verde)', 'Via 2 (Sinal Verde)']
    valores = [contagem_v1, contagem_v2]
    cores = ['orange', 'purple']
    
    if sum(valores) > 0:
        # autopct='%1.1f%%' calcula e mostra a porcentagem automaticamente
        plt.pie(valores, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90, 
                textprops={'fontsize': 12, 'fontweight': 'bold'})
        plt.title('Tempo de Prioridade do Semáforo por Via', fontsize=14, fontweight='bold')
        
        # Salvar Gráfico 2
        nome_imagem2 = 'grafico_pizza_prioridade.png'
        plt.savefig(nome_imagem2, dpi=300)
        print(f"✅ Gráfico 2 (Pizza) salvo como: {nome_imagem2}")
    else:
        print("⚠️ Sem dados suficientes para o gráfico de pizza.")

    # Mostra os gráficos na tela (Vai abrir o primeiro. Feche a janela para ver o segundo!)
    print("\nFeche a janela do primeiro gráfico para visualizar o segundo.")
    plt.show()

if __name__ == "__main__":
    main()