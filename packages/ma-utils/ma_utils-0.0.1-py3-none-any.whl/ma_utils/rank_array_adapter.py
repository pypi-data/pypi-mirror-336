"""
rank_array_adapter.py

Provides functionality to convert rank-based data among multiple formats:

    1A) LISTROW_RANKCOL (list as row, rank position as column, storing item IDs)
    1B) LISTCOL_RANKROW (list as column, rank position as row, storing item IDs)
    2A) LISTROW_ITEMCOL (rows as lists, columns as distinct items, storing rank values)
    2B) LISTCOL_ITEMROW (columns as lists, rows as distinct items, storing rank values)

This module enforces consistent handling and ensures the final return is always a
numeric NumPy array, optionally mapping string item identifiers to integer IDs
internally. If desired, the final array can be converted back to string IDs.

Key Features:
- The input can be a NumPy array, pandas DataFrame, or a RankData object.
- The output is always a RankData containing a strictly numeric array unless
  return_string_ids=True, in which case internal integer IDs map back to strings.
- Unequal-length lists in 1A/1B are handled by trailing NaNs; for 2A/2B, items unranked
  in a list become NaN. Midrow nulls or duplicated ranks/items within the same list
  are disallowed by design.
- The canonical internal representation is LISTROW_RANKCOL. A dictionary tracks
  string ↔ integer relationships so repeated conversions remain consistent.
- All-empty or all-NaN arrays are rejected as invalid.

"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Optional, Union, Dict, Any, Tuple
from enum import Enum


class RankShape(str, Enum):
    """
    Enumerates rank data shapes:

    LISTROW_RANKCOL : Rows correspond to individual lists; columns are rank positions
                      containing item identifiers at each position.
    LISTCOL_RANKROW : Columns correspond to individual lists; rows are rank positions
                      containing item identifiers at each position.
    LISTROW_ITEMCOL : Rows are individual lists; columns are distinct items; values
                      are rank positions for that item in the list.
    LISTCOL_ITEMROW : Columns are individual lists; rows are distinct items; values
                      are rank positions for that item in the list.
    """

    LISTROW_RANKCOL = "listrow_rankcol"
    LISTCOL_RANKROW = "listcol_rankrow"
    LISTROW_ITEMCOL = "listrow_itemcol"
    LISTCOL_ITEMROW = "listcol_itemrow"


@dataclass
class RankData:
    """
    Container for rank data and associated item mapping.

    data : np.ndarray of numeric IDs or rank values.
    item_mapping : Dict tracking item→ID and ID→item if strings were encountered.
    original_info : Optional dict storing extra metadata (DataFrame columns, etc.).
    """

    data: np.ndarray
    item_mapping: Dict[str, Any]
    original_info: Optional[Dict[str, Any]] = None

    def to_string_array(self, na_value: Any = np.nan) -> np.ndarray:
        """
        Converts integer IDs in 'data' back to item strings using 'item_mapping'.

        Parameters
        ----------
        na_value : Any, default=np.nan
            Value to place where no mapping is found or IDs are NaN.

        Returns
        -------
        np.ndarray of object
        """
        return _convert_ids_to_strings(self.data, self.item_mapping, na_value)


def convert_rank_data(
    data: Union[np.ndarray, pd.DataFrame, RankData],
    from_shape: RankShape,
    to_shape: RankShape,
    return_string_ids: bool = False,
    na_value: Any = np.nan,
) -> RankData:
    """
    Converts rank data between supported shapes, returning a RankData object
    with a NumPy array. If return_string_ids=True, these numeric IDs are mapped
    back to strings per the internal mapping.

    Parameters
    ----------
    data : np.ndarray, pd.DataFrame, or RankData
        Input rank data. If a DataFrame, we record index/columns in 'original_info'
        but otherwise treat .values as numeric or object for item IDs. If a RankData,
        the .data attribute is used, and its item_mapping is reused.
    from_shape : RankShape
        The shape format of the given data.
    to_shape : RankShape
        Desired output shape format.
    return_string_ids : bool, default=False
        Whether to map final numeric IDs back to strings in the output array.
    na_value : Any, default=np.nan
        Representation of missing data in the final array.

    Returns
    -------
    RankData
        Contains:
            data : A NumPy array of numeric or string item references.
            item_mapping : Dictionary mapping strings↔integers if strings were found.
            original_info : Possibly includes shape information or DataFrame metadata.

    Raises
    ------
    ValueError
        If from_shape or to_shape is invalid, or shapes are identical,
        or input is not a 2D array, or the entire array is empty/all-NaN,
        or if data violates format constraints (duplicate items, out-of-order NaNs, etc.).
    """
    # Validate shapes
    # Replace the current validation with:
    if not isinstance(from_shape, RankShape):
        try:
            from_shape = RankShape(from_shape)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid 'from_shape' value: {from_shape}")

    if not isinstance(to_shape, RankShape):
        try:
            to_shape = RankShape(to_shape)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid 'to_shape' value: {to_shape}")

    if from_shape == to_shape:
        raise ValueError("Input and output shapes must be different.")

    # Extract underlying data
    if isinstance(data, RankData):
        numeric_input = data.data
        mapping_in = data.item_mapping
        original_info = data.original_info
    elif isinstance(data, pd.DataFrame):
        numeric_input = data.values
        mapping_in = {}
        original_info = {
            "dataframe_columns": data.columns.tolist(),
            "dataframe_index": data.index.tolist(),
        }
    else:
        numeric_input = np.array(data, copy=True)
        mapping_in = {}
        original_info = None

    # Enforce 2D array
    if numeric_input.ndim != 2:
        raise ValueError("Input data must be a 2D array.")

    # If it's object dtype, attempt converting strings to numeric IDs
    if numeric_input.dtype == object:
        mapping_in, numeric_input = _string_array_to_numeric(
            numeric_input, mapping_in
        )

    # Check if array is empty or all-NaN
    if numeric_input.size == 0:
        raise ValueError("All-empty arrays are not allowed.")
    if np.isnan(numeric_input).all():
        raise ValueError("All-NaN arrays are not allowed.")

    # Convert: from_shape => canonical => to_shape
    canonical_arr, mapping_in = _to_canonical_listrow_rankcol(
        numeric_input, from_shape, mapping_in
    )
    converted_arr = _from_canonical_listrow_rankcol(
        canonical_arr, to_shape, na_value
    )

    # If returning strings, map numeric IDs back
    if return_string_ids:
        final_arr = _convert_ids_to_strings(converted_arr, mapping_in, na_value)
    else:
        final_arr = converted_arr

    return RankData(
        data=final_arr, item_mapping=mapping_in, original_info=original_info
    )


def _string_array_to_numeric(
    arr: np.ndarray, mapping: Dict[str, Any]
) -> Tuple[Dict[str, Any], np.ndarray]:
    """
    Maps string (or any non-NaN object) items in 'arr' to numeric IDs, reusing or updating
    'mapping' in place. Values that are None or np.nan remain np.nan in the output array.

    Parameters
    ----------
    arr : np.ndarray of object
        The array potentially containing strings or other object types.
    mapping : dict
        Must contain or be populated with item_to_id and id_to_item for consistent usage.
    na_value : Any
        Representation for missing values in the final numeric array.

    Returns
    -------
    updated_mapping : dict
        item_to_id and id_to_item updated with new items if encountered.
    numeric_arr : np.ndarray
        Float array where known objects are replaced by numeric IDs, and None/NaN remain NaN.
    """
    item_to_id = mapping.setdefault("item_to_id", {})
    id_to_item = mapping.setdefault("id_to_item", {})

    # Start next_id from max existing or 0 if empty
    max_existing_id = max(id_to_item.keys(), default=0)
    next_id = max_existing_id + 1

    # Create a new numeric array
    numeric_arr = np.full(arr.shape, np.nan, dtype=float)
    rows, cols = arr.shape

    for i in range(rows):
        for j in range(cols):
            val = arr[i, j]
            # Treat None or NaN as missing
            if val is None or (isinstance(val, float) and np.isnan(val)):
                continue
            # If not in mapping, assign a new ID
            if val not in item_to_id:
                item_to_id[val] = next_id
                id_to_item[next_id] = val
                next_id += 1
            numeric_arr[i, j] = item_to_id[val]

    return mapping, numeric_arr


def _to_canonical_listrow_rankcol(
    data_in: np.ndarray,
    shape_in: RankShape,
    mapping: Dict[str, Any],
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Converts any recognized shape (1A,1B,2A,2B) to the canonical LISTROW_RANKCOL.

    Parameters
    ----------
    data_in : np.ndarray
        A 2D array of numeric IDs or rank values, possibly containing np.nan.
    shape_in : RankShape
        The shape format of data_in.
    mapping : dict
        item_to_id, id_to_item used for referencing item IDs.
    na_value : Any
        Missing value representation.

    Returns
    -------
    canonical_arr : np.ndarray
        A 2D array in LISTROW_RANKCOL format (rows=lists, columns=rank positions).
    updated_mapping : dict
        Possibly updated mapping (if new item labels discovered).
    """
    if shape_in == RankShape.LISTROW_RANKCOL:
        _validate_rankcol_no_midrow_nulls(data_in)
        _validate_rankcol_no_duplicates(data_in)
        return data_in, mapping

    if shape_in == RankShape.LISTCOL_RANKROW:
        arr_t = data_in.T
        _validate_rankcol_no_midrow_nulls(arr_t)
        _validate_rankcol_no_duplicates(arr_t)
        return arr_t, mapping

    if shape_in == RankShape.LISTROW_ITEMCOL:
        _validate_itemcol_no_rank_duplicates(data_in)
        out_arr, mapping = _listrow_itemcol_to_listrow_rankcol_with_labels(
            data_in, np.arange(data_in.shape[1]), mapping
        )
        return out_arr, mapping

    # shape_in == RankShape.LISTCOL_ITEMROW
    arr_t = data_in.T
    _validate_itemcol_no_rank_duplicates(arr_t)
    out_arr, mapping = _listrow_itemcol_to_listrow_rankcol_with_labels(
        arr_t, np.arange(arr_t.shape[1]), mapping
    )
    return out_arr, mapping


def _from_canonical_listrow_rankcol(
    data_canonical: np.ndarray,
    shape_out: RankShape,
    na_value: Any,
) -> np.ndarray:
    """
    Converts canonical LISTROW_RANKCOL to the desired shape (1A,1B,2A,2B).

    Parameters
    ----------
    data_canonical : np.ndarray
        2D numeric array in LISTROW_RANKCOL format (rows=lists, cols=rank positions).
    shape_out : RankShape
        Target shape.
    na_value : Any
        Representation for missing values. This can be float('nan') or another sentinel.

    Returns
    -------
    np.ndarray
        2D array in the requested shape, with numeric item IDs or rank values.
    """
    if shape_out == RankShape.LISTROW_RANKCOL:
        return data_canonical.copy()

    if shape_out == RankShape.LISTCOL_RANKROW:
        return data_canonical.T

    if shape_out == RankShape.LISTROW_ITEMCOL:
        return _listrow_rankcol_to_listrow_itemcol(data_canonical, na_value)

    # shape_out == RankShape.LISTCOL_ITEMROW
    arr_itemcol = _listrow_rankcol_to_listrow_itemcol(data_canonical, na_value)
    return arr_itemcol.T


def _listrow_itemcol_to_listrow_rankcol_with_labels(
    arr_itemcol: np.ndarray,
    column_labels: np.ndarray,
    mapping: Dict[str, Any],
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Converts LISTROW_ITEMCOL data to the canonical LISTROW_RANKCOL by sorting columns
    within each row by ascending rank value.
    """
    item_to_id = mapping.setdefault("item_to_id", {})
    id_to_item = mapping.setdefault("id_to_item", {})

    next_id = max(id_to_item.keys(), default=0) + 1
    rows, cols = arr_itemcol.shape
    max_length = 0
    rowwise_items = []

    for i in range(rows):
        row_entries = []
        for col_idx in range(cols):
            rank_val = arr_itemcol[i, col_idx]
            if np.isnan(rank_val):
                continue
            label = column_labels[col_idx]
            if label not in item_to_id:
                item_to_id[label] = next_id
                id_to_item[next_id] = label
                next_id += 1
            row_entries.append((rank_val, item_to_id[label]))
        row_entries.sort(key=lambda x: (x[0], x[1]))
        item_ids = [x[1] for x in row_entries]
        max_length = max(max_length, len(item_ids))
        rowwise_items.append(item_ids)

    out_arr = np.full((rows, max_length), np.nan, dtype=float)
    for i, items in enumerate(rowwise_items):
        for j, item_id in enumerate(items):
            out_arr[i, j] = item_id

    _validate_rankcol_no_midrow_nulls(out_arr)
    _validate_rankcol_no_duplicates(out_arr)

    return out_arr, mapping


def _listrow_rankcol_to_listrow_itemcol(
    data_rankcol: np.ndarray, na_value: Any
) -> np.ndarray:
    """
    Converts LISTROW_RANKCOL to LISTROW_ITEMCOL:
    - For each row, the position in the row is the rank of that item.
    - Gathers all unique item IDs across all rows and expands columns accordingly.

    If the max item ID for expansion is too large (over 100000 by default),
    this raises ValueError due to impractical array size.

    Parameters
    ----------
    data_rankcol : np.ndarray
        2D numeric array in LISTROW_RANKCOL format (rows=lists, cols=rank positions).
    na_value : Any
        Representation for missing data in the final array.

    Returns
    -------
    np.ndarray of shape (n_rows, max_id), storing rank positions or na_value.
    """
    rows, cols = data_rankcol.shape

    # Gather all item IDs ignoring NaNs
    valid_ids_list = []
    for i in range(rows):
        valid_ids = data_rankcol[i, ~np.isnan(data_rankcol[i])]
        if len(valid_ids) > 0:
            valid_ids_list.append(valid_ids)

    if not valid_ids_list:
        raise ValueError(
            "No valid items found in rank data; cannot build item columns."
        )

    all_ids = np.unique(np.concatenate(valid_ids_list))
    sorted_ids = np.sort(all_ids)

    # Memory feasibility check
    if len(sorted_ids) > 100000:
        raise ValueError(
            f"Detected {len(sorted_ids)} distinct item IDs which exceed 100000; "
            "cannot expand columns that large."
        )

    id_to_col = {val: idx for idx, val in enumerate(sorted_ids)}
    out_arr = np.full((rows, len(sorted_ids)), na_value, dtype=float)

    for i in range(rows):
        row_valid = ~np.isnan(data_rankcol[i])
        row_ids = data_rankcol[i, row_valid]
        for rank_pos, item_id in enumerate(row_ids, start=1):
            col_idx = id_to_col[item_id]
            out_arr[i, col_idx] = rank_pos

    return out_arr


def _convert_ids_to_strings(
    arr: np.ndarray, mapping: Dict[str, Any], na_value: Any
) -> np.ndarray:
    """
    Converts numeric IDs to string labels via mapping['id_to_item']. Cells become
    'na_value' for invalid or NaN IDs.
    """
    id_to_item = mapping.get("id_to_item", {})
    output = np.full(arr.shape, na_value, dtype=object)
    rows, cols = arr.shape

    for i in range(rows):
        for j in range(cols):
            val = arr[i, j]
            if isinstance(val, float) and np.isnan(val):
                continue
            mapped_item = id_to_item.get(int(val), na_value)
            output[i, j] = mapped_item

    return output


def _validate_rankcol_no_midrow_nulls(arr: np.ndarray) -> None:
    """
    Ensures that for each row in a LISTROW_RANKCOL layout, once NaN appears,
    no subsequent non-NaN values may appear.
    """
    rows, cols = arr.shape
    for i in range(rows):
        found_null = False
        for j in range(cols):
            val = arr[i, j]
            if np.isnan(val):
                found_null = True
            else:
                if found_null:
                    raise ValueError(
                        f"Non-null item found after a null in row {i}; "
                        "violates trailing-null requirement for LISTROW_RANKCOL."
                    )


def _validate_rankcol_no_duplicates(arr: np.ndarray) -> None:
    """
    Ensures no duplicated item IDs appear in the same row of a LISTROW_RANKCOL array.
    """
    rows, cols = arr.shape
    for i in range(rows):
        seen = set()
        for j in range(cols):
            val = arr[i, j]
            if np.isnan(val):
                continue
            if val in seen:
                raise ValueError(
                    f"Duplicate item ID {val} found in row {i}; "
                    "not allowed in LISTROW_RANKCOL."
                )
            seen.add(val)


def _validate_itemcol_no_rank_duplicates(arr_itemcol: np.ndarray) -> None:
    """
    Ensures that no rank value is repeated within the same row for LISTROW_ITEMCOL
    or LISTCOL_ITEMROW data.
    """
    rows, cols = arr_itemcol.shape
    for i in range(rows):
        seen_ranks = set()
        for j in range(cols):
            val = arr_itemcol[i, j]
            if np.isnan(val):
                continue
            if val in seen_ranks:
                raise ValueError(
                    f"Duplicate rank {val} found in row {i}; "
                    "violates LISTROW_ITEMCOL / LISTCOL_ITEMROW uniqueness."
                )
            seen_ranks.add(val)
