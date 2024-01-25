import json

with open("DrugInfoItem.jsonl", 'r', encoding='utf-8') as iFile:
    json_data = json.load(iFile)

all_data = ""
for key, value in json_data.items():
    if value:
        print("--------------")
        # print(key)
        print(value["title"])
        all_data += f"# {value['title']}\n\n{value['content']}\n\n"

file_name = f"{json_data['headers']['title']}.md"
with open(file_name, 'w', encoding='utf-8') as oFile:
    oFile.write(all_data)
