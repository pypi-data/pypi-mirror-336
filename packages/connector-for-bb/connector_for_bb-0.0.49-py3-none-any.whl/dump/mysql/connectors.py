import pymysql

from dump.config_utils import load_config


TYPE_MAPPER = {
    "bigint": "Int64",
    "real": "Int64",
    "integer": "Int64",
    "double precision": "float",
    "decimal": "float",
    "USER-DEFINED": "str",
    "character varying": "str",
    "character": "str",
    "text": "str",
    "boolean": "bool",
    "timestamp without time zone": "timestamp",
    "timestamp": "timestamp",
    "date": "timestamp",
}


class ConnectorMySQL:
    def __init__(
        self,
        db_config_name: str = "postgres",
    ) -> None:
        self.db_config_name = db_config_name

        self.__config = load_config(section=self.db_config_name)
        self.__config["port"] = int(self.__config["port"])

        self._conn = None
        self._cursor = None

    @property
    def conn(self):
        if self._conn is None:
            try:
                self._conn = pymysql.connect(**self.__config)
            except pymysql.Error as error:
                raise error
        return self._conn

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.conn.cursor()
        return self._cursor

    @property
    def close(self):
        self._conn.close()

        self._conn = None
        self._cursor = None

    @property
    def commit(self):
        self.conn.commit()

    def execute(self, query: str):
        self.cursor.execute(query)
        self.conn.commit()

    def fetchall(self, query: str) -> list:
        self.execute(query)
        values = self.cursor.fetchall()
        self.conn.commit()

        return values


class DBUtilsMySQL(ConnectorMySQL):
    @staticmethod
    def _validate_output(inp: list):
        return [x[0] for x in inp]

    def get_table_structure(self, table_name: str) -> dict:
        query = f"""
            SELECT column_name, data_type, is_nullable, ordinal_position
            FROM information_schema.columns
            WHERE table_name = '{table_name}';
        """

        schema = {}
        for column_name, data_type, is_nullable, position in self.fetchall(query):
            if "int" in data_type:
                data_type = "integer"
            if "numeric" in data_type or "decimal" in data_type:
                data_type = "decimal"
            if "time" in data_type:
                data_type = "timestamp"

            schema[column_name] = {
                "data_type": TYPE_MAPPER.get(data_type, "str"),
                "is_nullable": is_nullable,
                "position": position,
            }
        return schema
