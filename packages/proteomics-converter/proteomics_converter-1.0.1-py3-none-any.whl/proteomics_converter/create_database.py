import sqlite3

import pandas as pd
from canopy import Adat
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import sqlalchemy as sa

from proteomics_converter.create_tables import Sample, Somamer, Count

Base = declarative_base()


class Sample(Base):
    __tablename__ = 'samples'

    id = sa.Column(sa.Integer, sa.Sequence('sample_id_sequence'), primary_key=True)
    sample_name = sa.Column(sa.String(50))

    # define one-to-many relationship
    counts = relationship('Count', backref='sample_')

    def __repr__(self):
        return f'<Sample(name={self.sample_name})>'


class Count(Base):
    __tablename__ = 'counts'

    id = sa.Column(sa.Integer, primary_key=True)
    sample_id = sa.Column(sa.Integer, sa.ForeignKey('samples.id'))
    somamer_id = sa.Column(sa.Integer, sa.ForeignKey('somamers.id'))
    value = sa.Column(sa.Float)

    # sample = relationship('Sample', backref='counts')
    # somamer = relationship('Somamer', backref='counts')

    def __repr__(self):
        return f'<Count(sample_id={self.sample_id})>'


class Somamer(Base):
    __tablename__ = 'somamers'

    id = sa.Column(sa.Integer, primary_key=True)
    somamer_name = sa.Column(sa.String(10), unique=True)

    counts = relationship('Count', backref='somamer_')

    def __repr__(self):
        return f'<Somamer(somamer_name={self.somamer_name})>'

engine = sa.create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def create_df(adat: Adat) -> list[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    somamers = adat.columns.to_frame()
    samples = adat.index.to_frame()
    counts = adat.values
    i = 0
    for idx_sample, sample in samples.iterrows():
        sample_obj = Sample(sample_name=sample['SampleID'])
        session.add(sample_obj)
        j = 0
        for idx_somamer, somamer in somamers.iterrows():
            print(i, j, sample['SampleID'], somamer['SeqId'])
            somamer_obj = Somamer(somamer_name=somamer['SeqId'])
            count_obj = Count(value=counts[i, j], sample_=sample_obj, somamer_=somamer_obj)
            try:
                session.add(somamer_obj     )
            except sa.exc.IntegrityError:
                pass
            session.add(count_obj)
            j += 1
        i += 1
    session.commit()
    tables = ['samples', 'somamers', 'counts']
    df = []
    for table in tables:
        query = sa.text(f"SELECT * from {table}")
        df.append(pd.read_sql_query(
            query,
            con=engine.connect(),
        )
        )
    return df





