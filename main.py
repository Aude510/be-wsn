import threading

def init_threads():
    thread_reception = threading.Thread(target=thread_reception)
    thread_envoi = threading.Thread(target=thread_envoi)
    thread_reception.start()
    thread_envoi.start()
    return

def thread_reception():
    return

def thred_envoi():
    return



if __name__ == "__main__":
    init_threads()
