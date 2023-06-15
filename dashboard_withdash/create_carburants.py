from app import Carburant, conf_essence, db

def main():
    for essence, id in conf_essence.items():
        newessence = Carburant()
        newessence.id = id
        newessence.name = essence
        db.session.add(newessence)
        db.session.commit()


if __name__ == "__main__":
    main()
