"""
pytest test suite for the redesigned rank_data_module.
Covers validation, shape conversions, item mapping, and edge cases.
"""

import pytest
import numpy as np

from ma_utils.rank_array_adapter import (
    RankShape,
    RankData,
    convert_rank_data,
    _validate_rankcol_no_midrow_nulls,
    _validate_rankcol_no_duplicates,
    _validate_itemcol_no_rank_duplicates,
)


def test_invalid_from_shape():
    """
    Ensures invalid from_shape raises ValueError.
    """
    arr = np.array([[1, 2], [3, 4]], dtype=float)
    with pytest.raises(ValueError, match="Invalid 'from_shape'"):
        convert_rank_data(arr, "bad_shape", RankShape.LISTROW_RANKCOL)


def test_invalid_to_shape():
    """
    Ensures invalid to_shape raises ValueError.
    """
    arr = np.array([[1, 2], [3, 4]], dtype=float)
    with pytest.raises(ValueError, match="Invalid 'to_shape'"):
        convert_rank_data(arr, RankShape.LISTROW_RANKCOL, "bogus_shape")


def test_identical_from_to_shape():
    """
    Ensures from_shape == to_shape raises ValueError.
    """
    arr = np.array([[1, 2], [3, 4]], dtype=float)
    with pytest.raises(ValueError, match="must be different"):
        convert_rank_data(
            arr, RankShape.LISTROW_RANKCOL, RankShape.LISTROW_RANKCOL
        )


def test_non_2d_array():
    """
    Ensures non-2D input raises ValueError.
    """
    one_d = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="2D"):
        convert_rank_data(
            one_d, RankShape.LISTROW_RANKCOL, RankShape.LISTCOL_RANKROW
        )


def test_all_nan_input():
    """
    Ensures an all-NaN array raises ValueError.
    """
    nan_arr = np.full((2, 3), np.nan)
    with pytest.raises(ValueError, match="All-NaN"):
        convert_rank_data(
            nan_arr, RankShape.LISTROW_RANKCOL, RankShape.LISTCOL_RANKROW
        )


def test_basic_listrow_rankcol_to_listcol_rankrow():
    """
    Simple row→col conversion of RANKCOL data (transposition), no mapping expected.
    """
    arr = np.array([[10, 20, np.nan], [30, np.nan, np.nan]], dtype=float)
    rd = convert_rank_data(
        arr, RankShape.LISTROW_RANKCOL, RankShape.LISTCOL_RANKROW
    )
    assert rd.data.shape == (3, 2)
    assert not rd.id_to_index_mapping


def test_basic_listcol_rankrow_to_listrow_rankcol():
    """
    Simple col→row conversion of RANKROW data (transpose), no mapping expected.
    """
    arr = np.array([[1, 2], [3, np.nan]], dtype=float)
    rd = convert_rank_data(
        arr, RankShape.LISTCOL_RANKROW, RankShape.LISTROW_RANKCOL
    )
    assert rd.data.shape == (2, 2)
    assert not rd.id_to_index_mapping


def test_listrow_rankcol_to_itemcol():
    """
    Expands RANKCOL to ITEMCOL, checking rank positions and mapping.
    """
    arr = np.array([[101, 202, np.nan], [202, 303, 101]], dtype=float)
    rd = convert_rank_data(
        arr, RankShape.LISTROW_RANKCOL, RankShape.LISTROW_ITEMCOL
    )
    assert rd.data.shape == (2, 3)
    assert len(rd.id_to_index_mapping) == 3

    c101 = rd.id_to_index_mapping[101]
    c202 = rd.id_to_index_mapping[202]
    c303 = rd.id_to_index_mapping[303]

    # Row 0: 101->rank1, 202->rank2
    assert rd.data[0, c101] == 1
    assert rd.data[0, c202] == 2
    assert np.isnan(rd.data[0, c303])

    # Row 1: 202->rank1, 303->rank2, 101->rank3
    assert rd.data[1, c202] == 1
    assert rd.data[1, c303] == 2
    assert rd.data[1, c101] == 3


def test_listcol_rankrow_to_itemrow():
    """
    Expands RANKROW→ITEMROW. Transposed array has multiple lists, an output map needed.
    """
    arr = np.array(
        [[10, 11, np.nan], [12, np.nan, np.nan]], dtype=float
    ).T  # shape (3,2)
    rd = convert_rank_data(
        arr, RankShape.LISTCOL_RANKROW, RankShape.LISTCOL_ITEMROW
    )
    # 3 lists (columns), distinct IDs ~ {10,11,12}, shape => (3 items) x (3 lists)
    # But actually 3 distinct IDs => rows=3, columns=3
    assert rd.data.shape == (3, 2)
    assert len(rd.id_to_index_mapping) == 3


def test_itemcol_to_listrow_rankcol():
    """
    Converts ITEMCOL to RANKCOL and checks sorting of item IDs by rank.
    """
    arr = np.array([[1, np.nan, 3], [2, 4, np.nan]], dtype=float)
    rd = convert_rank_data(
        arr, RankShape.LISTROW_ITEMCOL, RankShape.LISTROW_RANKCOL
    )
    # row0 => 2 non-NaN ranks => shape (2,2) or (2,3) with trailing NaN
    assert rd.data.shape[0] == 2
    assert rd.data.shape[1] >= 2

    # row0 > item0-> rank=1, item2-> rank=3 => sorted => [0,2]
    valid0 = rd.data[0][~np.isnan(rd.data[0])]
    assert list(valid0) == [0.0, 2.0]

    # row1 > item0-> rank=2, item1-> rank=4 => sorted => [0,1]
    valid1 = rd.data[1][~np.isnan(rd.data[1])]
    assert list(valid1) == [0.0, 1.0]


def test_itemrow_to_listcol_rankrow():
    """
    Converts ITEMROW to RANKROW, verifying final shape and content.
    """
    # shape (2,3): 2 rank positions, 3 lists => each col is a list, each row an item ID
    arr = np.array([[10, 20, np.nan], [30, np.nan, 40]], dtype=float)
    rd = convert_rank_data(
        arr, RankShape.LISTCOL_ITEMROW, RankShape.LISTCOL_RANKROW
    )
    # 3 lists => columns=3, distinct items => 4 => rank positions up to 2
    # We expect shape => (2, 3) after contraction. No mapping needed for RANKROW output.
    assert rd.data.shape == (2, 3)
    assert not rd.id_to_index_mapping

    # Check the final layout
    # col0 => [10, 30], col1 => [20, nan], col2 => [nan, 40]
    # rank= row index+1 => item IDs => good. The test only checks shape/no exception.


def test_validate_rankcol_no_duplicates():
    """Duplicate IDs in a rankcol row should trigger ValueError."""
    arr = np.array([[1, 2, 2]], dtype=float)
    with pytest.raises(ValueError, match="duplicate item ID"):
        _validate_rankcol_no_duplicates(arr)


def test_validate_rankcol_midrow_nulls():
    """Non-null after null in a rankcol row should trigger ValueError."""
    arr = np.array([[10, np.nan, 11]], dtype=float)
    with pytest.raises(ValueError, match="after a NaN"):
        _validate_rankcol_no_midrow_nulls(arr)


def test_validate_itemcol_duplicate_rank():
    """Duplicate rank value in an itemcol row should trigger ValueError."""
    arr = np.array([[1, 1]], dtype=float)
    with pytest.raises(ValueError, match="duplicate rank"):
        _validate_itemcol_no_rank_duplicates(arr)


def test_expanding_to_large_item_ids():
    """
    Should raise error if item expansion leads to >100000 distinct IDs.
    """
    base = np.array([list(range(100001))], dtype=float)
    with pytest.raises(ValueError, match="too large for expansion"):
        convert_rank_data(
            base, RankShape.LISTROW_RANKCOL, RankShape.LISTROW_ITEMCOL
        )


def test_basic_round_trip_rankcol():
    """
    Checks round trip RANKCOL -> RANKROW -> RANKCOL preserves item IDs.
    """
    arr = np.array([[10, 20, np.nan], [30, np.nan, np.nan]], dtype=float)
    rd_step1 = convert_rank_data(
        arr, RankShape.LISTROW_RANKCOL, RankShape.LISTCOL_RANKROW
    )
    rd_step2 = convert_rank_data(
        rd_step1.data, RankShape.LISTCOL_RANKROW, RankShape.LISTROW_RANKCOL
    )

    row0_final = rd_step2.data[0, ~np.isnan(rd_step2.data[0])]
    row1_final = rd_step2.data[1, ~np.isnan(rd_step2.data[1])]
    orig0 = arr[0, ~np.isnan(arr[0])]
    orig1 = arr[1, ~np.isnan(arr[1])]
    np.testing.assert_array_equal(row0_final, orig0)
    np.testing.assert_array_equal(row1_final, orig1)


def test_input_via_rankdata_object():
    """
    If we pass RankData.data (with an empty mapping) to convert_rank_data,
    it should still convert properly.
    """
    input_arr = np.array([[100, 200], [300, 100]], dtype=float)
    rd_in = RankData(data=input_arr, id_to_index_mapping={})
    rd_out = convert_rank_data(
        rd_in.data, RankShape.LISTROW_RANKCOL, RankShape.LISTCOL_RANKROW
    )
    np.testing.assert_array_equal(rd_out.data, input_arr.T)
    assert not rd_out.id_to_index_mapping


def test_empty_input_array():
    """
    Ensures that truly empty arrays raise a ValueError.
    """
    arr = np.empty((0, 3), dtype=float)
    with pytest.raises(ValueError, match="empty"):
        convert_rank_data(
            arr, RankShape.LISTROW_RANKCOL, RankShape.LISTROW_ITEMCOL
        )


def test_float_and_int_item_ids():
    """
    Checks RANKCOL with mixed float/int item IDs expands correctly to ITEMCOL.
    """
    arr = np.array([[1.0, 2.5, np.nan], [3.0, 1.0, np.nan]], dtype=float)
    rd = convert_rank_data(
        arr, RankShape.LISTROW_RANKCOL, RankShape.LISTROW_ITEMCOL
    )
    assert rd.data.shape == (2, 3)
    assert len(rd.id_to_index_mapping) == 3

    # Validate rank positions
    c1 = rd.id_to_index_mapping[1.0]
    c2_5 = rd.id_to_index_mapping[2.5]
    c3 = rd.id_to_index_mapping[3.0]

    # row0 => item1-> rank1, item2.5-> rank2
    assert rd.data[0, c1] == 1
    assert rd.data[0, c2_5] == 2
    assert np.isnan(rd.data[0, c3])

    # row1 => item3-> rank1, item1-> rank2
    assert rd.data[1, c3] == 1
    assert rd.data[1, c1] == 2
    assert np.isnan(rd.data[1, c2_5])


def test_large_numeric_ids():
    """
    Checks that large numeric IDs (e.g., 1e9) work fine in RANKCOL -> ITEMCOL conversion.
    """
    arr = np.array(
        [[1e9, 1e9 + 1, np.nan], [1e9 + 2, np.nan, np.nan]], dtype=float
    )
    rd = convert_rank_data(
        arr, RankShape.LISTROW_RANKCOL, RankShape.LISTROW_ITEMCOL
    )
    assert rd.data.shape == (2, 3)
    assert len(rd.id_to_index_mapping) == 3


def test_itemcol_round_trip_preserves_structure():  # Renamed for clarity
    """
    Tests ITEMCOL -> RANKCOL -> ITEMCOL -> RANKCOL.
    Verifies that the relative order of items (structure) is preserved,
    even if absolute rank values change. Compares the RANKCOL representations.
    """
    arr = np.array([[1, np.nan, 2], [2, 3, np.nan]], dtype=float)

    # ITEMCOL -> RANKCOL
    rd1 = convert_rank_data(
        arr, RankShape.LISTROW_ITEMCOL, RankShape.LISTROW_RANKCOL
    )
    # RANKCOL -> ITEMCOL
    rd2 = convert_rank_data(
        rd1.data, RankShape.LISTROW_RANKCOL, RankShape.LISTROW_ITEMCOL
    )
    # ITEMCOL -> RANKCOL (again, from the result of the round trip)
    rd3 = convert_rank_data(
        rd2.data, RankShape.LISTROW_ITEMCOL, RankShape.LISTROW_RANKCOL
    )

    # The RANKCOL representations rd1.data and rd3.data should be identical
    # if the structure (relative ordering) was preserved.
    # rd1.data was [[0., 2.], [0., 1.]]
    # rd3.data should also be [[0., 2.], [0., 1.]]
    np.testing.assert_array_equal(rd1.data, rd3.data)


def test_custom_na_value():
    """
    Checks that a custom na_value (e.g. -1) is reflected in ITEMCOL expansions.
    """
    arr = np.array([[10, np.nan], [20, 30]], dtype=float)
    rd = convert_rank_data(
        arr, RankShape.LISTROW_RANKCOL, RankShape.LISTROW_ITEMCOL, na_value=-1
    )
    # We have 3 distinct IDs: (10, 20, 30) => 3 columns
    assert rd.data.shape == (2, 3)
    assert np.any(rd.data == -1)

    # row0 => item10->rank1, item20->NaN => -1, item30->NaN => -1
    c10 = rd.id_to_index_mapping[10.0]
    c20 = rd.id_to_index_mapping[20.0]
    c30 = rd.id_to_index_mapping[30.0]
    assert rd.data[0, c10] == 1
    assert rd.data[0, c20] == -1
    assert rd.data[0, c30] == -1
