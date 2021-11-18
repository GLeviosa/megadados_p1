from database import Base,engine
from models import Discipline, Note

print("Creating database ....")

Base.metadata.create_all(engine)