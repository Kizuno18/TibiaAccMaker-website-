import multiprocessing
import time

runDir = "K:\RuHaOTClient"

def run_task():
    import aiohttp, asyncio, pytesseract, io, random, os
    from bs4 import BeautifulSoup
    from faker import Faker
    from PIL import Image

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

            if charSet:
                avgTime = totalTime / charCount
                minTime = round(avgTime/60, 2)

                print("                         [ALL TIME INFO]")
                print("Média de tempo online: {} minutos".format(minTime))
                print("Crystal coins: {}cc".format(ccTotal))
                print("Chars logados: {}".format(charCount))
            else:
                print("Nenhum personagem encontrado.")
                if (ccTotal >= 100):                    
                 print("Crystal coins: {}kk".format(ccTotal/100))
                else:
                 print("Crystal coins: {}cc".format(ccTotal))                 
                print("Chars logados: {}".format(charCount))



    async def main():
        proxy_url = 'http://p.webshare.io:80'
        proxy_auth = aiohttp.BasicAuth('gbuyvexz-rotate', 'pvyqn3ihdk19')

        def generate_form_data(text, name, email, password, strNumber):
            return {
                'account': strNumber+name.lower().replace(' ', ''),
                'reg_code': text,
                'email': strNumber+email,
                'country': 'br',
                'password': strNumber+password,
                'password2': strNumber+password,
                'name': name,
                'sex': str(random.randint(0, 1)),
                'world': '0',
                'accept_rules': 'true',
                'save': '1',
            }

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    url = 'https://rubinot.com/?account/create'
                    response = await session.get(url, proxy=proxy_url, proxy_auth=proxy_auth)
                    content = await response.read()

                    soup = BeautifulSoup(content, 'html.parser')
                    img_tag = soup.find('td', {'colspan': '2'}).find('img')
                    img_url = img_tag['src']
                    img_response = await session.get(
                        f'https://rubinot.com/{img_url}',
                        proxy=proxy_url,
                        proxy_auth=proxy_auth,
                    )
                    img_data = await img_response.read()

                    img = Image.open(io.BytesIO(img_data))
                    text = pytesseract.image_to_string(img)

                    faker = Faker()
                    name, pw, email = faker.name(), faker.name(), faker.unique.email(domain='gmail.com')
                    special_chars = '!@#$%^&*()_+[];:.<>?'
                    random_special_char = random.choice(special_chars)
                    strNumber = str(random.randint(0, 9999))
                    password = pw.replace(' ', random_special_char)

                    form_data = generate_form_data(text, name, email, password, strNumber)
                    response = await session.post(url, data=form_data, proxy=proxy_url, proxy_auth=proxy_auth)
                    text = await response.text()

                    if 'id="verify"' not in text:
                        env_path = runDir+'\mods\kizuLibrary\.env'
                        with open(env_path, 'r') as f:
                            env_lines = f.readlines()

                        env_lines[6:9] = [f"ACC_NAME={form_data['account']}\n", f"ACC_PASS={form_data['password']}\n", f"ACC_CHARNAME={form_data['name']}\n"]

                        new_path = runDir+'\mods\kizuLibrary\.env.new'
                        with open(new_path, "w") as f:
                            f.writelines(env_lines)

                        os.replace(new_path, env_path)

                    else:
                        print("não foi possivel criar a conta.")
                        break
            except:
                pass

        while True:
            try:                    
                await genStats()
                print("[Login]: "+form_data['name']+"\n")

                return_code = os.system(runDir+'\RuHaOT.exe')  
                await main()
            except:
                pass

    asyncio.run(main())

if __name__ == '__main__':
    processes = []
    for _ in range(5):
        p = multiprocessing.Process(target=run_task)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()