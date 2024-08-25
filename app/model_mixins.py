from .extensions import db


class ModelMixin:
    def save_to_db(self) -> None:
        """
        Save the current instance to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete the current instance from the database.
        """
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()
