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


'''import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QStackedWidget, QLineEdit, QInputDialog
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from nats.aio.client import Client as NATS

class NATSWorker(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, subject, payload=b'', timeout=20):
        super().__init__()
        self.subject = subject
        self.payload = payload
        self.timeout = timeout

    async def send_request(self):
        nc = NATS()
        try:
            print(f"Envoi de la requête au sujet {self.subject} avec payload {self.payload}")
            await nc.connect("nats://192.168.164.130:4222")
            response = await nc.request(self.subject, self.payload, timeout=self.timeout)
            await nc.close()
            print(f"Réponse reçue : {response.data.decode()}")
            self.response_received.emit(response.data.decode())
        except Exception as e:
            print(f"Erreur lors de l'envoi de la requête : {str(e)}")
            self.response_received.emit(f"Error: {str(e)}")

    def run(self):
        asyncio.run(self.send_request())

class NATSSubscriptionWorker(QThread):
    validation_request_received = pyqtSignal(str, str)

    def __init__(self, client_name):
        super().__init__()
        self.client_name = client_name
        self.nc = NATS()

    async def subscribe_to_validation(self):
        await self.nc.connect("nats://192.168.164.130:4222")
        await self.nc.subscribe(f"banque.validation.{self.client_name}", cb=self.handle_validation_request)

    async def handle_validation_request(self, msg):
        client_name = msg.subject.split('.')[-1]
        montant = msg.data.decode()
        print(f"Requête de validation reçue pour {client_name} : {montant}")
        self.validation_request_received.emit(montant, msg.reply)

    def run(self):
        asyncio.run(self.subscribe_to_validation())

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
        self.page_validation = QWidget()  # Nouvelle page pour la validation

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page_create_account)
        self.stacked_widget.addWidget(self.page_validation)

        self.init_page1()
        self.init_page2()
        self.init_page_create_account()
        self.init_page_validation()  # Initialiser la nouvelle page

        self.update_accounts_list()
        self.client_name = ""
        self.validation_subject = ""

        self.subscription_worker = None

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

        pay_button = QPushButton("Pay")
        pay_button.clicked.connect(self.make_payment)
        layout.addWidget(pay_button)

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

    def init_page_validation(self):
        layout = QVBoxLayout()
        self.validation_label = QLabel("Validation de paiement")
        layout.addWidget(self.validation_label)

        self.accept_button = QPushButton("Accepter")
        self.accept_button.clicked.connect(self.accept_payment)
        layout.addWidget(self.accept_button)

        self.reject_button = QPushButton("Rejeter")
        self.reject_button.clicked.connect(self.reject_payment)
        layout.addWidget(self.reject_button)

        self.page_validation.setLayout(layout)

    def start_subscription(self):
        if self.subscription_worker:
            self.subscription_worker.terminate()

        self.subscription_worker = NATSSubscriptionWorker(self.client_name)
        self.subscription_worker.validation_request_received.connect(self.display_validation_request)
        self.subscription_worker.start()

    @pyqtSlot(str, str)
    def display_validation_request(self, montant, subject):
        self.validation_subject = subject
        self.validation_label.setText(f"Valider le paiement de {montant} ?")
        self.stacked_widget.setCurrentIndex(3)

    def accept_payment(self):
        asyncio.create_task(self.publish_response('true'))
        self.stacked_widget.setCurrentIndex(1)

    def reject_payment(self):
        asyncio.create_task(self.publish_response('false'))
        self.stacked_widget.setCurrentIndex(1)

    async def publish_response(self, response):
        await self.subscription_worker.nc.publish(self.validation_subject, response.encode())

    def go_to_page1(self):
        self.update_accounts_list()
        self.stacked_widget.setCurrentIndex(0)

    def go_to_page2(self):
        selected_client = self.combo_box.currentText()
        self.client_name = selected_client  # Store the selected client name
        self.label.setText(f"Client Selected: {selected_client}")

        subject = f"banque.{selected_client}.compte"
        self.nats_worker = NATSWorker(subject)
        self.nats_worker.response_received.connect(self.display_response)
        self.nats_worker.start()
        self.start_subscription()  # Start the subscription when a client is selected
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

    def make_payment(self):
        amount, ok = QInputDialog.getDouble(self, "Payment", "Enter amount to pay:", min=0)
        if ok:
            subject = f"banque.{self.client_name}.payment"
            payload = str(amount).encode()
            self.nats_worker = NATSWorker(subject, payload)
            self.nats_worker.response_received.connect(self.display_payment_response)
            self.nats_worker.start()

    def display_payment_response(self, response):
        self.response_label.setText(f"Payment Response: {response}")

    def handle_validation_request(self, montant, reply_subject):
        print(f"Autorisation automatique de paiement de {montant} pour {self.client_name}")
        worker = NATSWorker(reply_subject, b"true")
        worker.response_received.connect(self.show_validation_response)
        worker.start()

    def show_validation_response(self, response):
        print(f"Réponse de validation : {response}")
        self.response_label.setText(f"Validation Response: {response}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
'''