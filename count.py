import os

runDir = "K:\RuHaOTClient"   
async def genStats():
        os.system("cls" if os.name == "nt" else "clear")
        with open(runDir+"\Tempoonline.txt", "r") as f:
            totalTime = 0
            transferCount = 0
            ccTotal = 0
            charSet = set()

            for line in f:
                if "segundos" in line:
                    time_online = int(line.split()[4])
                    if time_online > 2000:
                        continue
                    totalTime += time_online
                    charSet.add(line.split(',')[0]) # Adiciona o nome do personagem ao conjunto
                elif "transferred: true" in line:
                    transferCount += 1
                    ccTotal += 1
                elif "transferred: false" in line:
                    transferCount += 1

            charCount = len(charSet) # Calcula o número de personagens únicos

            if len(charSet) > 0:
                avgTime = totalTime / charCount
                print("Média de tempo online: {} segundos".format(avgTime))
                print("Crystal coins: {}cc".format(ccTotal))
                print("Chars logados: {}".format(charCount))                    
            else:
                print("Nenhum personagem encontrado.")
                print("Crystal coins: {}cc".format(ccTotal))
                print("Chars logados: {}".format(charCount))
