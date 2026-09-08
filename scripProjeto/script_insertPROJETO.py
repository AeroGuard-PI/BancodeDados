import mysql.connector 
import psutil as p
from datetime import datetime, date
import time
import socket

hostname_atual = socket.gethostname()

cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="nicolas",
    password="12345",
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

def salvar_dado(fkMetricas, fkMaquina, valorCapturado, horario):
    sql = "INSERT INTO historicoLeitura (fkMetricas, fkMaquina, valorCapturado, horario)  VALUES (%s, %s, %s, %s)"
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
    
    discoPorcentagem = p.disk_usage('C://').percent
    salvar_dado("3", fk_maquina, discoPorcentagem, horarioAtual)

    espacoDisco = round(p.disk_usage("C://").total / (1024**3), 2)
    salvar_dado("8", fk_maquina, espacoDisco, horarioAtual)
    
    print("Métricas capturadas e enviadas ao AeroGuard!")
    
    time.sleep(10)