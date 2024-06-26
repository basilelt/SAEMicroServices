import asyncio
import nats
import pickle
import os

# Directory for storing client data
data_dir = "./data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
data_file = os.path.join(data_dir, "clients.pkl")

def save_clients():
    """Save the clients' data to a file."""
    with open(data_file, "wb") as f:
        pickle.dump(clients, f)

# Load existing client data or initialize with default values
if os.path.exists(data_file):
    with open(data_file, "rb") as f:
        clients = pickle.load(f)
else:
    clients = {
        "client1": 153,
        "client2": 456,
        "client3": 789,
        "client4": 1011,
        "client5": 1213
    }
    save_clients()

autorize = True

async def handle_list_accounts_request(msg):
    """
    Handle requests to list all account names.
    
    Args:
        msg (nats.aio.msg.Msg): The message received from NATS.
    """
    reply = msg.reply
    accounts_list = ",".join(clients.keys())
    print(f"Liste des comptes demandée : {accounts_list}")
    await nc.publish(reply, accounts_list.encode())

async def handle_payment_request(msg):
    """
    Handle payment validation requests.
    
    Args:
        msg (nats.aio.msg.Msg): The message received from NATS.
    """
    global autorize
    try:
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        parts = data.split(':')
        client = parts[0]
        montant = float(parts[1])
        
        if client in clients:
            if clients[client] >= montant:
                print(f"Validation de paiement reçue : autorize={autorize}")

                if autorize:
                    print(f"Paiement de {montant} à {client} autorisé.")
                    clients[client] -= montant
                    response_msg = "True"
                    save_clients()
                else:
                    print("Paiement refusé.")
                    response_msg = "False"
            else:
                print("Paiement refusé, solde insuffisant.")
                response_msg = "False"
        else:
            print("Client inconnu.")
            response_msg = "False"

        await nc.publish(reply, response_msg.encode())

    except Exception as e:
        print(f"Erreur: {str(e)}")
        rep=f"Erreur: {str(e)}"
        await nc.publish(reply, rep.encode())

async def handle_account_request(msg):
    """
    Handle requests for account balance information.
    
    Args:
        msg (nats.aio.msg.Msg): The message received from NATS.
    """
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    info = subject.split(".")
    client = info[1]
    if client in clients:
        compte = clients[client]
        print(f"Message reçu sur le sujet {subject} : {data}")
        response = f"Le solde du compte est de : {compte}"
    else:
        response = "Client inconnu."
    
    await nc.publish(reply, response.encode())

async def handle_create_account_request(msg):
    """
    Handle requests to create new accounts.
    
    Args:
        msg (nats.aio.msg.Msg): The message received from NATS.
    """
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    try:
        name, balance = data.split(":")
        balance = int(balance)
        if name not in clients:
            clients[name] = balance
            response = f"Compte créé pour {name} avec un solde de {balance}."
            save_clients()
            print(response)
        else:
            response = f"Le compte {name} existe déjà."
            print(response)
    except Exception as e:
        response = f"Erreur lors de la création du compte: {str(e)}"
        print(response)

    await nc.publish(reply, response.encode())

async def handle_remboursement_request(msg):
    """
    Handle reimbursement requests.
    
    Args:
        msg (nats.aio.msg.Msg): The message received from NATS.
    """
    try:
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        parts = subject.split('.')
        client = parts[1]
        montant = float(data)
        
        # Log for debugging
        print(f"Requête de paiement reçue : client={client}, montant={montant}")

        if client in clients:
            print(f"remboursement de {montant} à {client}.")
            clients[client] += montant
            save_clients()
            response_msg = f"True,Rembourse,Nouveau solde de {client}: {clients[client]}"
        else:
            print("Client inconnu.")
            response_msg = "False,Failed,Client inconnu."

        await nc.publish(reply, response_msg.encode())
    except Exception as err:
        print(err)

async def main():
    """
    Main function to set up NATS client and subscribe to various subjects.
    """
    global nc
    env = os.getenv("DJANGO_ENVIRONMENT", "development")
    user = os.getenv("NATS_USER", '')
    password = os.getenv("NATS_PASSWORD", '')
    if env == "development":
        nc = await nats.connect("nats://localhost:4222", user=user, password=password)
    else:
        nc = await nats.connect("nats://nats:4222", user=user, password=password)
        
    try:
        await nc.subscribe("banque.*.compte", cb=handle_account_request)
        await nc.subscribe("banque.creation", cb=handle_create_account_request)
        await nc.subscribe("banque.list_accounts", cb=handle_list_accounts_request)
        await nc.subscribe("banque.validation", cb=handle_payment_request)
        await nc.subscribe("banque.*.rembousement", cb=handle_remboursement_request)

        while True:
            await asyncio.sleep(1)
           
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()

if __name__ == '__main__':
    asyncio.run(main())
