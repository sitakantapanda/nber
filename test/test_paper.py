import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://localhost:5432/postgres')
connection = engine.connect()

class TestPaper:

    def test_connect(self):
        assert connection.closed == False

    def test_closed(self):
        connection.close()
        assert connection.closed == True