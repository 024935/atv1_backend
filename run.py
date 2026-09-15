"""Front controller: carrega o `.env`, abre a conexão com o banco e sobe o servidor."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402  (precisa vir depois do load_dotenv)
from app.config.database import Database  # noqa: E402

app = create_app(Database.connection())

if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", "3589"))
    app.run(host="0.0.0.0", port=port)
