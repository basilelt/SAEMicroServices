import asyncio
import nats
import json
import pickle
import os

data_dir = "/valid-place/data"
data_file = os.path.join(data_dir, "vol.pkl")


if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if os.path.exists(data_file):
    with open(data_file, "rb") as f:
        vol = pickle.load(f)
else:
    vol = {}


def save_vol():
    with open(data_file, "wb") as f:
        pickle.dump(vol, f)


async def handle_create_vol(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    try:
        name, place = data.split(":")
        place = int(place)
        if name not in vol:
            vol[name] = place
            response = f"vol crée {name} avec  {place} place."
            print(response)
            save_vol()
        elif vol[name] == place:
            response = f"Le vol {name} existe déjà."
            print(response)
        else:
            vol[name] = place
            response = f"vol crée {name} avec  {place} place."
            print(response)
            save_vol()
    except Exception as e:
        response = f"Erreur lors de la création du vol: {str(e)}"
        print(response)

    await nc.publish(reply, response.encode())

async def handle_place_validation(msg):
    subject = msg.subject
    reply = msg.reply
    vol_request = msg.data.decode
    try:
        name, place=vol_request.splt(":")
        if name in vol:
            if vol[name] >= place:
               print(f"les place du vol {name} sont reserver.")
               vol[name] -= place
               response_msg = f"True,Resever,Vol reservé. Les place restente sont de {vol[name]}"
               save_vol()
            
            else:
                print("Place insufisante")
                response_msg = "False,failed, nombre de place insufisante"
        else:
            print("Vol inconnu.")
            response_msg = "False,Failed,Vol inconnu."

        await nc.publish(reply, response_msg.encode())   
    except Exception as err:
        print(err)
 
async def handle_place_devalidation(msg):
    subject = msg.subject
    reply = msg.reply
    vol_request = msg.data.decode
    try:
        name, place=vol_request.splt(":")
        if name in vol:
            print(f"{place} place du vol {name} sont de nouveaux displonible.")
            vol[name] += place
            response_msg = f"True,Rembourse,Les place restente sont de {vol[name]}"
            
        else:
            print("Vol inconnu.")
            response_msg = "False,Failed,Vol inconnu."

        await nc.publish(reply, response_msg.encode())   
    except Exception as err:
        print(err)

async def vol_request():

    # Envoi de la requête et attente de la réponse
    reponse = await nc.request("vol.request",timeout=10)

    # Décodage de la réponse
    reponse_data = json.loads(reponse.data.decode())
    print("Received response:", reponse_data)
   
    for key, value in reponse_data.items():
        if key not in vol:
            vol[key] = value
    
    save_vol()

async def main():
    global nc
    nc = await nats.connect("nats://192.168.164.130:4222")
    vol_request
    try:
        await nc.subscribe("validation.reservation.place.client", cb=handle_place_validation)
        await nc.subscribe("validation.remboursement.place.client.*", cb=handle_place_devalidation)
        await nc.subscribe("vol.creation", cb=handle_create_vol)
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()


if __name__ == '__main__':
    asyncio.run(main())

