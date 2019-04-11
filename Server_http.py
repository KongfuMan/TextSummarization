import socket
from aylienapiclient import textapi
# import thread module
from _thread import *
import threading

# print_lock = threading.Lock()


index_content = '''
HTTP/1.x 200 ok
Content-Type: text/html

'''

file = open('index.html', 'r')
index_content += file.read()
file.close()



after_content = '''
HTTP/1.x 200 ok
Content-Type: text/html

'''

file_a1 = open('after1.html', 'r')
after_content1 = after_content + file_a1.read()
file_a1.close()
file_a2 = open('after2.html', 'r')
after_content2 = file_a2.read()
file_a2.close()





# thread fuction
def threaded(clientSocket):
    while True:
        # data received from client

        request = clientSocket.recv(1024)

        print("Thread "+threading.currentThread().getName() + "receives msg ")
        print('REQUEST',request)
        print(str(request, encoding = "utf-8"))
        method = str(request, encoding = "utf-8").split(' ')[0]
        print('M:',method)

        src = str(request, encoding = "utf-8").split(' ')[1]


        print('SRC:',src)

        if method == 'GET':
            if src == '/index.html':
                content = index_content
            else:
                continue

        elif method == 'POST':
            form = str(request, encoding = "utf-8").split('\r\n')
            entry = form[-1]
            sentnum = entry.split('&')[0]
            sentnum = sentnum.split('=')[1]
            oriText = entry.split('&')[1]
            oriText = oriText.split('=')[1]

            # try:
            #     oriTextList = oriText.split('+')
            #     oriText = " ".join(oriTextList)
            #     oriText = oriText.replace('%27',"'")
            #     oriText = oriText.replace('%2C', ",")
            # except:
            #     print('no need for rematching')



            print('sentnum',sentnum)
            print('oriText',oriText)



            #API Connection
            api_client = textapi.Client("fb06fac0", "2ae63c83921394ba9b699154902a3a21")
            summary = api_client.Summarize({'title': 'Test', 'text': oriText, 'sentences_number': sentnum})

            outputSent = ""
            for sentence in summary['sentences']:
                # print(sentence)
                outputSent = outputSent + sentence


            print('OUT:',outputSent)

            jsScript1 = "<script>document.getElementById('oriText').innerHTML=\"<textarea maxlength=\\\"50000\\\" name=\\\"oriText\\\" size=\\\"5000\\\" style=\\\"width:600px;height:250px\\\">" + oriText + "</textarea>\";</script>"
            #jsScript2 = "<script>document.getElementById('sentnum').innerHTML=\"<input id=\\\"sentnum\\\" maxlength=\\\"100\\\" name=\\\"sentnum\\\"  size=\\\"50\\\" style=\\\"width:100px;height:20px\\\" type=\\\"text\\\" value=\\\"" + sentnum + "\\\">\";</script>"

            jsScript3 = "<script>document.getElementById('output').innerHTML=\"<textarea maxlength=\\\"50000\\\" size=\\\"5000\\\" style=\\\"width:600px;height:250px\\\" disabled>" + outputSent + "</textarea>\";</script>"

            content = after_content1 + jsScript1 + '\n'  +'\n' + jsScript3 + after_content2

            content += '<p>Summarize successs!</p>'




            #form data process

        else:
            continue

        # print(bytes(content, encoding = "utf8").type)
        clientSocket.sendall(bytes(content, encoding = "utf8"))

        clientSocket.close()








        # if not data:
        #     print('Bye')
        #
        #     # lock released on exit
        #     # print_lock.release()
        #     break
        #
        # # reverse the given string from client
        # data = data[::-1]
        #
        # # send back reversed string to client
        # clientSocket.send(data)
        #
        # # connection closed



def Main():
    host = "127.0.0.1"

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 1111
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setblocking(True)
    serverSocket.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    serverSocket.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        clientSocket, addr = serverSocket.accept()

        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (clientSocket,))

    serverSocket.close()


if __name__ == '__main__':
    Main()