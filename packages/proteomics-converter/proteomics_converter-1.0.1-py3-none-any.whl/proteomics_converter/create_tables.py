import pandas as pd
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import sqlalchemy as sa

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


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


if __name__ == '__main__':
    engine = sa.create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    session = create_session(engine)

    sample_1 = Sample(sample_name='S1')  # hyb norm count
    sample_2 = Sample(sample_name='S1')  # raw count

    somamer_1 = Somamer(somamer_name='10008-1')
    somamer_2 = Somamer(somamer_name='ilmn-xxxx')

    count_1_1 = Count(sample_=sample_1, somamers=somamer_1, value=100)
    count_2_1 = Count(sample_=sample_2, somamers=somamer_1, value=1000)
    count_1_2 = Count(sample_=sample_1, somamers=somamer_2, value=200)
    count_2_2 = Count(sample_=sample_2, somamers=somamer_2, value=2000)

    # create Session class that talks to the database

    # create new Session

    # add a new record in the session
    # Note: no SWL has yet been issue, no row is added, until we query
    # session.add(first_sample)
    # our_sample = (
    #     session.query(Sample).filter_by(sample_name='S1').first()
    # )
    # first_sample.sample_name = 'S_1'
    session.add_all(
        [
            sample_1,
            sample_2,
            somamer_1,
            somamer_2,
            count_1_1,
            count_1_2,
            count_2_1,
            count_2_2,

        ]
    )
    session.commit()
    # for instance in session.query(Sample).order_by(Sample.id):
    #     print(instance.sample_name, instance.matrix_type)

    query = sa.text("""SELECT * FROM counts""")
    df = pd.read_sql_query(
        query,
        con=engine.connect(),
    )
    print(df)
    print()
