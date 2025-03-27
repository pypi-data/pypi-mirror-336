from typing import Any, Dict, List

from mag_db.data.db_output import DbOutput


class ResultSetHelper:
    @staticmethod
    def to_maps(result_set: list[Dict[str, Any]], db_output: DbOutput) -> List[Dict[str, Any]]:
        return [
            {
                db_output.column_name_mapping.get_target_name(column_name) or column_name:
                    row_map[column_name] for column_name in db_output.column_names
            }
            for row_map in result_set
        ]

    @staticmethod
    def to_beans(result_set: list[Dict[str, Any]], db_output: DbOutput) -> List[Any]:
        result_list = []
        for row_map in result_set:
            kwargs = {}
            for column_name in db_output.column_names:
                target_name = db_output.get_target_name(column_name)
                kwargs[target_name] = row_map.get(column_name)

            result_list.append(db_output.result_class(**kwargs))

        return result_list
