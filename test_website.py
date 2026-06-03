# -*- coding: utf-8 -*-
"""
Автоматизированные проверки сайта-презентации (роль Senior QA).

Запуск:  python test_website.py

Перед первым запуском:
  pip install -r requirements.txt
  playwright install chromium

Проверки (см. docstrings функций и комментарии в коде):
  — битые ссылки (a/area href, img src), в т.ч. якоря на странице;
  — ошибки консоли и сбои загрузки ресурсов;
  — базовая HTML-структура (lang, title, h1);
  — a11y: alt у img, заметка про контраст;
  — адаптив: 3 viewport, горизонтальный скролл, видимость навигации;
  — раскрытие: <details>, аккордеоны опыта и кейсов;
  — переключатель языка #lang-toggle;
  — эвристики UI (размер кликабельных зон).

Выход: report_YYYYMMDD_HHMMSS.xlsx, папка screenshots/
Код выхода 1 при наличии дефектов с приоритетом Critical (для CI).
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urljoin, urlparse

from playwright.sync_api import Page, sync_playwright

import config
from report_generator import DefectRecord, RunSummary, write_excel_report

# ---------------------------------------------------------------------------
# Вспомогательные структуры
# ---------------------------------------------------------------------------


@dataclass
class RunContext:
    """Контекст прогона: счётчики и накопители."""

    base_url: str
    screenshot_dir: Path
    defect_counter: int = 0
    passed_steps: int = 0
    failed_steps: int = 0
    defects: List[DefectRecord] = None
    console_errors: List[str] = None
    request_failures: List[str] = None

    def __post_init__(self) -> None:
        self.defects = []
        self.console_errors = []
        self.request_failures = []


def _next_id(ctx: RunContext) -> str:
    ctx.defect_counter += 1
    return f"D{ctx.defect_counter:03d}"


def _add_defect(
    ctx: RunContext,
    *,
    dtype: str,
    priority: str,
    description: str,
    location: str,
    screenshot_path: str = "",
    recommendation: str = "",
) -> None:
    """Регистрирует дефект и увеличивает счётчик неуспешных шагов."""
    ctx.failed_steps += 1
    ctx.defects.append(
        DefectRecord(
            defect_id=_next_id(ctx),
            defect_type=dtype,
            priority=priority,
            description=description,
            location=location,
            screenshot_path=screenshot_path,
            recommendation=recommendation or "Проверить вручную и исправить по описанию.",
        )
    )


def _pass_step(ctx: RunContext) -> None:
    ctx.passed_steps += 1


def _screenshot(page: Page, ctx: RunContext, name: str) -> str:
    """Сохраняет скриншот, возвращает относительный путь строкой."""
    ctx.screenshot_dir.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)[:120]
    path = ctx.screenshot_dir / f"{safe}.png"
    page.screenshot(path=str(path), full_page=False)
    return str(path.as_posix())


def _ensure_chromium() -> None:
    """
    Пытается установить браузер Chromium для Playwright, если запуск из коробки не удался.
    В CI обычно вызывают `playwright install` заранее; здесь — мягкая попытка.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
    except Exception:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=False,
        )


def _navigate_with_retry(page: Page, url: str) -> None:
    """Загрузка страницы с повторами при сетевых сбоях."""
    last: Optional[Exception] = None
    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=config.NAVIGATION_TIMEOUT_MS,
            )
            page.wait_for_load_state("networkidle", timeout=config.NETWORK_IDLE_TIMEOUT_MS)
            return
        except Exception as e:
            last = e
            time.sleep(config.RETRY_DELAY_SEC * attempt)
    raise last  # type: ignore[misc]


def _is_skipped_scheme(url: str) -> bool:
    u = url.strip().lower()
    return u.startswith("javascript:") or u.startswith("mailto:") or u.startswith("tel:") or u.startswith(
        "data:"
    )


# ---------------------------------------------------------------------------
# Проверки
# ---------------------------------------------------------------------------


def _attach_console_listeners(page: Page, ctx: RunContext) -> None:
    """Собирает сообщения консоли (error) и неуспешные запросы."""

    def on_console(msg) -> None:
        if msg.type == "error":
            text = f"{msg.type}: {msg.text}"
            ctx.console_errors.append(text)

    def on_request_failed(request) -> None:
        ctx.request_failures.append(f"{request.failure} — {request.url}")

    page.on("console", on_console)
    page.on("requestfailed", on_request_failed)


def _paths_equivalent(base: str, target: str) -> bool:
    """Сравнение путей одной страницы (учёт index.html и слэша)."""
    pb, pt = urlparse(base), urlparse(target)
    bpath = pb.path.rstrip("/") or "/"
    tpath = pt.path.rstrip("/") or "/"
    if bpath.endswith("/index.html"):
        bpath = bpath[: -len("index.html")].rstrip("/") or "/"
    if tpath.endswith("/index.html"):
        tpath = tpath[: -len("index.html")].rstrip("/") or "/"
    return (pb.scheme, pb.netloc, bpath) == (pt.scheme, pt.netloc, tpath)


def _check_anchor_exists(page: Page, fragment: str) -> bool:
    fid = fragment.lstrip("#")
    return page.evaluate(
        """(id) => {
        try {
            return !!(document.getElementById(id) || document.querySelector(`[name="${CSS.escape(id)}"]`));
        } catch (e) { return false; }
    }""",
        fid,
    )


def check_links(page: Page, ctx: RunContext) -> None:
    """
    Проверяет href у a/area и src у img: доступность URL, якоря на текущей странице.
    Внешние URL проверяются через page.request (HEAD с fallback на GET).
    """
    base = page.url
    data = page.evaluate(
        """() => {
        const links = [];
        document.querySelectorAll('a[href], area[href]').forEach(el => links.push(el.getAttribute('href')));
        document.querySelectorAll('img[src]').forEach(el => links.push(el.getAttribute('src')));
        return [...new Set(links.filter(Boolean))];
    }"""
    )

    for raw in data:
        raw = (raw or "").strip()
        if _is_skipped_scheme(raw):
            continue
        absolute = urljoin(base, raw)
        if _is_skipped_scheme(absolute):
            continue

        parsed = urlparse(absolute)

        # Только якорь на текущей странице
        if raw.startswith("#") and parsed.fragment:
            ok = _check_anchor_exists(page, "#" + parsed.fragment)
            if ok:
                _pass_step(ctx)
            else:
                p = _screenshot(page, ctx, f"broken-anchor-{parsed.fragment[:20]}")
                _add_defect(
                    ctx,
                    dtype=config.DefectType.BROKEN_LINK,
                    priority=config.Priority.HIGH,
                    description=f"Элемент с id/name для якоря не найден: #{parsed.fragment}",
                    location=absolute,
                    screenshot_path=p,
                    recommendation="Добавить секцию с id или исправить href.",
                )
            continue

        if parsed.fragment and _paths_equivalent(base, absolute):
            ok = _check_anchor_exists(page, "#" + parsed.fragment)
            if ok:
                _pass_step(ctx)
            else:
                p = _screenshot(page, ctx, f"broken-anchor-{parsed.fragment[:20]}")
                _add_defect(
                    ctx,
                    dtype=config.DefectType.BROKEN_LINK,
                    priority=config.Priority.HIGH,
                    description=f"Якорь не найден на странице: #{parsed.fragment}",
                    location=absolute,
                    screenshot_path=p,
                    recommendation="Проверить id секции или href.",
                )
            continue

        try:
            r = page.request.head(absolute, timeout=config.ACTION_TIMEOUT_MS)
            status = r.status
            if status >= 400 or status == 0:
                r = page.request.get(absolute, timeout=config.ACTION_TIMEOUT_MS)
                status = r.status
            if status < 400:
                _pass_step(ctx)
                continue
            is_nav = ".github.io" in absolute and any(
                x in absolute for x in ("#hero", "#skills", "#experience", "#cases", "#final")
            )
            pr = config.Priority.CRITICAL if status >= 500 else config.Priority.HIGH
            if is_nav and "#" in absolute:
                pr = config.Priority.CRITICAL
            p = _screenshot(page, ctx, f"http-{status}-{hashlib.md5(absolute.encode()).hexdigest()[:8]}")
            _add_defect(
                ctx,
                dtype=config.DefectType.BROKEN_LINK,
                priority=pr,
                description=f"HTTP {status} для ресурса",
                location=absolute,
                screenshot_path=p,
                recommendation="Проверить файл на сервере или путь к ресурсу.",
            )
        except Exception as e:
            pr = config.Priority.HIGH
            p = _screenshot(page, ctx, f"link-err-{hashlib.md5(absolute.encode()).hexdigest()[:8]}")
            _add_defect(
                ctx,
                dtype=config.DefectType.BROKEN_LINK,
                priority=pr,
                description=f"Не удалось загрузить: {e}",
                location=absolute,
                screenshot_path=p,
                recommendation="Проверить сеть, CORS, SSL и доступность URL.",
            )


def check_console_and_network(ctx: RunContext) -> None:
    """Переносит накопленные ошибки консоли и сбоев запросов в дефекты."""
    if not ctx.console_errors and not ctx.request_failures:
        _pass_step(ctx)
        return

    for msg in ctx.console_errors:
        is_crit = "SyntaxError" in msg or "ReferenceError" in msg or "TypeError" in msg
        pr = config.Priority.CRITICAL if is_crit else config.Priority.HIGH
        _add_defect(
            ctx,
            dtype=config.DefectType.CONSOLE,
            priority=pr,
            description=msg[:500],
            location=config.BASE_URL,
            recommendation="Исправить JS или подключение скриптов; проверить в DevTools.",
        )

    for msg in ctx.request_failures:
        is_doc = "document" in msg.lower() or ".html" in msg
        pr = config.Priority.CRITICAL if is_doc else config.Priority.HIGH
        _add_defect(
            ctx,
            dtype=config.DefectType.CONSOLE,
            priority=pr,
            description=msg[:500],
            location=config.BASE_URL,
            recommendation="Проверить URL ресурса и сеть (блокировки, 404).",
        )


def check_html_basics(page: Page, ctx: RunContext) -> None:
    """Обязательные теги: html[lang], title, один h1."""
    checks = [
        (
            "lang",
            lambda: page.evaluate(
                """() => {
                const h = document.documentElement.getAttribute('lang');
                return h && h.trim().length > 0;
            }"""
            ),
            "У элемента <html> должен быть непустой атрибут lang.",
        ),
        (
            "title",
            lambda: page.evaluate("() => !!document.querySelector('title') && document.title.trim().length > 0"),
            "Должен быть непустой <title>.",
        ),
        (
            "h1",
            lambda: page.evaluate("() => document.querySelectorAll('h1').length >= 1"),
            "На странице должен быть хотя бы один <h1>.",
        ),
    ]
    for name, fn, rec in checks:
        try:
            ok = bool(fn())
        except Exception:
            ok = False
        if ok:
            _pass_step(ctx)
        else:
            p = _screenshot(page, ctx, f"html-{name}")
            _add_defect(
                ctx,
                dtype=config.DefectType.HTML,
                priority=config.Priority.HIGH,
                description=f"Проверка HTML не пройдена: {name}",
                location=page.url,
                screenshot_path=p,
                recommendation=rec,
            )


def check_a11y_images(page: Page, ctx: RunContext) -> None:
    """Изображения без alt (кроме aria-hidden и декоративных с role=presentation)."""
    bad = page.evaluate(
        """() => {
        let n = 0;
        document.querySelectorAll('img').forEach((img) => {
            if (img.getAttribute('aria-hidden') === 'true') return;
            if (img.getAttribute('role') === 'presentation') return;
            if (img.alt === undefined || img.alt === null) n++;
        });
        return n;
    }"""
    )
    if bad == 0:
        _pass_step(ctx)
    else:
        p = _screenshot(page, ctx, "a11y-img-no-alt")
        _add_defect(
            ctx,
            dtype=config.DefectType.A11Y,
            priority=config.Priority.MEDIUM,
            description=f"Найдено изображений без корректного alt: {bad}",
            location=page.url,
            screenshot_path=p,
            recommendation="Заполнить alt или role=presentation для декоративных изображений.",
        )


def append_contrast_note(notes: List[str]) -> None:
    """
    Не выполняет глубокий анализ контраста; в отчёт на лист «Общая сводка»
    добавляется примечание (не дефект). См. config.A11Y_CONTRAST_NOTE.
    """
    notes.append(config.A11Y_CONTRAST_NOTE)


def check_responsive(page: Page, ctx: RunContext) -> None:
    """Скриншоты и проверка горизонтального скролла и положения навигации."""
    for w, h, label in config.VIEWPORTS:
        page.set_viewport_size({"width": w, "height": h})
        page.wait_for_timeout(400)
        overflow = page.evaluate(
            f"""() => {{
            const d = document.documentElement;
            return d.scrollWidth - d.clientWidth > {config.HORIZONTAL_SCROLL_TOLERANCE_PX};
        }}"""
        )
        if overflow:
            p = _screenshot(page, ctx, f"responsive-overflow-{label}")
            _add_defect(
                ctx,
                dtype=config.DefectType.RESPONSIVE,
                priority=config.Priority.HIGH,
                description=f"Горизонтальный скролл на viewport {label} ({w}×{h})",
                location=page.url,
                screenshot_path=p,
                recommendation="Убрать overflow-x, проверить фиксированные ширины и отступы.",
            )
        else:
            _pass_step(ctx)

        nav_ok = page.evaluate(
            """() => {
            const nav = document.querySelector('.nav-fixed');
            if (!nav) return true;
            const r = nav.getBoundingClientRect();
            return r.width > 0 && r.top >= -2 && r.left >= -2 && r.right <= window.innerWidth + 2;
        }"""
        )
        if not nav_ok:
            p = _screenshot(page, ctx, f"responsive-nav-{label}")
            _add_defect(
                ctx,
                dtype=config.DefectType.RESPONSIVE,
                priority=config.Priority.HIGH,
                description=f"Навигация визуально выходит за пределы экрана ({label})",
                location=page.url,
                screenshot_path=p,
                recommendation="Проверить flex/wrap, padding и position у .nav-fixed / .nav-links.",
            )
        else:
            _pass_step(ctx)

        _screenshot(page, ctx, f"viewport-{label}-{w}x{h}")


def check_details_and_accordions(page: Page, ctx: RunContext) -> None:
    """
    Раскрытие: нативные <details>, заголовки опыта (.experience-header),
    заголовки кейсов (.case-title). Проверяется появление контента / класса active.
    """
    # <details> (если на странице есть нативные раскрывающиеся блоки)
    count = page.locator(config.SELECTOR_DETAILS).count()
    for i in range(count):
        det = page.locator(config.SELECTOR_DETAILS).nth(i)
        det.evaluate("el => { el.open = false; }")
        det.evaluate("el => { el.open = true; }")
        opened = det.evaluate("el => el.open === true")
        if opened:
            _pass_step(ctx)
        else:
            p = _screenshot(page, ctx, f"details-fail-{i}")
            _add_defect(
                ctx,
                dtype=config.DefectType.FUNCTIONAL,
                priority=config.Priority.MEDIUM,
                description=f"Не удалось раскрыть details[{i}]",
                location=page.url,
                screenshot_path=p,
                recommendation="Проверить разметку <details>/<summary>.",
            )

    # Опыт работы (кастомный аккордеон .experience-item)
    n_exp = page.locator(".experience-item").count()
    for i in range(n_exp):
        item = page.locator(".experience-item").nth(i)
        item.locator(".experience-header").click(timeout=config.ACTION_TIMEOUT_MS)
        page.wait_for_timeout(400)
        has_active = item.evaluate("el => el.classList.contains('active')")
        if has_active:
            _pass_step(ctx)
        else:
            p = _screenshot(page, ctx, f"experience-accordion-{i}")
            _add_defect(
                ctx,
                dtype=config.DefectType.FUNCTIONAL,
                priority=config.Priority.HIGH,
                description=f"Аккордеон опыта [{i}] не получил класс active после клика",
                location=page.url,
                screenshot_path=p,
                recommendation="Проверить toggleExperience и CSS .experience-item.active.",
            )

    # Кейсы (.case-item)
    n_case = page.locator(".case-item").count()
    for i in range(n_case):
        item = page.locator(".case-item").nth(i)
        item.locator(".case-title").click(timeout=config.ACTION_TIMEOUT_MS)
        page.wait_for_timeout(400)
        active = item.evaluate("el => el.classList.contains('active')")
        if active:
            _pass_step(ctx)
        else:
            p = _screenshot(page, ctx, f"case-accordion-{i}")
            _add_defect(
                ctx,
                dtype=config.DefectType.FUNCTIONAL,
                priority=config.Priority.MEDIUM,
                description=f"Кейс [{i}] не получил класс active после клика",
                location=page.url,
                screenshot_path=p,
                recommendation="Проверить toggleCase и стили .case-item.active.",
            )


def check_language_toggle(page: Page, ctx: RunContext) -> None:
    """Кнопка #lang-toggle: смена подписи Eng ↔ Rus после первого клика и возврат после второго."""
    btn = page.locator(config.SELECTOR_LANG_TOGGLE)
    if btn.count() == 0:
        _add_defect(
            ctx,
            dtype=config.DefectType.FUNCTIONAL,
            priority=config.Priority.HIGH,
            description="Кнопка переключения языка #lang-toggle не найдена",
            location=page.url,
            recommendation="Добавить кнопку с id=lang-toggle или обновить селектор в config.py.",
        )
        return

    text0 = btn.inner_text().strip()
    btn.click(timeout=config.ACTION_TIMEOUT_MS)
    page.wait_for_timeout(500)
    text1 = btn.inner_text().strip()
    btn.click(timeout=config.ACTION_TIMEOUT_MS)
    page.wait_for_timeout(500)
    text2 = btn.inner_text().strip()

    if text0 == text1:
        p = _screenshot(page, ctx, "lang-toggle-no-change")
        _add_defect(
            ctx,
            dtype=config.DefectType.FUNCTIONAL,
            priority=config.Priority.HIGH,
            description="Текст кнопки языка не изменился после первого клика",
            location=config.SELECTOR_LANG_TOGGLE,
            screenshot_path=p,
            recommendation="Проверить i18n.js и обработчик клика.",
        )
    elif text2 != text0:
        p = _screenshot(page, ctx, "lang-toggle-state")
        _add_defect(
            ctx,
            dtype=config.DefectType.FUNCTIONAL,
            priority=config.Priority.MEDIUM,
            description=f"После двух кликов подпись не вернулась к исходной: было «{text0}», стало «{text2}»",
            location=config.SELECTOR_LANG_TOGGLE,
            screenshot_path=p,
            recommendation="Проверить логику переключения и localStorage.",
        )
    else:
        _pass_step(ctx)


def check_ui_heuristics(page: Page, ctx: RunContext) -> None:
    """Слишком маленькие интерактивные элементы (ниже MIN_CLICKABLE_SIZE_PX). Исключение: #lang-toggle (фиксированная кнопка)."""
    bad = page.evaluate(
        f"""() => {{
        const min = {config.MIN_CLICKABLE_SIZE_PX};
        const bad = [];
        document.querySelectorAll('a, button, input, [role="button"]').forEach(el => {{
            if (el.id === 'lang-toggle' || el.closest('.lang-toggle')) return;
            const r = el.getBoundingClientRect();
            if (r.width <= 0 || r.height <= 0) return;
            if (r.width < min || r.height < min) {{
                bad.push({{ tag: el.tagName, w: Math.round(r.width), h: Math.round(r.height) }});
            }}
        }});
        return bad.slice(0, 15);
    }}"""
    )
    if bad:
        p = _screenshot(page, ctx, "ui-small-targets")
        _add_defect(
            ctx,
            dtype=config.DefectType.UI,
            priority=config.Priority.MEDIUM,
            description=f"Элементы меньше {config.MIN_CLICKABLE_SIZE_PX}px (пример): {bad[:5]}",
            location=page.url,
            screenshot_path=p,
            recommendation=f"Увеличить область касания минимум до {config.MIN_CLICKABLE_SIZE_PX}×{config.MIN_CLICKABLE_SIZE_PX} px (WCAG 2.5.5).",
        )
    else:
        _pass_step(ctx)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def run_audit(
    base_url: str,
    screenshot_dir: Path,
    skip_browser_install: bool,
) -> Tuple[Path, RunContext]:
    """
    Выполняет полный аудит и возвращает путь к отчёту и контекст с дефектами.
    """
    if not skip_browser_install:
        _ensure_chromium()

    ctx = RunContext(base_url=base_url, screenshot_dir=screenshot_dir)
    notes: List[str] = []
    append_contrast_note(notes)
    started = datetime.now()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        page = context.new_page()
        page.set_default_timeout(config.DEFAULT_TIMEOUT_MS)
        _attach_console_listeners(page, ctx)

        _navigate_with_retry(page, base_url)

        check_html_basics(page, ctx)
        check_a11y_images(page, ctx)
        check_links(page, ctx)
        check_responsive(page, ctx)
        # Для аккордеонов и языка — стабильный десктопный viewport
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.wait_for_timeout(300)
        check_details_and_accordions(page, ctx)
        check_language_toggle(page, ctx)
        check_ui_heuristics(page, ctx)
        check_console_and_network(ctx)

        browser.close()

    finished = datetime.now()
    total_checks = ctx.passed_steps + ctx.failed_steps
    critical_list = [d.description for d in ctx.defects if d.priority == config.Priority.CRITICAL]

    summary = RunSummary(
        started_at=started,
        finished_at=finished,
        base_url=base_url,
        total_checks=total_checks,
        passed=ctx.passed_steps,
        failed=ctx.failed_steps,
        critical_issues=critical_list,
        notes=notes,
    )

    report_name = f"report_{finished.strftime('%Y%m%d_%H%M%S')}.xlsx"
    report_path = Path(report_name)
    write_excel_report(report_path, summary, ctx.defects)

    return report_path, ctx


def main() -> int:
    parser = argparse.ArgumentParser(description="Автотесты сайта-презентации (Playwright + Excel).")
    parser.add_argument(
        "--url",
        default=config.BASE_URL,
        help="Базовый URL (по умолчанию из config.BASE_URL)",
    )
    parser.add_argument(
        "--screenshots",
        default="screenshots",
        help="Каталог для скриншотов",
    )
    parser.add_argument(
        "--skip-browser-install",
        action="store_true",
        help="Не пытаться ставить Chromium (для CI, если браузер уже установлен)",
    )
    args = parser.parse_args()

    raw = (args.url or config.BASE_URL).strip()
    if not raw.startswith("http"):
        raw = "https://" + raw
    base_url = raw if raw.endswith("/") else raw + "/"

    report_path, ctx = run_audit(
        base_url=base_url,
        screenshot_dir=Path(args.screenshots),
        skip_browser_install=args.skip_browser_install,
    )

    has_critical = any(d.priority == config.Priority.CRITICAL for d in ctx.defects)
    if has_critical:
        print("\n[CRITICAL] One or more Critical defects. See report:", report_path)

    print(f"\nDone. Report: {report_path.resolve()}")
    print(f"Screenshots: {Path(args.screenshots).resolve()}")
    print(
        f"Defects: {len(ctx.defects)}, passed steps: {ctx.passed_steps}, failed steps: {ctx.failed_steps}"
    )

    return 1 if has_critical else 0


if __name__ == "__main__":
    sys.exit(main())
