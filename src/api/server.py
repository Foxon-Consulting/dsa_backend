import uvicorn


def run():
    """Point d'entrée pour démarrer le serveur API."""
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
