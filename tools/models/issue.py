from sqlalchemy import Column, Integer, String
from tools.models.base import Base

class Issue(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    pdf_url = Column(String, nullable=False)
    detail_url = Column(String, nullable=False)
    content_html = Column(String, nullable=True)