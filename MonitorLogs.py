#Yan Lopes de Barros da Silva / Victor Vieira de Souza / Gabriel Novaes Chagas de Oliveira

import random
import datetime


def menu():

    nomeArquivo = "log.txt"

    while True:

        print("\nMonitor LogPy")
        print("1 - Gerar Logs")
        print("2 - Analisar Logs")
        print("3 - Gerar e Analisar Logs")
        print("4 - Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":

            try:
                quantidade = int(input("Quantidade de logs: "))
                gerarArquivo(quantidade, nomeArquivo)
            except:
                print("Quantidade inválida")

        elif opcao == "2":

            analisarLog(nomeArquivo)

        elif opcao == "3":

            try:
                quantidade = int(input("Quantidade de logs: "))
                gerarArquivo(quantidade, nomeArquivo)
                analisarLog(nomeArquivo)
            except:
                print("Quantidade inválida")

        elif opcao == "4":

            print("Saindo...")
            break


def gerarArquivo(quantidade, nomeArquivo):

    with open(nomeArquivo, "w", encoding="utf-8") as file:

        for i in range(quantidade):

            file.write(montarLog(i) + "\n")

    print("Logs gerados")


def montarLog(i):

    data = gerar_data_hora(i)
    ip = gerar_ip(i)
    recurso = gerar_recurso(i)
    metodo = gerar_metodo(recurso)
    status = gerar_status(i, recurso)
    tempo = gerar_tempo(i)
    agente = gerar_agente(i)

    return f"[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - 512B - HTTP/1.1 - {agente} - /home"


def gerar_data_hora(i):

    base = datetime.datetime(2026, 3, 30, 22, 8, 0)

    data = datetime.timedelta(seconds=i * random.randint(5, 20))

    return (base + data).strftime("%d/%m/%Y %H:%M:%S")


def gerar_ip(i):

    r = random.randint(1, 5)

    if r == 1:
        return "192.168.0.12"
    elif r == 2:
        return "192.168.1.100"
    elif r == 3:
        return "192.168.2.4"
    elif r == 4:
        return "172.16.0.1"
    else:
        return "10.0.0.50"


def gerar_recurso(i):

    if 5 <= i <= 9:
        return "/login"

    if 50 <= i <= 53:
        return "/admin"

    if 60 <= i <= 62:
        return "/pagina-inexistente"

    r = random.randint(1, 4)

    if r == 1:
        return "/home"
    elif r == 2:
        return "/login"
    elif r == 3:
        return "/admin"
    else:
        return "/produtos"


def gerar_metodo(recurso):

    if recurso == "/login":
        return "POST"

    return "GET"


def gerar_status(i, recurso):

    if recurso == "/pagina-inexistente":
        return 404

    if recurso == "/admin":
        return 403

    if i % 15 == 0:
        return 500

    return 200


def gerar_tempo(i):

    if 30 <= i <= 34:
        return 120 + (i - 30) * 180

    if i % 7 == 0:
        return random.randint(800, 1200)

    return random.randint(80, 450)


def gerar_agente(i):

    if 40 <= i <= 46:
        return "Googlebot"

    r = random.randint(1, 3)

    if r == 1:
        return "Chrome"
    elif r == 2:
        return "Firefox"
    else:
        return "Safari"


def extrair_campos_linha(linha):

    fim_data = linha.find("]")

    data_hora = linha[1:fim_data]

    rest = linha[fim_data + 1:].strip()

    pos = rest.find(" - ")
    ip = rest[:pos].strip()
    rest = rest[pos + 3:].strip()

    pos = rest.find(" - ")
    metodo = rest[:pos].strip()
    rest = rest[pos + 3:].strip()

    pos = rest.find(" - ")
    status = int(rest[:pos].strip())
    rest = rest[pos + 3:].strip()

    pos = rest.find(" - ")
    recurso = rest[:pos].strip()
    rest = rest[pos + 3:].strip()

    pos_ms = rest.find("ms")
    tempo = int(rest[:pos_ms].strip())

    return data_hora, ip, metodo, status, recurso, tempo


def classificar_tempo(tempo):

    if tempo < 200:
        return "rapido"

    elif tempo <= 799:
        return "normal"

    else:
        return "lento"


def classificar_estado_final(disponibilidade, lentos, total, forca, bot, falha):

    if falha >= 1 or disponibilidade < 70:
        return "CRÍTICO"

    elif disponibilidade < 85 or lentos > total // 3:
        return "INSTÁVEL"

    elif disponibilidade < 95 or forca > 0 or bot > 0:
        return "ATENÇÃO"

    else:
        return "SAUDÁVEL"


def analisarLog(nomeArquivo):

    try:

        with open(nomeArquivo, "r", encoding="utf-8") as file:

            total_acessos = 0
            total_sucessos = 0
            total_erros = 0
            total_erros_criticos = 0

            soma_tempos = 0
            maior_tempo = 0
            menor_tempo = 999999

            rapidos = 0
            normais = 0
            lentos = 0

            count_200 = 0
            count_403 = 0
            count_404 = 0
            count_500 = 0

            prev_ip = ""
            prev_tempo = -1

            streak_login_403 = 0
            streak_500 = 0
            streak_increase = 0
            streak_bot = 0

            prev_ip_bot = ""

            num_forca_bruta = 0
            ultimo_ip_forca = "Nenhum"

            num_degradacao = 0
            num_falha_critica = 0

            num_bot = 0
            ultimo_ip_bot = "Nenhum"

            total_rotas_sensiveis = 0
            total_falhas_sensiveis = 0

            count_admin = 0

            for linha in file:

                linha = linha.strip()

                if not linha:
                    continue

                data, ip, metodo, status, recurso, tempo = extrair_campos_linha(linha)

                total_acessos += 1

                soma_tempos += tempo

                if tempo > maior_tempo:
                    maior_tempo = tempo

                if tempo < menor_tempo:
                    menor_tempo = tempo

                tipo = classificar_tempo(tempo)

                if tipo == "rapido":
                    rapidos += 1
                elif tipo == "normal":
                    normais += 1
                else:
                    lentos += 1

                if status == 200:
                    total_sucessos += 1
                    count_200 += 1
                else:
                    total_erros += 1

                    if status == 403:
                        count_403 += 1
                    elif status == 404:
                        count_404 += 1
                    elif status == 500:
                        count_500 += 1
                        total_erros_criticos += 1

                if recurso == "/admin":
                    count_admin += 1

                if recurso == "/admin" or recurso == "/pagina-inexistente":

                    total_rotas_sensiveis += 1

                    if status != 200:
                        total_falhas_sensiveis += 1

                if ip == prev_ip and recurso == "/login" and status == 403:

                    streak_login_403 += 1

                    if streak_login_403 == 3:

                        num_forca_bruta += 1
                        ultimo_ip_forca = ip

                else:

                    streak_login_403 = 0

                if status == 500:

                    streak_500 += 1

                    if streak_500 == 3:
                        num_falha_critica += 1

                else:

                    streak_500 = 0

                if prev_tempo != -1 and tempo > prev_tempo:

                    streak_increase += 1

                    if streak_increase == 3:
                        num_degradacao += 1

                else:

                    streak_increase = 0

                prev_tempo = tempo

                if ip == prev_ip_bot:

                    streak_bot += 1

                    if streak_bot == 5:
                        num_bot += 1
                        ultimo_ip_bot = ip

                else:

                    streak_bot = 1
                    prev_ip_bot = ip

                prev_ip = ip

            disponibilidade = (total_sucessos / total_acessos) * 100
            taxa_erro = (total_erros / total_acessos) * 100
            tempo_medio = soma_tempos / total_acessos

            estado = classificar_estado_final(
                disponibilidade,
                lentos,
                total_acessos,
                num_forca_bruta,
                num_bot,
                num_falha_critica
            )

            print("\n============================================================")
            print("RELATÓRIO FINAL - MONITOR LOGPY")
            print("============================================================")

            print("Total de acessos:", total_acessos)
            print("Total de sucessos:", total_sucessos)
            print("Total de erros:", total_erros)
            print("Total de erros críticos:", total_erros_criticos)

            print("Disponibilidade:", f"{disponibilidade:.2f}%")
            print("Taxa de erro:", f"{taxa_erro:.2f}%")

            print("Tempo médio:", f"{tempo_medio:.2f} ms")
            print("Maior tempo:", maior_tempo)
            print("Menor tempo:", menor_tempo)

            print("Acessos rápidos:", rapidos)
            print("Acessos normais:", normais)
            print("Acessos lentos:", lentos)

            print("Status 200:", count_200)
            print("Status 403:", count_403)
            print("Status 404:", count_404)
            print("Status 500:", count_500)

            print("Total de força bruta:", num_forca_bruta)
            print("Último IP força bruta:", ultimo_ip_forca)

            print("Acessos indevidos ao /admin:", count_admin)

            print("Eventos de degradação:", num_degradacao)
            print("Eventos de falha crítica:", num_falha_critica)

            print("Suspeitas de bot:", num_bot)
            print("Último IP bot:", ultimo_ip_bot)

            print("Acessos rotas sensíveis:", total_rotas_sensiveis)
            print("Falhas rotas sensíveis:", total_falhas_sensiveis)

            print("Estado final do sistema:", estado)

            print("============================================================")

    except FileNotFoundError:

        print("Arquivo não encontrado")


menu()