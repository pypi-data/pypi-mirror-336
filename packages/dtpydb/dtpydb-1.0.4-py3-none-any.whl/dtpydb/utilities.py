from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import insert


def upsert_data(list_of_data: list[dict], model, db, only_update=False, only_insert=False):
    if list_of_data:
        if only_update:
            db.bulk_update_mappings(model, list_of_data)
            db.commit()
        elif only_insert:
            db.bulk_insert_mappings(model, list_of_data)
            db.commit()
        else:
            data_keys = list_of_data[0].keys()
            stmt = insert(model.__table__).values(list_of_data)
            update_dict = {c.name: c for c in stmt.excluded if not c.primary_key and c.name in data_keys}
            if update_dict:
                primary_keys = [key.name for key in inspect(model.__table__).primary_key]
                stmt = stmt.on_conflict_do_update(index_elements=primary_keys, set_=update_dict)
                db.execute(stmt)
                db.commit()
                return True
            else:
                return False
    else:
        return False
