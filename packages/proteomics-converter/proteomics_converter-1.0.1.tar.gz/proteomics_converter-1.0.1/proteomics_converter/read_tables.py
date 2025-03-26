import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from proteomics_converter.create_tables import Sample

engine = sa.create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# SQLAlCHEMY ORM QUERY TO FETCH ALL RECORDS
query = sa.text("""SELECT * FROM Sample""")
df = pd.read_sql_query(
    query,
    con=engine.connect(),
)
print(df)
