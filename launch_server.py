import http.server
import webbrowser
import threading
import os
import sys

# Ensure current working directory is the script folder
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

PORT = 8711

class QuizHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def open_browser():
    import time
    time.sleep(0.8)
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    print('=' * 60)
    print('  🏪 7-ELEVEN 門市月營收 AI 智慧回推系統看板原型')
    print('=' * 60)
    print(f'  伺服器已啟動: http://localhost:{PORT}')
    print('  請於瀏覽器中操作；若要停止請按 Ctrl + C')
    print('=' * 60)
    
    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()

    try:
        server = http.server.HTTPServer(('', PORT), QuizHTTPRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n伺服器已安全停止。')
        sys.exit(0)
