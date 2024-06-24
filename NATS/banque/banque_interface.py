import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QStackedWidget, QLineEdit
from PyQt6.QtCore import QThread, pyqtSignal
from nats.aio.client import Client as NATS

class NATSWorker(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, subject, payload=b''):
        super().__init__()
        self.subject = subject
        self.payload = payload

    async def send_request(self):
        nc = NATS()
        try:
            await nc.connect("192.168.164.130:4222")
            response = await nc.request(self.subject, self.payload)
            await nc.close()
            self.response_received.emit(response.data.decode())
        except Exception as e:
            self.response_received.emit(f"Error: {str(e)}")

    def run(self):
        asyncio.run(self.send_request())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Client Selector")
        self.setGeometry(100, 100, 400, 300)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page_create_account = QWidget()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page_create_account)

        self.init_page1()
        self.init_page2()
        self.init_page_create_account()

        self.update_accounts_list()


    def init_page1(self):
        layout = QVBoxLayout()

        self.combo_box = QComboBox()
        layout.addWidget(self.combo_box)

        button = QPushButton("Select Client")
        button.clicked.connect(self.go_to_page2)
        layout.addWidget(button)

        create_account_button = QPushButton("Create Account")
        create_account_button.clicked.connect(self.go_to_page_create_account)
        layout.addWidget(create_account_button)

        self.page1.setLayout(layout)

    def init_page2(self):
        layout = QVBoxLayout()

        self.label = QLabel("Client Selected:")
        layout.addWidget(self.label)

        self.response_label = QLabel("Response: ")
        layout.addWidget(self.response_label)

        back_button = QPushButton("Back to Selection")
        back_button.clicked.connect(self.go_to_page1)
        layout.addWidget(back_button)

        self.page2.setLayout(layout)


    def init_page_create_account(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter account name")
        layout.addWidget(self.name_input)

        self.balance_input = QLineEdit()
        self.balance_input.setPlaceholderText("Enter initial balance")
        layout.addWidget(self.balance_input)

        create_button = QPushButton("Create Account")
        create_button.clicked.connect(self.create_account)
        layout.addWidget(create_button)

        back_button = QPushButton("Back to Selection")
        back_button.clicked.connect(self.go_to_page1)
        layout.addWidget(back_button)
        self.page_create_account.setLayout(layout)

    def go_to_page1(self):
        self.update_accounts_list()
        self.stacked_widget.setCurrentIndex(0)

    def go_to_page2(self):
        selected_client = self.combo_box.currentText()
        self.label.setText(f"Client Selected: {selected_client}")

        subject = f"banque.{selected_client}.compte"
        self.nats_worker = NATSWorker(subject)
        self.nats_worker.response_received.connect(self.display_response)
        self.nats_worker.start()
        self.stacked_widget.setCurrentIndex(1)

    def go_to_page_create_account(self):
        self.stacked_widget.setCurrentIndex(2)

    def display_response(self, response):
        self.response_label.setText(f"Response: {response}")

    def create_account(self):
        name = self.name_input.text()
        balance = self.balance_input.text()
        if name and balance:
            try:
                balance = int(balance)
                subject = "banque.creation"
                payload = f"{name}:{balance}".encode()
                self.nats_worker = NATSWorker(subject, payload)
                self.nats_worker.response_received.connect(self.account_created_response)
                self.nats_worker.start()
            except ValueError:
                self.response_label.setText("Invalid balance. Please enter a number.")

    def account_created_response(self, response):
        self.response_label.setText(f"Response: {response}")
        self.go_to_page1()

    def update_accounts_list(self):
        subject = "banque.list_accounts"
        self.nats_worker = NATSWorker(subject)
        self.nats_worker.response_received.connect(self.populate_combo_box)
        self.nats_worker.start()

    def populate_combo_box(self, response):
        accounts = response.split(',')
        self.combo_box.clear()
        self.combo_box.addItems(accounts)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
