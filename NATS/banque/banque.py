import asyncio
import nats

# Dictionnaire des clients avec leurs soldes
clients = {
    "client1": 153,
    "client2": 456,
    "client3": 789,
    "client4": 1011,
    "client5": 1213
}

# Variable d'autorisation globale
autorize = True

async def handle_list_accounts_request(msg):
    reply = msg.reply
    accounts_list = ",".join(clients.keys())
    print(f"Liste des comptes demandée : {accounts_list}")
    await nc.publish(reply, accounts_list.encode())

async def handle_payment_request(msg):
    global autorize
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
            if clients[client] >= montant:
                # Envoyer la demande de validation au client spécifique

                autorize = 'true'
                
                print(f"Validation de paiement reçue : autorize={autorize}")

                if autorize:
                    print(f"Paiement de {montant} à {client} autorisé.")
                    clients[client] -= montant
                    response_msg = f"Paiement autorisé. Nouveau solde de {client}: {clients[client]}"
                else:
                    print("Paiement refusé.")
                    response_msg = "Paiement refusé par l'autorisation."
            else:
                print("Paiement refusé, solde insuffisant.")
                response_msg = "Paiement refusé, solde insuffisant."
        else:
            print("Client inconnu.")
            response_msg = "Client inconnu."

        await nc.publish(reply, response_msg.encode())

    except Exception as e:
        print(f"Erreur: {str(e)}")
        await nc.publish(reply, f"Erreur: {str(e)}".encode())

async def handle_account_request(msg):
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
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    try:
        name, balance = data.split(":")
        balance = int(balance)
        if name not in clients:
            clients[name] = balance
            response = f"Compte créé pour {name} avec un solde de {balance}."
            print(response)
        else:
            response = f"Le compte {name} existe déjà."
            print(response)
    except Exception as e:
        response = f"Erreur lors de la création du compte: {str(e)}"
        print(response)

    await nc.publish(reply, response.encode())

async def main():
    global nc
    nc = await nats.connect("nats://192.168.164.130:4222")
    try:
        await nc.subscribe("banque.demande.client.*", cb=handle_payment_request)
        await nc.subscribe("banque.*.compte", cb=handle_account_request)
        await nc.subscribe("banque.creation", cb=handle_create_account_request)
        await nc.subscribe("banque.list_accounts", cb=handle_list_accounts_request)
        await nc.subscribe("banque.validation.*", cb=handle_payment_request)
        await nc.subscribe("banque.*.payment", cb=handle_payment_request)
        
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()


if __name__ == '__main__':
    asyncio.run(main())
