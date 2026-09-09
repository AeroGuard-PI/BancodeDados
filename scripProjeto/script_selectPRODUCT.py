import mysql.connector 
import psutil as p
import socket
import time

hostname_atual = socket.gethostname()

cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="nicolas",
    password="12345",
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
ORDER BY h.horario DESC
limit 3;"""

    cur.execute(sql)
    resultado = cur.fetchall()
    return resultado
while True:
    registros = select_banco()

    print("\n" + "="*95)
    print(f"{'HORÁRIO DO REGISTRO':<20} | {'MÉTRICA':<22} | {'DADO CAPT.':<12} | {'UNIDADE':<8} | {'LIMITE DEF.':<13} | {'STATUS ALERTA'}")
    print("="*95)

    for linha in registros:
        metrica         = linha[1] 
        unidade_medida  = linha[2]  
        dado_capturado  = linha[3]  
        limite_definido = linha[4] 
        horario         = linha[5]
        status_alerta   = linha[6]  
        
        dado_formatado = f"{dado_capturado:.1f}" if isinstance(dado_capturado, (int, float)) else dado_capturado
        horario_formatado = horario.strftime("%d/%m/%Y %H:%M:%S")

        print(f"({horario_formatado:<19} | {metrica:<22} | {dado_formatado:<12} | {unidade_medida:<8} | {limite_definido:<13} | {status_alerta}")

    print("="*95 + "\n")
    time.sleep(1)

