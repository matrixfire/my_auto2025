import sys
import webbrowser

def ai(n=1, link="https://chatgpt.com/"):
    for _ in range(n):
        webbrowser.open(link)
        try:
            webbrowser.get("C:/Program Files/Mozilla Firefox/firefox.exe %s").open("https://www.linkedin.com/feed/")
        except Exception as e:
            print(f"Failed to open LinkedIn in Firefox: {e}")

def ai2():
    links = [
        "https://www.bing.com/chat",
        "https://yiyan.baidu.com/",
        "https://kimi.moonshot.cn/chat",
        "https://chatglm.cn/main/alltoolsdetail",
        "https://cp.baidu.com/?utm_source=ai-bot.cn",
        "https://gemini.google.com/",
        "https://www.doubao.com/",
    ]
    for link in links:
        webbrowser.open(link)

def sns():
    webbrowser.open("https://www.facebook.com/")
    webbrowser.get("C:/Program Files/Mozilla Firefox/firefox.exe %s").open("https://www.youtube.com/")
    webbrowser.get("C:/Program Files/Mozilla Firefox/firefox.exe %s").open("https://www.linkedin.com/feed/")


if __name__ == "__main__":
    args = sys.argv[1:]  # Skip the first argument which is the script filename
    
    if args[0] == "ai":
        if len(args) == 1:
            ai()
        elif len(args) == 2:
            try:
                n = int(args[1])
                ai(n)
            except ValueError:
                print("Invalid parameter. Usage: u ai [integer]")
        else:
            print("Invalid number of arguments. Usage: u ai [integer]")
    
    elif args[0] == "ai2":
        if len(args) == 1:
            ai2()
        else:
            print("Invalid number of arguments. Usage: u ai2")
    elif args[0] == "sns":
        if len(args) == 1:
            sns()
        else:
            print("Invalid number of arguments. Usage: u sns")
    else:
        print("Invalid command. Usage: u [ai | ai2]")



# webbrowser.get("C:/Program Files/Mozilla Firefox/firefox.exe %s").open("https://example.com")