import subprocess, os, json, re, tkinter as tk
from urllib.parse import urlparse
from tkinter import ttk

def get_chats():
    res = subprocess.run(["sigexport", "--list-chats"], capture_output=True, text=True)
    return res.stdout.strip().split("|")

root = tk.Tk()
root.title("Select Chat")
chats = get_chats()
chat_var = tk.StringVar(value=chats[0] if chats else "")
ttk.Label(root, text="Choose a chat:").pack(padx=10, pady=5)
ttk.OptionMenu(root, chat_var, chat_var.get(), *chats).pack(padx=10, pady=5)
ttk.Button(root, text="OK", command=root.destroy).pack(padx=10, pady=5)
root.mainloop()

chat = chat_var.get().replace(" ", "")

subprocess.run(["sigexport", f"--chats={chat}", "--overwrite", os.path.join(os.path.dirname(__file__), "urls")], check=True)


with open(os.path.join(os.path.dirname(__file__), "urls",chat,"data.json"), "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
    url_pattern = re.compile(
        r'(?:(?:https?|ftp)://|www\.)[^\s<>()"\']+'
        r'|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^\s<>()"\']*)?',
        re.IGNORECASE
    )
    path = os.path.join(os.path.dirname(__file__), "urls",chat,"urls.json")
    urls = [u for d in data for u in url_pattern.findall(d["body"])]
    grouped = {}; [grouped.setdefault(urlparse(u).netloc or urlparse("http://" + u).netloc, []).append(u) for u in urls]
    urls_new = json.load(open(path)) if os.path.exists(path) else {}; urls_new.update(grouped)
    
    json.dump(urls_new, open(path, "w"), indent=2)










