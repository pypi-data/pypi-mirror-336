"""
Revised test suite covering additional scenarios and edge cases for rank_array_adapter.py.
"""

import pytest
import numpy as np
import pandas as pd

from ma_utils.rank_array_adapter import (
    RankShape,
    RankData,
    convert_rank_data,
    _validate_rankcol_no_midrow_nulls,
    _validate_rankcol_no_duplicates,
    _validate_itemcol_no_rank_duplicates,
    _string_array_to_numeric,
    _convert_ids_to_strings,
)


def test_invalid_from_shape():
    """
    Ensures an invalid from_shape raises ValueError.
    """
    data = np.array([[1, 2], [3, 4]], dtype=float)
    with pytest.raises(ValueError, match="Invalid 'from_shape' value"):
        convert_rank_data(data, "invalid_shape", RankShape.LISTROW_RANKCOL)


def test_invalid_to_shape():
    """
    Ensures an invalid to_shape raises ValueError.
    """
    data = np.array([[1, 2], [3, 4]], dtype=float)
    with pytest.raises(ValueError, match="Invalid 'to_shape' value"):
        convert_rank_data(data, RankShape.LISTROW_RANKCOL, "erroneous_shape")


def test_identical_from_to_shape():
    """
    Ensures a ValueError is raised when from_shape equals to_shape.
    """
    data = np.array([[1, 2], [3, 4]], dtype=float)
    with pytest.raises(
        ValueError, match="Input and output shapes must be different"
    ):
        convert_rank_data(
            data,
            from_shape=RankShape.LISTROW_RANKCOL,
            to_shape=RankShape.LISTROW_RANKCOL,
        )


def test_non_2d_input_raises_error():
    """
    Checks that non-2D arrays are handled appropriately or raise errors.
    """
    data_1d = np.array([1, 2, 3], dtype=float)
    # We expect something to break in validation or shape handling.
    with pytest.raises(ValueError):
        _validate_rankcol_no_midrow_nulls(data_1d)


def test_all_nan_array():
    """
    Confirms that an all-NaN array raises ValueError as expected.
    """
    data = np.full((2, 3), np.nan, dtype=float)
    with pytest.raises(ValueError):
        convert_rank_data(
            data,
            from_shape=RankShape.LISTROW_RANKCOL,
            to_shape=RankShape.LISTCOL_RANKROW,
        )


def test_extremely_large_item_ids():
    """
    Uses very large integer IDs to ensure no overflow or indexing issues arise.
    """
    data = np.array(
        [[1e9, 1e9 + 1, np.nan], [1e9 + 2, np.nan, np.nan]], dtype=float
    )
    rd = convert_rank_data(
        data,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTROW_ITEMCOL,
    )
    # Just confirming it processes and retains shape.
    assert rd.data.shape[0] == 2
    assert (
        rd.data.shape[1] == 3
    )  # largest item_id = 1e9+2 => column index= (1e9+2)-1
    # However, actual array creation that large is impractical, so short-circuit check:
    # We only confirm code doesn't raise an error here. Implementation detail:
    # For an actual environment, memory errors might occur.


def test_non_sequential_rank_values():
    """
    Ensures non-sequential rank values do not break the system.
    """
    arr = np.array([[2, 5, np.nan], [10, 12, 20]], dtype=float)
    rd = convert_rank_data(
        data=arr,
        from_shape=RankShape.LISTROW_ITEMCOL,
        to_shape=RankShape.LISTROW_RANKCOL,
    )
    # The resulting shape should be (2, 3) because each row has at most 3 ranked items.
    assert rd.data.shape == (2, 3)


def test_mixed_numeric_string_ids_listrow_rankcol():
    """
    Ensures a mix of string and numeric IDs can be handled.
    """
    data = np.array([["A", 10, None], [20, "B", None]], dtype=object)
    rd = convert_rank_data(
        data,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTROW_ITEMCOL,
        return_string_ids=False,
    )
    # We check that the code didn't raise and that a mapping was created.
    assert "item_to_id" in rd.item_mapping
    assert (
        "A" in rd.item_mapping["item_to_id"]
        or 10 in rd.item_mapping["item_to_id"]
    )


def test_custom_na_value():
    """
    Tests that a custom na_value is used in final output when return_string_ids=True.
    """
    data = np.array([["X", None], ["Y", None]], dtype=object)
    rd = convert_rank_data(
        data,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTCOL_RANKROW,
        return_string_ids=True,
        na_value="MISSING",
    )
    # Check the second rank positions (originally None) in each list (column)
    assert rd.data[1, 0] == "MISSING"  # First list's second rank
    assert rd.data[1, 1] == "MISSING"  # Second list's second rank


def test_id_mapping_reuse():
    initial_data = np.array(
        [["Apple", "Banana", None], ["Carrot", None, None]], dtype=object
    )
    # Convert to LISTCOL_RANKROW first to avoid same from/to shape
    rd_step1 = convert_rank_data(
        initial_data,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTCOL_RANKROW,
        return_string_ids=False,
    )
    # Reuse mapping from rd_step1 in new Data (adjust shape as needed)
    new_data = RankData(
        data=np.array([["Banana", "Date"]], dtype=object),
        item_mapping=rd_step1.item_mapping,
    )
    # Convert new data (adjust from_shape appropriately)
    rd_step2 = convert_rank_data(
        new_data,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTCOL_RANKROW,
        return_string_ids=False,
    )
    # Check ID mapping consistency
    banana_id_old = rd_step1.item_mapping["item_to_id"]["Banana"]
    banana_id_new = rd_step2.item_mapping["item_to_id"]["Banana"]
    assert banana_id_old == banana_id_new


def test_listcol_itemrow_to_listrow_itemcol_direct():
    """
    Ensures direct conversion from LISTCOL_ITEMROW to LISTROW_ITEMCOL.
    """
    arr = np.array([[1, np.nan], [np.nan, 2]], dtype=float)
    rd = convert_rank_data(
        arr,
        from_shape=RankShape.LISTCOL_ITEMROW,
        to_shape=RankShape.LISTROW_ITEMCOL,
    )
    # Each row is a list; each col is an item. Should not raise error.
    assert rd.data.shape == (arr.shape[1], int(np.nanmax(arr)))


def test_direct_string_array_to_numeric():
    """
    Tests _string_array_to_numeric directly for consistent ID assignment and NaN handling.
    """
    arr = np.array([["a", "b", None], [None, "c", "b"]], dtype=object)
    mapping = {}
    updated_mapping, num_arr = _string_array_to_numeric(arr, mapping)
    assert num_arr.shape == arr.shape
    assert not np.isnan(num_arr[0, 0])
    assert "a" in updated_mapping["item_to_id"]
    # Ensure that None mapped to np.nan
    assert np.isnan(num_arr[0, 2])


def test_direct_convert_ids_to_strings():
    """
    Tests _convert_ids_to_strings to ensure correct mapping back to item labels.
    """
    mapping = {"id_to_item": {1: "apple", 2: "banana"}}
    arr = np.array([[1, 2, np.nan]], dtype=float)
    str_arr = _convert_ids_to_strings(arr, mapping, na_value="missing")
    assert str_arr[0, 0] == "apple"
    assert str_arr[0, 1] == "banana"
    assert str_arr[0, 2] == "missing"


def test_listrow_rankcol_duplicate_detection():
    """Checks that a row with duplicate IDs raises a validation error."""
    arr = np.array([[1, 2, 2, np.nan], [10, 20, 30, 30]], dtype=float)
    with pytest.raises(ValueError, match="Duplicate item ID"):
        _validate_rankcol_no_duplicates(arr)


def test_listrow_rankcol_midrow_null_violation():
    """Checks that a non-null item after a null in a row raises an error."""
    arr = np.array([[5, np.nan, 7]], dtype=float)
    with pytest.raises(ValueError, match="Non-null item found after a null"):
        _validate_rankcol_no_midrow_nulls(arr)


def test_listcol_rankrow_round_trip():
    """
    Converts LISTCOL_RANKROW → LISTROW_RANKCOL, then back to LISTCOL_RANKROW.
    Checks final array shape equality.
    """
    original = np.array(
        [
            [1, 2],
            [3, 4],
            [np.nan, 5],
        ],
        dtype=float,
    )

    rd_canonical = convert_rank_data(
        data=original,
        from_shape=RankShape.LISTCOL_RANKROW,
        to_shape=RankShape.LISTROW_RANKCOL,
    )
    assert rd_canonical.data.shape == (2, 3)

    rd_final = convert_rank_data(
        data=rd_canonical.data,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTCOL_RANKROW,
    )
    np.testing.assert_array_equal(rd_final.data, original)


def test_listrow_itemcol_to_listrow_rankcol_simple():
    """
    Converts LISTROW_ITEMCOL → LISTROW_RANKCOL. Ensures shape is correct.
    """
    arr_itemcol = np.array([[1, 2, 3], [1, 2, np.nan]], dtype=float)

    rd = convert_rank_data(
        data=arr_itemcol,
        from_shape=RankShape.LISTROW_ITEMCOL,
        to_shape=RankShape.LISTROW_RANKCOL,
    )
    assert rd.data.shape == (2, 3)


def test_listrow_itemcol_duplicate_ranks():
    """Checks that duplicate rank values in one row of LISTROW_ITEMCOL raises error."""
    arr = np.array([[1, 2, 2], [np.nan, np.nan, 3]], dtype=float)
    with pytest.raises(ValueError, match="Duplicate rank"):
        _validate_itemcol_no_rank_duplicates(arr)


def test_listrow_rankcol_to_listrow_itemcol():
    """
    Converts LISTROW_RANKCOL → LISTROW_ITEMCOL.
    Checks final array shape matches the number of unique item IDs.
    """
    input_arr = np.array([[10, 20, 30], [12, 11, np.nan]], dtype=float)
    rd_itemcol = convert_rank_data(
        data=input_arr,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTROW_ITEMCOL,
    )
    # Unique item IDs are 10, 11, 12, 20, 30 → 5 columns
    assert rd_itemcol.data.shape == (2, 5)
    # Check specific positions
    assert rd_itemcol.data[0, 0] == 1  # Item 10 in first list has rank 1
    assert rd_itemcol.data[0, 3] == 2  # Item 20 in first list has rank 2
    assert rd_itemcol.data[0, 4] == 3  # Item 30 in first list has rank 3
    assert rd_itemcol.data[1, 1] == 2  # Item 11 in second list has rank 2


def test_listrow_rankcol_to_listcol_itemrow_multi_step():
    """
    Converts LISTROW_RANKCOL → LISTCOL_ITEMROW, checks the intermediate shape.
    Converts back to LISTROW_RANKCOL, confirming shape is correct.
    """
    input_arr = np.array([[101, 102, np.nan], [201, 202, 203]], dtype=float)

    rd_intermediate = convert_rank_data(
        data=input_arr,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTCOL_ITEMROW,
    )
    assert rd_intermediate.data.shape[1] == input_arr.shape[0]

    rd_final = convert_rank_data(
        data=rd_intermediate.data,
        from_shape=RankShape.LISTCOL_ITEMROW,
        to_shape=RankShape.LISTROW_RANKCOL,
    )
    assert rd_final.data.shape == input_arr.shape


def test_string_inputs_multi_step():
    """
    Provides a LISTROW_RANKCOL with string IDs. Converts to LISTCOL_RANKROW,
    checks shape and mapping, then converts back to LISTROW_RANKCOL.
    """
    arr_str = np.array(
        [["A", "B", "C", None], ["A", "X", None, None]], dtype=object
    )

    rd_step1 = convert_rank_data(
        data=arr_str,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTCOL_RANKROW,
        return_string_ids=False,
    )
    assert len(rd_step1.item_mapping["item_to_id"]) == 4
    assert rd_step1.data.shape == (4, 2)

    rd_step2 = convert_rank_data(
        data=rd_step1.data,
        from_shape=RankShape.LISTCOL_RANKROW,
        to_shape=RankShape.LISTROW_RANKCOL,
        return_string_ids=True,
    )
    assert rd_step2.data.shape == arr_str.shape


def test_dataframe_input_listrow_rankcol_to_listcol_rankrow():
    """
    Uses a DataFrame of string items from LISTROW_RANKCOL → LISTCOL_RANKROW.
    Checks shape and stored reference info.
    """
    df = pd.DataFrame(
        [["apple", "banana", "cherry", None], ["apple", "banana", None, None]],
        columns=["r1", "r2", "r3", "r4"],
    )

    rd = convert_rank_data(
        data=df,
        from_shape=RankShape.LISTROW_RANKCOL,
        to_shape=RankShape.LISTCOL_RANKROW,
        return_string_ids=False,
    )
    assert rd.data.shape == (4, 2)
    assert "dataframe_columns" in rd.original_info
    assert "apple" in rd.item_mapping["item_to_id"]


def test_listrow_itemcol_to_listcol_itemrow_with_strings():
    """
    Converts LISTROW_ITEMCOL with string columns → LISTCOL_ITEMROW.
    Checks shape.
    """
    df = pd.DataFrame(
        [[1, 2, np.nan], [3, np.nan, 1]],
        columns=["cat", "dog", "bird"],
        dtype=float,
    )

    rd = convert_rank_data(
        data=df,
        from_shape=RankShape.LISTROW_ITEMCOL,
        to_shape=RankShape.LISTCOL_ITEMROW,
        return_string_ids=True,
    )
    assert rd.data.shape == (3, 2)


def test_shape_mismatch_small_data():
    empty_arr = np.array([[]], dtype=float)
    # Expect error since empty array is rejected
    with pytest.raises(ValueError, match="All-empty arrays"):
        convert_rank_data(
            empty_arr,
            from_shape=RankShape.LISTROW_RANKCOL,
            to_shape=RankShape.LISTROW_ITEMCOL,
        )


def test_listrow_rankcol_strict_validation():
    """
    Validates a properly formed LISTROW_RANKCOL with trailing nans and no duplicates.
    """
    arr = np.array([[1, 2, 3, np.nan], [4, 5, np.nan, np.nan]], dtype=float)
    _validate_rankcol_no_midrow_nulls(arr)
    _validate_rankcol_no_duplicates(arr)


def test_itemcol_rank_duplicates_error():
    """Checks that duplicating a rank in the same row for ITEMCOL is invalid."""
    arr = np.array([[1, 1], [2, np.nan]], dtype=float)
    with pytest.raises(ValueError, match="Duplicate rank"):
        convert_rank_data(
            data=arr,
            from_shape=RankShape.LISTROW_ITEMCOL,
            to_shape=RankShape.LISTROW_RANKCOL,
        )
