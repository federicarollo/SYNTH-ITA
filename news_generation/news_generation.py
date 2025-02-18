from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import login
#from accelerate import disk_offload

import os
import torch
import json
from datetime import datetime

login(token="your_token")


model_id = "meta-llama/Meta-Llama-3-8B-Instruct"


quantization = False

tokenizer = AutoTokenizer.from_pretrained(model_id)
if quantization:
    # use quantization
    quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16, llm_int8_enable_fp32_cpu_offload=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=quantization_config, device_map="auto")
else:
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
    # model.to('cuda')


examples_set_filename = "example_set.json"
annotations_filename = "created_annotations.json"

# Load example set
with open(examples_set_filename, "r", encoding='utf-8') as f:
    examples = json.load(f)

# Load news items to submit to the model
with open(annotations_filename, "r", encoding='utf-8') as f:
    annotations = json.load(f)

few_shot = [
        {
            "role": "system",
            "content": f"""
Immagina di essere un giornalista che riceve le informazioni in merito ad un furto in un JSON, scrivi una notizia in lingua italiana, in stile giornalistico, utilizzando le informazioni fornite nel JSON.  Aggiungi un contesto, una dinamica all'avvenimento, senza aggiungere ulteriori dettagli sulle entità descritte nel JSON.
La notizia deve includere tutte le informazioni disponibili nel JSON così come sono, senza riformulazioni.

Il JSON può includere informazioni nei seguenti campi:
  • AUT: Lista di sottoliste di stringhe, ciascuna delle quali contiene stringhe descriventi un singolo autore del furto (es. nome, età, sesso, occupazione, precedenti penali). Se il campo è vuoto, descrivere l'autore con termini generici come "ladro", "malvivente", "criminale" etc.
  • AUTG: Lista di stringhe descriventi un intero gruppo criminale.
  • OBJ: Lista di sottoliste di stringhe, ciascuna delle quali contiene stringhe descriventi un singolo oggetto rubato, con quantità se specificata. Tutti gli oggetti devono essere menzionati nel testo generato.
  • VIC: Lista di sottoliste di stringhe, ciascuna delle quali contiene stringhe descriventi una singola vittima del furto (es. nome, età, occupazione). Se vuoto, usare termini generici come "vittima", "malcapitato" etc.
  • VICG: Lista di stringhe descriventi un intero gruppo di vittime.
  • PAR: Contiene la ragione sociale di un'attività commerciale, ente pubblico o associazione colpita dal furto.
  • LOC: Luogo del furto (es. città, via, tipo di struttura).

Regole logiche:
  • Se AUTG contiene del testo questo deve essere usato per descrivere un gruppo criminale, mentre il contenuto di AUT, se presente, descrive i singoli autori del gruppo.
  • Se VICG contiene del testo questo deve essere usato per descrivere un gruppo di vittime, mentre il contenuto di VIC descrive le singole vittime.
"""
        }
]

# select example
examples_indices = [2, 5, 4, 9]

for index in examples_indices:
    few_shot.append({
                        "role": "user",
                        "content": json.dumps(examples[index]['annotation'])
    })

    few_shot.append({
                        "role": "assistant",
                        "content": json.dumps(examples[index]['text'])
    })


dataset = []

for annotation in annotations:

    prompt = few_shot + [{"role": "user", "content": json.dumps(annotation)}]

    encodeds = tokenizer.apply_chat_template(prompt, return_tensors="pt")
    model_inputs = encodeds.to('cuda')
    outputs = model.generate(model_inputs, max_new_tokens=2000, do_sample = True, temperature=0.6)

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)

    dataset.append({
                        "completion": decoded,
                        "annotation": annotation
    })

    with open(f"generated_dataset.json", "w", encoding='utf-8') as f:
        json.dump(dataset, f)
