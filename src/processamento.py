import psycopg2

def configurar_banco_e_views():
    conn = None
    try:
        # Conectar ao Banco de Dados
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="senha123" 
        )
        cursor = conn.cursor()

        # Criar a Tabela Base 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tabela_sensor (
                id SERIAL PRIMARY KEY,
                data_leitura DATE DEFAULT CURRENT_DATE,
                temperatura FLOAT NOT NULL
            );
        """)

        cursor.execute("DROP VIEW IF EXISTS vw_resumo_iot CASCADE;")
        cursor.execute("DROP VIEW IF EXISTS vw_alertas_criticos CASCADE;")
        cursor.execute("DROP VIEW IF EXISTS vw_volume_dados CASCADE;")

        # VIEW 1: Resumo Analítico Diário (Média, Máx, Min)
        cursor.execute("""
            CREATE VIEW vw_resumo_iot AS
            SELECT 
                data_leitura, 
                ROUND(AVG(temperatura)::numeric, 2) AS media_temperatura,
                MAX(temperatura) AS temperatura_maxima,
                MIN(temperatura) AS temperatura_minima
            FROM tabela_sensor
            GROUP BY data_leitura;
        """)

        #  VIEW 2: Alertas Críticos (Temperaturas > 25°C)
        cursor.execute("""
            CREATE VIEW vw_alertas_criticos AS
            SELECT * FROM tabela_sensor
            WHERE temperatura > 25.0;
        """)

        # VIEW 3: Volume de Dados (Contagem por dia)
        cursor.execute("""
            CREATE VIEW vw_volume_dados AS
            SELECT data_leitura, COUNT(*) AS total_leituras
            FROM tabela_sensor
            GROUP BY data_leitura;
        """)

        conn.commit()
        print("Sucesso: Views antigas removidas e novas 3 Views criadas com sucesso!")

    except Exception as e:
        print(f" Erro: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    configurar_banco_e_views()