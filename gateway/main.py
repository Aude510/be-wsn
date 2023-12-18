import threading

def init_threads():
    threading.Thread(target=thread_reception).start()
    threading.Thread(target=thread_envoi).start()
    threading.Thread(target=thread_decode).start()

def thread_reception():
    return

def thread_envoi():
    return

def thread_decode():
    return



if __name__ == "__main__":
    init_threads()
