import mysql.connector 
import psutil as p
import socket

hostname_atual = socket.gethostname()

cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Naelu1821@",
    database="AeroGuard")

cur = cnx.cursor()


def select_banco():
    sql = """SELECT 
    h.fkMaquina AS 'ID da Máquina',
    m.Metrica AS 'Métrica',
    m.unidadeMedida AS 'Unidade de Medida',
    h.valorCapturado AS 'Dado Capturado',
    p.limite AS 'Limite Definido',
    h.horario AS 'Horário da Leitura',
    CASE 
        WHEN h.valorCapturado >= p.limite THEN 'Alerta: Crítico!'
        ELSE 'Normal'
    END AS 'Status Alerta'
FROM HistoricoLeitura h
LEFT JOIN Metrica m 
    ON h.fkMetricas = m.idMetrica
LEFT JOIN ParametroMonitoramento p 
    ON h.fkMaquina = p.fkMaquina 
    AND h.fkMetricas = p.fkMetrica
WHERE m.unidadeMedida = '%'   
ORDER BY h.horario DESC;"""

    cur.execute(sql)
    resultado = cur.fetchall()
    return resultado

registros = select_banco()

print("\n" + "="*95)
print(f"{'ID MÁQ.':<8} | {'MÉTRICA':<22} | {'DADO CAPT.':<12} | {'UNIDADE':<8} | {'LIMITE DEF.':<13} | {'STATUS ALERTA'}")
print("="*95)

for linha in registros:
    id_maquina      = linha[0]  
    metrica         = linha[1] 
    unidade_medida  = linha[2]  
    dado_capturado  = linha[3]  
    limite_definido = linha[4] 
    status_alerta   = linha[6]  
    
    dado_formatado = f"{dado_capturado:.1f}" if isinstance(dado_capturado, (int, float)) else dado_capturado

    print(f"{id_maquina:<8} | {metrica:<22} | {dado_formatado:<12} | {unidade_medida:<8} | {limite_definido:<13} | {status_alerta}")

print("="*95 + "\n")

