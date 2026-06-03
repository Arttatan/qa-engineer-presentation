# -*- coding: utf-8 -*-
"""
Конфигурация автотестов сайта-презентации.

Здесь задаются базовый URL, таймауты, размеры viewport,
пороги для UI-эвристик и правила приоритетов дефектов.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

# --- Основной URL (production GitHub Pages) ---
BASE_URL: str = "https://arttatan.github.io/qa-engineer-presentation/"

# --- Таймауты (мс) ---
NAVIGATION_TIMEOUT_MS: int = 60_000
DEFAULT_TIMEOUT_MS: int = 30_000
ACTION_TIMEOUT_MS: int = 15_000
NETWORK_IDLE_TIMEOUT_MS: int = 15_000

# --- Повторы при нестабильности сети / загрузки ---
MAX_RETRIES: int = 3
RETRY_DELAY_SEC: float = 1.5

# --- Viewport для скриншотов адаптивности (width, height, label) ---
VIEWPORTS: List[Tuple[int, int, str]] = [
    (1920, 1080, "desktop"),
    (768, 1024, "tablet"),
    (375, 667, "mobile"),
]

# --- Горизонтальный скролл: допустимый зазор (px) из-за скроллбара ---
HORIZONTAL_SCROLL_TOLERANCE_PX: int = 2

# --- WCAG 2.5.5 / практика: минимальный размер цели касания (px) ---
MIN_CLICKABLE_SIZE_PX: int = 44

# --- Селекторы, специфичные для этого сайта ---
SELECTOR_LANG_TOGGLE: str = "#lang-toggle"
SELECTOR_NAV: str = ".nav-fixed"
SELECTOR_NAV_LINKS: str = ".nav-links"
SELECTOR_EXPERIENCE_HEADERS: str = ".experience-header"
SELECTOR_CASE_TITLES: str = ".case-title"
SELECTOR_DETAILS: str = "details"

# --- Комментарий для отчёта: автоматическая проверка контраста ограничена ---
A11Y_CONTRAST_NOTE: str = (
    "Полная проверка контраста текста и фона требует ручного аудита или axe-core / "
    "специализированных инструментов; в автотесте зафиксировано только базовое напоминание."
)

# --- Типы дефектов (для колонки «Тип») ---
class DefectType:
    BROKEN_LINK = "битая ссылка"
    CONSOLE = "консольная ошибка"
    A11Y = "a11y"
    RESPONSIVE = "адаптив"
    UI = "UI/UX"
    HTML = "HTML"
    FUNCTIONAL = "функционал"
    OTHER = "другое"


class Priority:
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class PriorityRule:
    """Правило: ключевое слово в описании или тип -> приоритет по умолчанию."""

    defect_type: str
    default_priority: str
    keywords_critical: Tuple[str, ...] = field(default_factory=tuple)


# Эвристика приоритета (дополняется логикой в test_website.py)
PRIORITY_RULES: List[PriorityRule] = [
    PriorityRule(DefectType.BROKEN_LINK, Priority.HIGH, ("nav", "#hero", "критич")),
    PriorityRule(DefectType.CONSOLE, Priority.HIGH, ()),
    PriorityRule(DefectType.HTML, Priority.HIGH, ("lang", "title", "h1")),
    PriorityRule(DefectType.A11Y, Priority.MEDIUM, ()),
    PriorityRule(DefectType.RESPONSIVE, Priority.HIGH, ("скролл", "scroll")),
    PriorityRule(DefectType.UI, Priority.MEDIUM, ()),
    PriorityRule(DefectType.FUNCTIONAL, Priority.HIGH, ()),
]
