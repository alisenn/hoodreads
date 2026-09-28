import json
import pytest
from src.book_loader import BookLoader
from src.state_manager import StateManager


def test_state_advancement(tmp_path):
    test_state_file = tmp_path / "test_state.json"
    loader = BookLoader()
    state_mgr = StateManager(state_file=test_state_file, book_loader=loader)

    # Set book
    assert state_mgr.set_active_book("donusum", chapter_num=1)
    task1 = state_mgr.get_next_task()
    assert task1 is not None
    assert task1["book"].id == "donusum"
    assert task1["chapter"].chapter_num == 1

    # Advance
    state_mgr.advance(tweet_id="sim_123")
    task2 = state_mgr.get_next_task()
    assert task2 is not None
    assert task2["chapter"].chapter_num == 2

    # Check history saved
    saved_state = state_mgr.load_state()
    assert len(saved_state["history"]) == 1
    assert saved_state["history"][0]["tweet_id"] == "sim_123"
