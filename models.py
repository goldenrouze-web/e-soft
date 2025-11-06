from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)
    filepath = Column(String(255))


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    mean = Column(Float)
    median = Column(Float)
    correlation = Column(Float)
