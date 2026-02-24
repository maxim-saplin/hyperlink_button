from __future__ import annotations

import hyperlink_button._component as component


def test_click_id_empty_is_not_clicked(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    def fake_component(**kwargs):
        return {"click_id": ""}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    assert component.hyperlink_button("Label", key="k") is False


def test_click_id_missing_is_not_clicked(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    def fake_component(**kwargs):
        return {}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    assert component.hyperlink_button("Label", key="k") is False


def test_click_id_none_is_not_clicked(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    def fake_component(**kwargs):
        return {"click_id": None}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    assert component.hyperlink_button("Label", key="k") is False


def test_click_id_same_value_is_only_clicked_once(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    def fake_component(**kwargs):
        return {"click_id": "same"}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    assert component.hyperlink_button("Label", key="k") is True
    assert component.hyperlink_button("Label", key="k") is False


def test_click_id_new_value_is_clicked_each_time(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    calls = {"count": 0}

    def fake_component(**kwargs):
        calls["count"] += 1
        if calls["count"] == 1:
            return {"click_id": "first"}
        return {"click_id": "second"}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    assert component.hyperlink_button("Label", key="k") is True
    assert component.hyperlink_button("Label", key="k") is True


def test_on_click_runs_only_on_new_click_id(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    def fake_component(**kwargs):
        return {"click_id": "same"}

    called = {"n": 0}

    def on_click():
        called["n"] += 1

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    assert component.hyperlink_button("Label", key="k", on_click=on_click) is True
    assert called["n"] == 1

    assert component.hyperlink_button("Label", key="k", on_click=on_click) is False
    assert called["n"] == 1


def test_component_called_with_default_click_id_dict(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    seen: dict[str, object] = {}

    def fake_component(**kwargs):
        seen.update(kwargs)
        return {"click_id": ""}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    component.hyperlink_button("Label", key="k")

    assert seen.get("default") == {"click_id": ""}


def test_invalid_type_raises(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    def fake_component(**kwargs):
        return {"click_id": ""}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    try:
        component.hyperlink_button("Label", key="k", type="nope")
        raise AssertionError("Expected StreamlitAPIException")
    except Exception as e:
        assert "Invalid `type`" in str(e)


def test_invalid_icon_position_raises(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    def fake_component(**kwargs):
        return {"click_id": ""}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    try:
        component.hyperlink_button("Label", key="k", icon_position="nope")
        raise AssertionError("Expected StreamlitAPIException")
    except Exception as e:
        assert "Invalid `icon_position`" in str(e)


def test_invalid_width_raises(monkeypatch):
    monkeypatch.setattr(component.st, "session_state", {})

    def fake_component(**kwargs):
        return {"click_id": ""}

    monkeypatch.setattr(component, "_hyperlink_button_component", fake_component)

    try:
        component.hyperlink_button("Label", key="k", width=object())
        raise AssertionError("Expected StreamlitAPIException")
    except Exception as e:
        assert "Invalid `width`" in str(e)
