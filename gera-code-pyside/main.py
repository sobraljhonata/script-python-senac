from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton 
from PySide6.QtWidgets import QLineEdit, QMessageBox, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap
import qrcode

# CRIA A CLASSE QUE CARREGA A TELA PRINCIPAL
# E TODAS AS FUNÇÕES NECESSÁRIAS PARA O FUNCIONAMENTO DO PROGRAMA
# E A CLASSE CRIADA HERDA DO QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Código QR")
        self.setGeometry(100, 100, 400, 300)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.website_label = QLabel("URL:")
        self.layout.addWidget(self.website_label)
        
        self.website_entry = QLineEdit()
        self.layout.addWidget(self.website_entry)
        
        self.name_file_label = QLabel("Nome do Arquivo:")
        self.layout.addWidget(self.name_file_label)
        
        self.name_file_entry = QLineEdit()
        self.layout.addWidget(self.name_file_entry)
        
        self.add_button = QPushButton("Gerar QR Code")
        self.add_button.clicked.connect(self.gera_qr_code)
        self.layout.addWidget(self.add_button)
        
    def gera_qr_code(self):
        url = self.website_entry.text()
        nome_arquivo = self.name_file_entry.text()
        if len(url) == 0:
            QMessageBox.information(self, "Erro!", "Favor insira uma URL válida")
        if len(nome_arquivo) == 0:
            QMessageBox.information(self, "Erro!", "Favor insira um nome de arquivo válido")
        else:
            opcao_escolhida = QMessageBox.question(
                self, url, f"O endereço URL é: \n Endereço: {url} \n Pronto para salvar?",
                QMessageBox.Ok | QMessageBox.Cancel
            )
            if opcao_escolhida == QMessageBox.Ok:
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color='white')
                img.save(nome_arquivo + '.png')
                self.create_image_window(f'{nome_arquivo}.png')
                
    def create_image_window(self, image_path):
        self.image_window = QMainWindow()
        self.image_window.setWindowTitle("Exibir Imagem PNG")
        self.image_window.setGeometry(100, 100, 450, 500)
        
        # Cria um QLabel para exibir a imagem
        self.image_label = QLabel(self.image_window)
        self.image_label.setGeometry(50, 50, 300, 200)
        
        # Carrega a imagem PNG
        pixmap = QPixmap(image_path)
        
        # Define o QPixmap no QLabel
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        
        self.add_button = QPushButton("Gerar Novo", self.image_window)
        self.add_button.setGeometry(150, 260, 100, 30)
        self.add_button.clicked.connect(self.voltar_tela_inicial)
        
        self.image_window.show()
        
    def voltar_tela_inicial(self):
        self.image_window.close()
        self.website_entry.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()