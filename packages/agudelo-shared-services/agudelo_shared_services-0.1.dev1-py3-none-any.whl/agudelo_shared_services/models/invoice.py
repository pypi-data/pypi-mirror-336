from agudelo_shared_services.db import Base
from sqlalchemy import Column, Integer, String


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True)

    def __init__(self, code: str):
        self.code = code

    def __repr__(self):
        return f"<Invoice {self.code!r}>"
