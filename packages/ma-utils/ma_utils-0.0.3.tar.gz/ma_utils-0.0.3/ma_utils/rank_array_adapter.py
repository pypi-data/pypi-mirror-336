"""
This module provides functionality to convert rank-based data among four recognized shapes:
    1) LISTROW_RANKCOL: Each row represents a list. Each column position in that row
       corresponds to an item in ascending rank order. The cell value is the numeric
       ID of that item. Trailing columns in a row may be NaN if that row has fewer items
       than others. Once a row encounters a NaN, no subsequent non-NaN is allowed
       in the same row. No item ID may appear more than once in a row.

    2) LISTCOL_RANKROW: The transpose of LISTROW_RANKCOL. Each column is a list, and
       each row position in that column corresponds to an item in ascending rank order.
       The cell value is the numeric ID of that item.

    3) LISTROW_ITEMCOL: Each row represents a list. Each column represents a specific
       item (where the numeric ID is the column index in practice). The cell value
       in row i, column j is the rank of item j in list i. If a cell is NaN, item j
       is absent from list i. No rank value may appear more than once in the same row.

    4) LISTCOL_ITEMROW: The transpose of LISTROW_ITEMCOL. Each column is a list, and
       each row represents an item. The cell value is the rank of that item in that list.
       No rank value may appear more than once in the same column.

The input to the main conversion function must be a 2D NumPy array, strictly numeric. This
greatly simplifies internal transformations and avoids complex handling of user-provided
labels or string-based item identifiers. For shapes where items are located along rows
or columns, the actual item “ID” is the corresponding row or column index. For shapes
where the cells themselves contain item IDs, the numeric cell values directly serve as
the item identifiers.

The conversion proceeds via a canonical form: LISTROW_RANKCOL. For any input shape,
we first convert to LISTROW_RANKCOL, then convert from that canonical form to the
desired output shape. The transformations and validations ensure data consistency,
such as preventing mid-row NaNs followed by non-NaNs in RANKCOL forms, or preventing
duplicate rank values in ITEMCOL forms.

When converting to an ITEMCOL or ITEMROW format, an ID→index mapping is created and
returned so that downstream processes can interpret which row/column index corresponds
to which original numeric ID. If the target shape is RANKCOL or RANKROW, no mapping is
needed, so an empty dictionary is returned.
"""

import numpy as np
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Tuple


class RankShape(str, Enum):
    """
    Enumerates the recognized shapes for rank-based data.

    LISTROW_RANKCOL:
        Each row represents a list, columns represent rank positions.
        Cell values are numeric item IDs in ascending rank order.
        No duplicates in a row, no non-NaN cells after the first NaN in a row.

    LISTCOL_RANKROW:
        Each column represents a list, rows represent rank positions.
        Cell values are numeric item IDs in ascending rank order.

    LISTROW_ITEMCOL:
        Each row represents a list, columns represent item IDs (by column index),
        and cell values store that item's rank in the list. No rank is repeated
        within the same row.

    LISTCOL_ITEMROW:
        Each column represents a list, rows represent item IDs (by row index),
        and cell values store that item's rank in the list. No rank is repeated
        within the same column.
    """

    LISTROW_RANKCOL = "listrow_rankcol"
    LISTCOL_RANKROW = "listcol_rankrow"
    LISTROW_ITEMCOL = "listrow_itemcol"
    LISTCOL_ITEMROW = "listcol_itemrow"


@dataclass
class RankDataAdapter:
    """
    Container for the converted rank data and optional mapping from item IDs
    to row/column indices in the output array.

    Attributes
    ----------
    data : np.ndarray
        The converted 2D numeric array representing rank data in the desired shape.
    id_to_index_mapping : Dict[float, int]
        Mapping of numeric item ID to index in the output array’s row or column axis.
        This only applies when shapes of type ITEMCOL or ITEMROW are produced. If
        the output shape is RANKCOL or RANKROW, this dictionary will be empty.
    """

    data: np.ndarray
    id_to_index_mapping: Dict[float, int]


def convert_rank_data(
    data: np.ndarray,
    from_shape: RankShape,
    to_shape: RankShape,
    na_value: Any = np.nan,
) -> RankDataAdapter:
    """
    Converts 2D numeric rank data between the specified input shape and output shape.

    Parameters
    ----------
    data : np.ndarray
        A 2D numeric array representing the rank data in the format indicated
        by 'from_shape'.
    from_shape : RankShape
        The shape of the given rank data. Must be one of the four recognized shapes.
    to_shape : RankShape
        The desired shape for the rank data. Must be different from 'from_shape'.
    na_value : Any, default=np.nan
        The placeholder for missing or absent data in the output array.

    Returns
    -------
    RankDataAdapter
        A dataclass containing the converted rank data in 'data', and the optional
        'id_to_index_mapping' if the output shape is ITEMCOL or ITEMROW.

    Raises
    ------
    ValueError
        If invalid shapes are provided, 'from_shape' equals 'to_shape', data is not
        a 2D numeric array, data is empty or all-NaN, or data violates the shape
        constraints (e.g., duplicates where forbidden, or non-NaN after a NaN in a row).
    """
    # Validate shape arguments
    if not isinstance(from_shape, RankShape):
        try:
            from_shape = RankShape(from_shape)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid 'from_shape': {from_shape!r}")

    if not isinstance(to_shape, RankShape):
        try:
            to_shape = RankShape(to_shape)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid 'to_shape': {to_shape!r}")

    if from_shape == to_shape:
        raise ValueError("Input and output shapes must be different.")

    # Validate data is a 2D numpy array
    if not isinstance(data, np.ndarray):
        raise ValueError("Input 'data' must be a NumPy array.")
    if data.ndim != 2:
        raise ValueError("Input 'data' must be 2D.")

    # Validate numeric dtype
    if not np.issubdtype(data.dtype, np.number):
        raise ValueError("Input 'data' must be numeric.")

    # Copy to avoid side effects
    data_in = data.astype(float, copy=True)

    # Check for empty or all-NaN
    if data_in.size == 0:
        raise ValueError("Input 'data' array is empty.")
    if np.all(np.isnan(data_in)):
        raise ValueError("All-NaN arrays are not allowed.")

    # Convert to canonical shape
    canonical_arr = _to_canonical_listrow_rankcol(data_in, from_shape)

    # Convert from canonical shape to requested
    converted_arr, id_map = _from_canonical_listrow_rankcol(
        canonical_arr, to_shape, na_value
    )

    return RankDataAdapter(data=converted_arr, id_to_index_mapping=id_map)


def _to_canonical_listrow_rankcol(
    data_in: np.ndarray,
    shape_in: RankShape,
) -> np.ndarray:
    """
    Converts a numeric rank array in the indicated 'shape_in' to the canonical
    LISTROW_RANKCOL shape.

    Parameters
    ----------
    data_in : np.ndarray
        A 2D numeric array in one of the recognized shapes.
    shape_in : RankShape
        Declared shape of 'data_in'.

    Returns
    -------
    np.ndarray
        A new 2D numeric array in the LISTROW_RANKCOL shape.

    Raises
    ------
    ValueError
        If the data violates shape constraints (e.g., duplicates in a row,
        repeated ranks, or non-NaN after a NaN in RANKCOL).
    """
    if shape_in == RankShape.LISTROW_RANKCOL:
        _validate_rankcol_no_midrow_nulls(data_in)
        _validate_rankcol_no_duplicates(data_in)
        return data_in.copy()

    if shape_in == RankShape.LISTCOL_RANKROW:
        arr_t = data_in.T
        _validate_rankcol_no_midrow_nulls(arr_t)
        _validate_rankcol_no_duplicates(arr_t)
        return arr_t

    if shape_in == RankShape.LISTROW_ITEMCOL:
        _validate_itemcol_no_rank_duplicates(data_in)
        return _item_indices_to_listrow_rankcol(data_in)

    # shape_in == RankShape.LISTCOL_ITEMROW
    arr_t = data_in.T
    _validate_itemcol_no_rank_duplicates(arr_t)
    return _item_indices_to_listrow_rankcol(arr_t)


def _item_indices_to_listrow_rankcol(arr_itemcol: np.ndarray) -> np.ndarray:
    """
    Converts a LISTROW_ITEMCOL-like array to the canonical LISTROW_RANKCOL shape.
    The input array's rows are separate lists, columns represent unique item IDs
    (numerically by the column index), and the cell values are ranks.

    Each row i is processed by reading all (rank, column_index) pairs. The column
    index is treated as the item ID, and the rank is used to determine ordering.
    The output's row i will list the item IDs in ascending rank order.

    Parameters
    ----------
    arr_itemcol : np.ndarray
        2D numeric array, each row is a list, each column is an item ID (the column index),
        and cell values are ranks.

    Returns
    -------
    np.ndarray
        The converted array in the LISTROW_RANKCOL shape, where each row is a list
        and the columns are item IDs in ascending rank order, padded by NaN.

    Raises
    ------
    ValueError
        If shape constraints are violated after conversion (e.g., duplicates
        or non-NaN after a NaN in a row).
    """
    rows, cols = arr_itemcol.shape
    max_length = 0
    all_rows_data = []

    for i in range(rows):
        row_ranks = arr_itemcol[i, :]
        valid_mask = ~np.isnan(row_ranks)
        # List of (rank_value, item_id)
        row_pairs = [(row_ranks[j], j) for j in range(cols) if valid_mask[j]]

        # Sort by ascending rank, then by item_id if needed
        row_pairs.sort(key=lambda x: (x[0], x[1]))

        # Extract sorted item_ids
        sorted_item_ids = [pair[1] for pair in row_pairs]
        max_length = max(max_length, len(sorted_item_ids))
        all_rows_data.append(sorted_item_ids)

    # Construct the output array
    out_arr = np.full((rows, max_length), np.nan, dtype=float)
    for i, item_ids in enumerate(all_rows_data):
        out_arr[i, : len(item_ids)] = item_ids

    _validate_rankcol_no_midrow_nulls(out_arr)
    _validate_rankcol_no_duplicates(out_arr)
    return out_arr


def _from_canonical_listrow_rankcol(
    data_canonical: np.ndarray,
    shape_out: RankShape,
    na_value: Any,
) -> Tuple[np.ndarray, Dict[float, int]]:
    """
    Converts a canonical LISTROW_RANKCOL array to the requested 'shape_out'.

    Parameters
    ----------
    data_canonical : np.ndarray
        A 2D numeric array in LISTROW_RANKCOL shape.
    shape_out : RankShape
        The desired output shape.
    na_value : Any
        A placeholder for missing or absent data in the output.

    Returns
    -------
    (converted_array, id_map)
        converted_array : np.ndarray
            The 2D numeric array in the requested shape.
        id_map : Dict[float, int]
            The mapping of numeric item ID to the row/column index in the output
            if the shape is ITEMCOL or ITEMROW. Empty otherwise.

    Raises
    ------
    ValueError
        If constraints are violated (e.g., expanding to an unreasonable
        number of columns/rows).
    """
    if shape_out == RankShape.LISTROW_RANKCOL:
        return data_canonical.copy(), {}

    if shape_out == RankShape.LISTCOL_RANKROW:
        return data_canonical.T, {}

    # Expanding to item-based shapes
    arr_itemcol, id_map = _rankcol_to_item_indices(data_canonical, na_value)

    if shape_out == RankShape.LISTROW_ITEMCOL:
        return arr_itemcol, id_map

    # shape_out == RankShape.LISTCOL_ITEMROW
    return arr_itemcol.T, id_map


def _rankcol_to_item_indices(
    data_rankcol: np.ndarray, na_value: Any
) -> Tuple[np.ndarray, Dict[float, int]]:
    """
    Expands a LISTROW_RANKCOL array into an item-based format (LISTROW_ITEMCOL).
    Each row remains a list, columns represent unique item IDs, and each cell
    is the rank of that item in that row.

    Parameters
    ----------
    data_rankcol : np.ndarray
        A 2D numeric array in the LISTROW_RANKCOL shape.
    na_value : Any
        Value to fill for absences.

    Returns
    -------
    (out_arr, id_map)
        out_arr : np.ndarray
            A 2D numeric array in the LISTROW_ITEMCOL shape.
        id_map : Dict[float, int]
            Mapping from numeric item ID to its column index in 'out_arr'.

    Raises
    ------
    ValueError
        If the number of distinct item IDs is excessively large (e.g. >100000),
        or if all rows have no valid items.
    """
    rows, cols = data_rankcol.shape
    # Gather valid item IDs across all rows
    valid_ids_list = []
    for i in range(rows):
        row_vals = data_rankcol[i, :]
        valid_mask = ~np.isnan(row_vals)
        item_ids = row_vals[valid_mask]
        if len(item_ids) > 0:
            valid_ids_list.append(item_ids)

    if not valid_ids_list:
        raise ValueError(
            "No valid item IDs found; cannot build item-based structure."
        )

    all_ids = np.unique(np.concatenate(valid_ids_list))
    # Filter NaN just in case
    all_ids = all_ids[~np.isnan(all_ids)]

    if len(all_ids) > 100000:
        raise ValueError(
            f"Detected {len(all_ids)} distinct item IDs, too large for expansion."
        )

    sorted_ids = np.sort(all_ids)
    id_to_index = {id_val: idx for idx, id_val in enumerate(sorted_ids)}

    # Build the expanded array, shape: (rows, number_of_unique_items)
    out_arr = np.full((rows, len(sorted_ids)), na_value, dtype=float)

    # Fill each row with rank=column-position + 1
    for i in range(rows):
        row_vals = data_rankcol[i, :]
        valid_mask = ~np.isnan(row_vals)
        item_ids = row_vals[valid_mask]
        for rank_pos, item_id in enumerate(item_ids):
            out_col = id_to_index[item_id]
            out_arr[i, out_col] = rank_pos + 1

    return out_arr, id_to_index


def _validate_rankcol_no_midrow_nulls(arr: np.ndarray) -> None:
    """
    Ensures that in a LISTROW_RANKCOL adaptation, once a row encounters a NaN value
    (indicating no further items), there are no subsequent non-NaN cells in that row.
    """
    rows, cols = arr.shape
    for i in range(rows):
        encountered_nan = False
        for j in range(cols):
            val = arr[i, j]
            if np.isnan(val):
                encountered_nan = True
            else:
                if encountered_nan:
                    raise ValueError(
                        f"Row {i} has a non-NaN after a NaN, violating RANKCOL structure."
                    )


def _validate_rankcol_no_duplicates(arr: np.ndarray) -> None:
    """
    Ensures that no row in a LISTROW_RANKCOL array contains duplicate item IDs.
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
                    f"Found duplicate item ID {val} in row {i}, violating RANKCOL structure."
                )
            seen.add(val)


def _validate_itemcol_no_rank_duplicates(arr_itemcol: np.ndarray) -> None:
    """
    Ensures that no row in a LISTROW_ITEMCOL array repeats a rank value.
    This also applies to the transposed input for LISTCOL_ITEMROW validation.
    """
    rows, cols = arr_itemcol.shape
    for i in range(rows):
        seen_ranks = set()
        for j in range(cols):
            rank_val = arr_itemcol[i, j]
            if np.isnan(rank_val):
                continue
            if rank_val in seen_ranks:
                raise ValueError(
                    f"Row {i} has a duplicate rank value {rank_val}, violating ITEMCOL structure."
                )
            seen_ranks.add(rank_val)
