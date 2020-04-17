"""Handler for Database Operations."""
import pyrebase
from datetime import datetime


class DBHandler(object):
    """Handles all Firebase interactions."""

    def __init__(self, config):
        """Construct object."""
        self._db = pyrebase.initialize_app(config).database()
        return

    def __find_collection(self, collection_path):
        collection = self._db
        for c in collection_path:
            collection = collection.child(c)
        return collection

    def test_db(self, json):
        """Tests Access to DB."""
        self._db.child("raw_sensor_data").push({
            "sensor_type": "testing - {}".format(datetime.now().time()),
            "json_data": json
        })
        return

    def put(self, collection_path, data, auto_id=True):
        """
        Put data into the firebase db.

        Args:
            collection_path (list[str]): a list of nested children to enter
                before putting data into db.
            data (dict): json object with data to put into db.
            auto_id: Whether or not to use an auto_id for the data or if key is
                present already in the data dict.
        """
        collection = self.__find_collection(collection_path)
        response = None
        if auto_id:
            response = collection.push(data)
        else:
            response = collection.set(data)
        return response

    def get(self, collection_path,
            raw_response=False,
            sort_by_key=False,
            limit_to_last=None,
            in_range=None):
        """
        Retrieve data from the firebase db.

        Args:
            collection_path (list[str]): a list of nested children to enter
                before putting data into db.
            raw_respone: Whether to get the unprocessed PyreResponse object
                instead of a dict.
        Returns:
            dict[JSON] OR pyrebase.PyreResponse
        """
        collection = self.__find_collection(collection_path)
        if sort_by_key:
            collection.order_by_key()
        if in_range:
            collection.start_at(in_range[0]).end_at(in_range[1])
        if limit_to_last:
            collection.limit_to_last(limit_to_last)
        response = collection.get()
        if not raw_response:
            response = response.val()
        return response
