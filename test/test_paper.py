import sqlalchemy

PASSWORD = input("Your PostgreSQL password: ")
ENGINE = sqlalchemy.create_engine(f'postgresql://postgres:{PASSWORD}@localhost:5432/postgres')
CONNECTION = ENGINE.connect()

class TestPaper:

    def test_connect(self):
        assert CONNECTION.closed == False

    def test_closed(self):
        CONNECTION.close()
        assert CONNECTION.closed == True