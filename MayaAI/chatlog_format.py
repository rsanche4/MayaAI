import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Since this looks at the whole chatlog, please be aware to not copy the same conversation. If it notices you are copying the same convo, it will warn you with which parts of the conversation are already stored. Only run this script daily or once in a while from where you last left off.
def store_conversation_in_database(file_path):
    jsondata = read_json("database.json")
    conversation = []
    with open(file_path, 'r',encoding='utf-8') as file:
        turn = "maya"
        current_contents = file.readlines()
        for line in current_contents:
            print(line)
            if line.strip()=="" or line.strip()=="\n" or line.lower()=="edit\n" or line.lower()=="regenerate\n" or line=="\u00e2\u20ac\u00a2\u00e2\u20ac\u00a2\u00e2\u20ac\u00a2" or line=="  " or "2024" in line:
                continue
            if line.lower()=="stop\n":
                turn = "maya"
                continue
            if line.lower()=="play\n":
                turn = "maya"
            else:
                if turn=="maya":
                    conversation.append({turn: line.rstrip()})
                    turn='rafa'
                else:
                    conversation.append({turn: line.rstrip()})
            #elif line.lower()=="nora\n":
            #    turn = "nora"
            #elif line.lower()=="rafa\n":
            #    turn = "rafa"
            #else:
            #    conversation.append({turn: line.rstrip()})
                    
    jsondata["chat_history"] = conversation
    with open("database.json", 'w') as json_file:
        json.dump(jsondata, json_file, indent=4)

def store_backstory(file_path):
    jsondata = read_json("database.json")
    backstory = ""
    with open(file_path, 'r',encoding='utf-8') as file:
        current_contents = file.readlines()
        backstory = "\n".join(current_contents)
                    
    jsondata["backstory"] = backstory
    with open("database.json", 'w') as json_file:
        json.dump(jsondata, json_file, indent=4)

def store_ltm(file_path):
    jsondata = read_json("database.json")
    ltm = []
    with open(file_path, 'r',encoding='utf-8') as file:
        current_contents = file.readlines()
        for line in current_contents:
            if line=="\n":
                continue
            ltm.append(line)
                    
    jsondata["long_term_memory"] = ltm
    with open("database.json", 'w') as json_file:
        json.dump(jsondata, json_file, indent=4)

file_path = "unparsed_convo.txt" 
file_path2 = "unparsed_backstory.txt"
file_path3 = "unparsed_ltm.txt"

store_conversation_in_database(file_path)
store_backstory(file_path2)
store_ltm(file_path3)