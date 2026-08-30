"""
Ponto de entrada da aplicação.

Uso:
    python run.py
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True apenas em desenvolvimento (nunca em produção)
    app.run(debug=True)
