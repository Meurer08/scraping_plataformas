import json
import re
import os

INPUT_DIR = 'resultados_linkedin'
OUTPUT_DIR = 'resultados_linkedin_filtrados'

pattern = re.compile("(?i)artigo|article")

def procuraInfo(fileToOpen, input_dir):
    matches = []
    with open(input_dir+'/'+fileToOpen, encoding='utf-8') as file:
        data = json.load(file)
        subDir = data[0]["publications"]
        for item in subDir:
            for key in item.keys():
                # Usars regex para procurar padrão de palavra Artigo
                if None != pattern.search(item[key]):
                    matches.append(item)
    return matches

listFiles = os.listdir(INPUT_DIR)


if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Pasta '{OUTPUT_DIR}' criada.")

for fileName in listFiles:
    matches = procuraInfo(fileName, INPUT_DIR)
    with open(OUTPUT_DIR+'/'+fileName, 'w', encoding='utf-8') as f:
        # Usa json.dump para serializar e escrever o objeto no arquivo
        json.dump(matches, f, indent=4, ensure_ascii=False)

    
