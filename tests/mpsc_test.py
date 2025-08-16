import mpsc

def received_sent_message():
    (sender, receiver) = mpsc.channel()

    sent_message = "Hello, world!"
    sender.send(sent_message)
    
    received_message = receiver.recv()
    assert sent_message == received_message