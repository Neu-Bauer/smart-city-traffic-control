import pandas as pd
import matplotlib.pyplot as plt
import os

ARQUIVO_CSV = 'dados_tcc_trafego.csv' 

def gerar_graficos():
    print("Iniciando análise de dados do tráfego...")

    if not os.path.exists(ARQUIVO_CSV):
        print(f"Erro: O arquivo '{ARQUIVO_CSV}' não foi encontrado.")
        return

    try:
        df = pd.read_csv(ARQUIVO_CSV, sep=None, engine='python', names=['Timestamp', 'Fila_V1', 'Fila_V2', 'Motivo', 'Tempo_Verde'], header=0)
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return

    df['Tempo_Verde'] = df['Tempo_Verde'].astype(str).str.replace('s', '', regex=False).astype(float)

    plt.style.use('ggplot')

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Fila_V1'], label='Via 1 (Carros)', color='#facc15', marker='o')
    plt.plot(df.index, df['Fila_V2'], label='Via 2 (Carros)', color='#d946ef', marker='o')
    
    plt.title('Volume de Veículos no Momento da Troca de Semáforo', fontsize=14, fontweight='bold')
    plt.xlabel('Número da Intervenção (Troca de Sinal)')
    plt.ylabel('Quantidade de Veículos')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.savefig('grafico_1_volume_filas.png', dpi=300)
    print("Gráfico 1 gerado: grafico_1_volume_filas.png")

    plt.figure(figsize=(10, 5))
    plt.bar(df.index, df['Tempo_Verde'], color='#3b82f6', alpha=0.8)
    
    media_tempo = df['Tempo_Verde'].mean()
    plt.axhline(y=media_tempo, color='red', linestyle='--', label=f'Média: {media_tempo:.1f}s')
    
    plt.title('Variação do Tempo de Sinal Verde (Tempo Dinâmico)', fontsize=14, fontweight='bold')
    plt.xlabel('Número da Intervenção (Troca de Sinal)')
    plt.ylabel('Tempo em Segundos (s)')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig('grafico_2_tempo_dinamico.png', dpi=300)
    print("Gráfico 2 gerado: grafico_2_tempo_dinamico.png")

    plt.figure(figsize=(8, 8))
    
    contagem_motivos = df['Motivo'].value_counts()
    
    plt.pie(contagem_motivos, labels=contagem_motivos.index, autopct='%1.1f%%', 
            startangle=140, colors=plt.cm.Paired.colors)
    
    plt.title('Distribuição dos Motivos de Troca de Semáforo', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig('grafico_3_motivos_troca.png', dpi=300)
    print("Gráfico 3 gerado: grafico_3_motivos_troca.png")

    print("\nSucesso! Todos os gráficos foram salvos na sua pasta.")

if __name__ == "__main__":
    gerar_graficos()