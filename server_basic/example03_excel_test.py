import http.server
import socketserver
from openpyxl.workbook import Workbook
from openpyxl.writer.excel import save_virtual_workbook
import io

# xlsxwriter로 만든 데이터를 BytesIO라는 데이터스트림으로 변환해서 출력
PORT = 8002

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        wb = Workbook()
        ws = wb.active
        ws.cell(1,1,"openpyxl test 1")
        output = io.BytesIO(save_virtual_workbook(wb))
        self.send_response(200)
        self.send_header('Content-Disposition', 'attachment; filename=test.xlsx')
        self.send_header('Content-type',
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.end_headers()
        self.wfile.write(output.read())
        return

print('serving at port', PORT)
httpd = socketserver.TCPServer(('',PORT), Handler)
httpd.serve_forever()