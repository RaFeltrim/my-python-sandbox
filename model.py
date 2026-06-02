from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import registry, sessionmaker

# =========================
# 1. MODELO DE DOMÍNIO
# =========================

class Book:
    def __init__(self, reference: str, title: str, quantity: int):
        self.reference = reference
        self.title = title
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"<Book {self.reference} - {self.title} (Qty: {self.quantity})>"

# =========================
# 2. CONFIGURAÇÃO DO BANCO
# =========================

metadata = MetaData()
mapper_registry = registry()

books_table = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255), unique=True, nullable=False),
    Column("title", String(255), nullable=False),
    Column("quantity", Integer, nullable=False),
)

def start_mappers():
    if mapper_registry.mappers:
        return
    mapper_registry.map_imperatively(Book, books_table)

# =========================
# 3. REPOSITORY
# =========================

class BookRepository:
    def __init__(self, session):
        self.session = session

    def add(self, book: Book):
        self.session.add(book)

    def get(self, reference: str) -> Book:
        return self.session.query(Book).filter_by(reference=reference).first()

    def list(self) -> list[Book]:
        return self.session.query(Book).all()

# =========================
# 4. EXECUÇÃO
# =========================

if __name__ == "__main__":
    # Inicializa os mapeadores clássicos do SQLAlchemy
    start_mappers()

    # Cria o engine SQLite em memória e gera as tabelas físicas
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)

    # Cria uma fábrica de sessões e abre uma sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Instancia o repositório passando a session
    repo = BookRepository(session)

    print("--- Adicionando livros ao banco de dados ---")
    book1 = Book("REF-UML", "UML Essencial", 5)
    book2 = Book("REF-DDD", "Architecture Patterns with Python", 3)
    
    repo.add(book1)
    repo.add(book2)
    session.commit()
    print("Livros salvos com sucesso!")

    print("\n--- Consultando livros salvos ---")
    retrieved_book = repo.get("REF-DDD")
    print(f"Livro recuperado por ID: {retrieved_book}")

    print("\n--- Listando todos os livros do banco ---")
    all_books = repo.list()
    for book in all_books:
        print(book)

    session.close()

