#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from collections import defaultdict
from typing import Union

from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def create_legend():
    legend = Table(show_header=False, box=None)
    legend.add_column(style="bold")
    legend.add_column()
    legend.add_row("Red", "Mismatch", style="red")
    legend.add_row("Cyan", "Match", style="cyan")
    legend.add_row("Yellow", "Duplicate", style="yellow")
    return Panel(legend, title="Info", border_style="cyan bold", width=80)


def create_schema_table(response, console, is_source=True):
    key = "source_dataset" if is_source else "target_dataset"
    columns = response[key]["columns"]
    title = f"Schema: {response[key]['database']}.{response[key]['schema']}.{response[key]['table_name']}"
    mapped_columns = response["columns_mappings"]
    other_columns = response["target_dataset"]["columns"] if is_source else response["source_dataset"]["columns"]

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("#")
    table.add_column("Column Name", style="cyan")
    table.add_column("Data Type", style="magenta")
    table.add_column("Reason", style="red")

    for index, col in enumerate(columns, start=1):
        name = col["column_name"]
        data_type = col["data_type"]
        max_length = col.get("character_maximum_length", None)

        mapped_col = next(
            (
                m["target_column"] if is_source else m["source_column"]
                for m in mapped_columns
                if m["source_column" if is_source else "target_column"] == name
            ),
            None,
        )

        other_col = next((c for c in other_columns if c["column_name"] == (mapped_col or name)), None)

        mismatch_reason = ""
        if other_col:
            if data_type != other_col["data_type"]:
                mismatch_reason = "Data type mismatch"
            elif max_length != other_col.get("character_maximum_length", None):
                mismatch_reason = "Max length mismatch"
        else:
            mismatch_reason = "Exclusive to source" if is_source else "Exclusive to target"

        data_type_with_max_len = f"{data_type} {('('+ str(max_length) + ')') if max_length is not None else ''}"
        if mismatch_reason:
            table.add_row(
                str(index),
                Text(name, style="red"),
                Text(data_type_with_max_len, style="red"),
                mismatch_reason,
            )
        else:
            table.add_row(str(index), name, data_type_with_max_len, Text("-", style="green", justify="left"))
        col["mismatch_reason"] = mismatch_reason
    console.print(table)


def create_table_schema_row_count(response, row_diff_table, console):
    source_dataset = response["source_dataset"]
    target_dataset = response["target_dataset"]

    console.print(create_legend())
    table_row_counts = Table(title="Row Counts", show_header=True, header_style="bold magenta")
    table_row_counts.add_column("")
    table_row_counts.add_column(
        f"{source_dataset['database'] }.{source_dataset['schema']}.{source_dataset['table_name']}",
        style="cyan",
    )
    table_row_counts.add_column(
        f"{target_dataset['database']}.{target_dataset['schema']}.{target_dataset['table_name']}",
        style="yellow",
    )
    table_row_counts.add_row(
        "Row Count",
        str(source_dataset["row_count"]),
        str(target_dataset["row_count"]),
    )
    console.print(table_row_counts)

    create_schema_table(response, console, is_source=True)
    create_schema_table(response, console, is_source=False)

    if row_diff_table is not None:
        console.print(row_diff_table)


def differ_rows(
    diff_iter,
    response,
    limit: int | None = None,
    table_limit: int = 100,
    display_table: bool = False,
):
    stats = diff_iter.get_stats_dict()
    exclusive_source_set = set(stats["exclusive_source_ids"])
    exclusive_target_set = set(stats["exclusive_target_ids"])
    diff_values_set = set(stats["diff_values_ids"])
    source_duplicates = set(stats["duplicate_source_ids"])
    target_duplicates = set(stats["duplicate_target_ids"])
    pk_key_cols = response["source_dataset"]["primary_keys"]

    exclusive_to_source = []
    exclusive_to_target = []
    duplicates_in_source = []
    duplicates_in_target = []

    seen_ex_source = set()
    seen_ex_target = set()

    diff_pks_to_collect = set(diff_values_set) if limit is None else set(list(diff_values_set)[:limit])
    diff_records_dict = {}

    total_source_duplicates = 0
    total_target_duplicates = 0
    table_data = []
    table = None
    for diff in diff_iter:
        sign, rows = diff
        obj = {"meta": {"origin": "source" if sign == "-" else "target", "sign": sign}}
        column_values = {}

        for idx, col_ in enumerate(rows):
            column_name = response["columns_mappings"][idx]["source_column"]
            obj[column_name] = col_
            column_values[column_name] = col_
        if len(table_data) < table_limit:
            table_data.append(obj)
        pk_value = tuple(column_values[col] for col in pk_key_cols)

        if sign == "-" and pk_value in source_duplicates:
            total_source_duplicates += 1
            if limit is None or len(duplicates_in_source) < limit:
                duplicates_in_source.append(obj.copy())
            continue

        if sign == "+" and pk_value in target_duplicates:
            total_target_duplicates += 1
            if limit is None or len(duplicates_in_target) < limit:
                duplicates_in_target.append(obj.copy())
            continue

        if sign == "-" and pk_value in exclusive_source_set:
            if pk_value not in seen_ex_source and (limit is None or len(exclusive_to_source) < limit):
                exclusive_to_source.append(obj.copy())
                seen_ex_source.add(pk_value)

        elif sign == "+" and pk_value in exclusive_target_set:
            if pk_value not in seen_ex_target and (limit is None or len(exclusive_to_target) < limit):
                exclusive_to_target.append(obj.copy())
                seen_ex_target.add(pk_value)

        if pk_value in diff_pks_to_collect:
            if pk_value not in diff_records_dict:
                diff_records_dict[pk_value] = []
            if limit is None or len(diff_records_dict[pk_value]) < 2:
                diff_records_dict[pk_value].append(obj.copy())

    def sort_by_pk(obj):
        sort_key = []
        for col in pk_key_cols:
            pk_value = obj[col]
            try:
                sort_key.append((0, int(pk_value)))
            except (ValueError, TypeError):
                sort_key.append((1, str(pk_value)))
        return tuple(sort_key)

    try:
        exclusive_to_source.sort(key=sort_by_pk)
        exclusive_to_target.sort(key=sort_by_pk)
        duplicates_in_source.sort(key=sort_by_pk)
        duplicates_in_target.sort(key=sort_by_pk)
    except:
        pass

    records_with_differences = []
    for pk_value, records in diff_records_dict.items():
        records.sort(key=lambda x: x["meta"]["sign"], reverse=True)
        records_with_differences.extend(records)

    stats["total_diff_count"] = len(diff_values_set) + len(exclusive_source_set) + len(exclusive_target_set)
    stats["diff_rows_count"] = len(diff_values_set)
    stats.pop("exclusive_source_ids", None)
    stats.pop("exclusive_target_ids", None)
    stats.pop("diff_values_ids", None)
    stats.pop("duplicate_source_ids", None)
    stats.pop("duplicate_target_ids", None)
    stats["total_duplicate_count_source"] = total_source_duplicates
    stats["total_duplicate_count_target"] = total_target_duplicates
    try:
        diff_rows_percent = stats.get("diff_rows_count", 0) / (
            stats.get("diff_rows_count", 0) + stats.get("unchanged", 0)
        )
    except ZeroDivisionError:
        diff_rows_percent = 0.0
    stats["diff_rows_percent"] = diff_rows_percent
    primary_keys = response["source_dataset"]["primary_keys"]
    if display_table:
        table = create_table_diff_rows(table_data, primary_keys, response["columns_mappings"], 100)

    return {
        "exclusive_pk_values_target": exclusive_to_target,
        "exclusive_pk_values_source": exclusive_to_source,
        "duplicate_pk_values_source": duplicates_in_source,
        "duplicate_pk_values_target": duplicates_in_target,
        "records_with_differences": records_with_differences,
        "stats": stats,
        "table": table,
    }


def create_table_diff_rows(data, primary_keys: Union[str, list[str]], columns_mappings, limit: int = 100):
    table = Table(title="Diff Rows", show_header=True, header_style="bold magenta")
    column_mapping_dict = {mapping["source_column"]: mapping["target_column"] for mapping in columns_mappings}

    table.add_column("#")
    table.add_column("Origin")
    for mapping in columns_mappings:
        source_col = mapping["source_column"]
        target_col = mapping["target_column"]
        if source_col == target_col:
            table.add_column(source_col, style="cyan")
        else:
            table.add_column(f"{target_col}/{source_col}", style="cyan")

    if isinstance(primary_keys, str):
        primary_keys = [primary_keys]

    def get_composite_key(row):
        return tuple(row[key] for key in primary_keys)

    records = defaultdict(lambda: defaultdict(list))
    for row in data:
        composite_key = get_composite_key(row)
        origin = row["meta"]["origin"]
        records[composite_key][origin].append(row)

    previous_composite_key = None
    serial_number = 0
    unique_keys_processed = set()
    for row in data:
        composite_key = get_composite_key(row)
        if composite_key not in unique_keys_processed:
            if len(unique_keys_processed) >= limit:
                break
            serial_number += 1
        meta_values = row["meta"]
        row_values = {key: row[key] for key in column_mapping_dict.keys()}
        origin = meta_values["origin"]
        has_duplicates = any(len(records[composite_key][orig]) > 1 for orig in records[composite_key])

        mismatched_columns = set()
        if not has_duplicates:
            source_count = len(records[composite_key]["source"])
            target_count = len(records[composite_key]["target"])
            if source_count == 1 and target_count == 1:
                source_row = records[composite_key]["source"][0]
                target_row = records[composite_key]["target"][0]
                if origin == "target":
                    for col in column_mapping_dict.keys():
                        if source_row[col] != target_row[col]:
                            mismatched_columns.add(col)

        formatted_cells = [Text(str(serial_number))]
        for col in meta_values:
            if col != "sign":
                formatted_cells.append(
                    Text(
                        str(meta_values[col]),
                        style=f"{'chartreuse2' if meta_values['origin'] == 'source' else 'cyan3'}",
                    )
                )

        for col in column_mapping_dict.keys():
            cell_value = row_values[col]
            if has_duplicates:
                formatted_cells.append(Text(str(cell_value), style="yellow bold"))
            elif col in mismatched_columns:
                formatted_cells.append(Text(str(cell_value), style="red bold"))
            else:
                formatted_cells.append(Text(str(cell_value)))

        if previous_composite_key is not None and previous_composite_key != composite_key:
            table.add_section()

        table.add_row(*formatted_cells)
        previous_composite_key = composite_key
        unique_keys_processed.add(composite_key)
    return table
