import mysql.connector 
import psutil as p
from datetime import datetime, date
import time
import socket

hostname_atual = socket.gethostname()

cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Naelu1821@",
    database="AeroGuard")

cur = cnx.cursor()

def obter_id_maquina(hostname):
    sql = "SELECT idMaquina FROM Maquina WHERE hostname = %s"
    cur.execute(sql, (hostname,))
    resultado = cur.fetchone()

    print(resultado)
    if resultado:
        return resultado[0]
    else:
        raise ValueError(f"Máquina com hostname '{hostname}' não foi encontrada na tabela Maquina.")

fk_maquina = obter_id_maquina(hostname_atual)

def verificacao_limites(fkMaquina):
    sql= "SELECT fkMaquina FROM ParametroMonitoramento WHERE fkMaquina = %s"
    cur.execute(sql, (fkMaquina,))
    resultado =cur.fetchone()
    cur.fetchall() 

    return resultado is not None

def limites_default(fkMaquina, fkMetrica, limite):
    sql = "INSERT INTO ParametroMonitoramento (fkMaquina, fkMetrica, limite) VALUES (%s, %s, %s)"
    cur.execute(sql, (fkMaquina, fkMetrica, limite))
    cnx.commit()

dados_metricas = [
    (1, 80.0),  
    (2, 80.0),  
    (3, 85.0),  
    (4, 3.5),   
    (5, 4.0),  
    (6, 16.0), 
    (7, 2.0),   
    (8, 20.0)   
]

if not verificacao_limites(fk_maquina):
    print(f"Configurando os limites padrões para a máquina {fk_maquina}...")
    for fk_metrica, limite in dados_metricas:
        limites_default(fk_maquina, fk_metrica, limite)
else:
    print(f"Limites já configurados anteriormente para a máquina {fk_maquina}.")

def salvar_dado(fkMetricas, fkMaquina, valorCapturado, horario):
    sql = "INSERT INTO HistoricoLeitura (fkMetricas, fkMaquina, valorCapturado, horario)  VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (fkMetricas, fkMaquina, float(valorCapturado), horario))
    cnx.commit()

while True:
    agora = datetime.now()
    horarioAtual = agora.strftime("%Y-%m-%d %H:%M:%S")    
    cpuPorcentagem = p.cpu_percent(interval=1)
    salvar_dado("1", fk_maquina, cpuPorcentagem, horarioAtual)

    cpuFrequencia = p.cpu_freq().current
    salvar_dado("4", fk_maquina, cpuFrequencia, horarioAtual)
    
    ramPorcentagem = p.virtual_memory().percent
    salvar_dado("2", fk_maquina, ramPorcentagem, horarioAtual)
    
    memoriaVirtual = round(p.virtual_memory().used / (1024**3), 2)
    salvar_dado("5", fk_maquina, memoriaVirtual, horarioAtual)
    
    memoriaTotal = round(p.virtual_memory().total / (1024**3), 2)
    salvar_dado("6", fk_maquina, memoriaTotal, horarioAtual)
    
    memoriaDisponivel = round(p.virtual_memory().available / (1024**3), 2)
    salvar_dado("7", fk_maquina, memoriaDisponivel, horarioAtual)
    
    discoPorcentagem = p.disk_usage('/').percent
    salvar_dado("3", fk_maquina, discoPorcentagem, horarioAtual)

    espacoDisco = round(p.disk_usage("/").total / (1024**3), 2)
    salvar_dado("8", fk_maquina, espacoDisco, horarioAtual)
    
    print("Métricas capturadas e enviadas ao AeroGuard!")
    
    time.sleep(10)