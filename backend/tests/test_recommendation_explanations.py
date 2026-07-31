"""Unit tests for app.recommendation_explanations.build_recommendation_explanation.

These tests exercise the pure explanation-building logic directly with
lightweight in-memory model instances (no database, network, or credentials).
"""

from app import models
from app.recommendation_explanations import (
    RecommendationContext,
    build_recommendation_explanation,
)


def _user(comfort_preference="medium", lifestyle="casual") -> models.User:
    return models.User(comfort_preference=comfort_preference, lifestyle=lifestyle)


def _item(category: str) -> models.ClothingItem:
    return models.ClothingItem(category=category, color="Black")


def _context(**overrides) -> RecommendationContext:
    defaults = dict(
        manual_temp=None,
        time_context=None,
        plan_date=None,
        exclude=None,
        weather_city=None,
        weather_category=None,
        occasion=None,
    )
    defaults.update(overrides)
    return RecommendationContext(**defaults)


def test_no_items_returns_fallback_message():
    result = build_recommendation_explanation(
        user=_user(), items=[], context=_context()
    )
    assert result == "No available items to recommend yet."


def test_base_sentence_lists_lowercased_categories():
    items = [_item("Top"), _item("Bottom"), _item("Shoes")]
    result = build_recommendation_explanation(user=_user(), items=items, context=_context())
    assert "top, bottom, shoes" in result
    assert result.startswith("I picked this outfit to keep your rotation fresh")


def test_time_context_sentence_included_when_present():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context(time_context="Evening")
    )
    assert "tuned for a evening plan." in result


def test_time_context_sentence_omitted_when_absent():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context()
    )
    assert "tuned for" not in result


def test_occasion_sentence_included_when_present():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context(occasion="Formal")
    )
    assert "balanced for a formal occasion." in result


def test_manual_temp_with_weather_city_mentions_city():
    result = build_recommendation_explanation(
        user=_user(),
        items=[_item("Top")],
        context=_context(manual_temp=72, weather_city="Austin"),
    )
    assert "adjusted for around 72F based on current weather in Austin." in result


def test_manual_temp_without_weather_city_omits_city_phrase():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context(manual_temp=50)
    )
    assert "adjusted for around 50F." in result
    assert "based on current weather" not in result


def test_weather_category_used_only_when_manual_temp_missing():
    result = build_recommendation_explanation(
        user=_user(),
        items=[_item("Top")],
        context=_context(weather_category="Rainy"),
    )
    assert "targets rainy weather conditions." in result


def test_weather_category_ignored_when_manual_temp_present():
    result = build_recommendation_explanation(
        user=_user(),
        items=[_item("Top")],
        context=_context(manual_temp=60, weather_category="Rainy"),
    )
    assert "targets rainy weather conditions." not in result
    assert "adjusted for around 60F." in result


def test_plan_date_valid_iso_is_formatted_and_strips_leading_zero():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context(plan_date="2026-01-05")
    )
    assert "work well for January 5." in result


def test_plan_date_without_leading_zero_day_is_unaffected():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context(plan_date="2026-01-15")
    )
    assert "work well for January 15." in result


def test_plan_date_invalid_falls_back_to_raw_text():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context(plan_date="not-a-date")
    )
    assert "work well for not-a-date." in result


def test_plan_date_absent_omits_sentence():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context()
    )
    assert "work well for" not in result


def test_comfort_preference_medium_is_not_mentioned():
    result = build_recommendation_explanation(
        user=_user(comfort_preference="Medium"), items=[_item("Top")], context=_context()
    )
    assert "comfort preference" not in result


def test_comfort_preference_non_medium_is_mentioned():
    result = build_recommendation_explanation(
        user=_user(comfort_preference="Relaxed"), items=[_item("Top")], context=_context()
    )
    assert "leaned toward your relaxed comfort preference." in result


def test_lifestyle_casual_is_not_mentioned():
    result = build_recommendation_explanation(
        user=_user(lifestyle="Casual"), items=[_item("Top")], context=_context()
    )
    assert "styling direction" not in result


def test_lifestyle_non_casual_is_mentioned():
    result = build_recommendation_explanation(
        user=_user(lifestyle="Athletic"), items=[_item("Top")], context=_context()
    )
    assert "matches your athletic routine." in result


def test_exclusions_are_parsed_trimmed_and_joined():
    result = build_recommendation_explanation(
        user=_user(),
        items=[_item("Top")],
        context=_context(exclude=" red , neon , "),
    )
    assert "I avoided red, neon based on your exclusion list." in result


def test_exclusions_blank_string_omits_sentence():
    result = build_recommendation_explanation(
        user=_user(), items=[_item("Top")], context=_context(exclude="   ")
    )
    assert "exclusion list" not in result


def test_all_optional_signals_combine_in_order():
    result = build_recommendation_explanation(
        user=_user(comfort_preference="Cozy", lifestyle="Sporty"),
        items=[_item("Top"), _item("Bottom")],
        context=_context(
            time_context="Morning",
            occasion="Casual Friday",
            manual_temp=65,
            weather_city="Denver",
            plan_date="2026-03-02",
            exclude="wool, leather",
        ),
    )
    expected = (
        "I picked this outfit to keep your rotation fresh, combining top, bottom "
        "pieces you have available now. "
        "It is tuned for a morning plan. "
        "It is also balanced for a casual friday occasion. "
        "The layering balance is adjusted for around 65F based on current weather in Denver. "
        "It should work well for March 2. "
        "I leaned toward your cozy comfort preference. "
        "The styling direction matches your sporty routine. "
        "I avoided wool, leather based on your exclusion list."
    )
    assert result == expected
