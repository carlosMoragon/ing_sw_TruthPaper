from flask_sqlalchemy import SQLAlchemy


class New(SQLAlchemy().Model):
    new_id = SQLAlchemy().Column(SQLAlchemy().Integer, primary_key=True, autoincrement=True)
    owner = SQLAlchemy().Column(SQLAlchemy().String(50), nullable=False)
    title = SQLAlchemy().Column(SQLAlchemy().String(255), nullable=False)
    image = SQLAlchemy().Column(SQLAlchemy().String(255), nullable=False)
    url = SQLAlchemy().Column(SQLAlchemy().String(255), nullable=False)
    content = SQLAlchemy().Column(SQLAlchemy().Text, nullable=False)
    container = SQLAlchemy().Column(SQLAlchemy().Integer, nullable=False)
    journalistuser_id = SQLAlchemy().Column(SQLAlchemy().Integer)
    date = SQLAlchemy().Column(SQLAlchemy().Date, nullable=False)
    category = SQLAlchemy().Column(SQLAlchemy().String(30), nullable=False)

    def __init__(self, new_id, owner, title, image, url, content, container, journalistuser_id, date, category):
        self.new_id = new_id
        self.owner = owner
        self.title = title
        self.image = image
        self.url = url
        self.content = content
        self.container = container
        self.journalistuser_id = journalistuser_id
        self.date = date
        self.category = category
