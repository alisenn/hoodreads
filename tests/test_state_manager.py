import pytest
from src.book_loader import BookLoader
from src.state_manager import StateManager


def test_state_advancement_and_previous(tmp_path):
    test_state_file = tmp_path / "test_state.json"
    loader = BookLoader()
    state_mgr = StateManager(state_file=test_state_file, book_loader=loader)

    # Set book
    assert state_mgr.set_active_book("donusum", chapter_num=1)
    curr1 = state_mgr.get_current()
    assert curr1 is not None
    assert curr1["book"].id == "donusum"
    assert curr1["chapter"].chapter_num == 1

    # Advance
    state_mgr.advance()
    curr2 = state_mgr.get_current()
    assert curr2 is not None
    assert curr2["chapter"].chapter_num == 2

    # Previous
    state_mgr.previous()
    curr_prev = state_mgr.get_current()
    assert curr_prev is not None
    assert curr_prev["chapter"].chapter_num == 1
