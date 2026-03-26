/**
 * RU/EN i18n: embedded dictionary, localStorage, DOM cache for Russian source.
 */
(function () {
    var STORAGE_KEY = 'presentation-lang';

    var STRINGS_EN = {
        page_title: 'Artem — QA Engineer',
        nav_logo: 'Artem QA',
        nav_skills: 'Skills',
        nav_stack: 'Stack',
        nav_exp: 'Experience',
        nav_what: 'What I want',
        nav_why: 'Why me',
        nav_cases: 'Cases',
        nav_final: 'Closing',
        hero_title: 'Artem — QA Engineer',
        hero_p1: 'QA engineer with 4+ years testing web, mobile (iOS/Android), and desktop apps.',
        hero_p2: 'Comfortable being the only tester on a project.',
        hero_p3: 'I build QA from the ground up: test strategy, test plans, metrics, and clear collaboration with the team.',
        hero_p4: 'Beyond manual testing, I write automated tests and wire them into the pipeline for a more stable product.',
        hero_p5: 'Detail-oriented; I work well with engineers and keep communication practical.',
        hero_p6: 'I stay current with tools and methods and keep sharpening skills to ship quality and grow professionally.',
        btn_next: 'Next',
        exp_section_title: 'Experience',
        exp_br_company: 'White rainbow — QA Engineer',
        exp_br_sub: 'Dental clinic network, 6 locations',
        exp_br_content:
            '<p>I work with a medical information system that holds patient data: X-rays, treatment plans, visit history.</p>' +
            '<p>I test the web app for doctor schedules, bookings, visit tracking, reports, and payments.</p>' +
            '<p>I test the patient mobile app: booking, payments, treatment history.</p>' +
            '<p>I fully validated the new clinic website against Figma designs.</p>' +
            '<p>I support end users of the software and collect feedback to improve the product.</p>' +
            '<p>I use Yandex Metrica for usage analytics.</p>' +
            '<p>We work in <span class="highlight-keyword">Agile</span> two-week sprints, collaborating closely for fast feedback.</p>' +
            '<p>Tools: <span class="highlight-keyword">KaiTen</span>, <span class="highlight-keyword">Postman</span> for API, <span class="highlight-keyword">MySQL</span>, <span class="highlight-keyword">Figma</span>, <span class="highlight-keyword">Confluence</span>.</p>' +
            '<p>Functional testing, regression, UI/UX.</p>' +
            '<p>Backend automation on <span class="highlight-keyword">Node.js</span>; UI automation with <span class="highlight-keyword">Python Playwright</span>.</p>' +
            '<p>I create and use checklists, test cases, and documentation.</p>',
        exp_fy_company: 'For You — QA Engineer',
        exp_fy_sub: 'Startup, beauty app (face massage)',
        exp_fy_content:
            '<p><span class="highlight-keyword">Agile/Scrum</span>, two-week sprints.</p>' +
            '<p>Test cases from business requirements; classic test-design techniques.</p>' +
            '<p>Testing on real devices and via Android Studio.</p>' +
            '<p>Frontend and backend: functional, UI/UX, regression, API (<span class="highlight-keyword">Postman</span>), SQL.</p>' +
            '<p>Bug reports in <span class="highlight-keyword">JIRA</span>; regression and release support.</p>' +
            '<p>Retrospectives and continuous improvement with the team.</p>',
        exp_ca_company: 'Conversion Advocates — QA Engineer',
        exp_ca_sub: 'IT company, A/B testing',
        exp_ca_content:
            '<p>Validated site changes before A/B experiments to lift conversion.</p>' +
            '<p>Tools: <span class="highlight-keyword">Figma</span>, <span class="highlight-keyword">BrowserStack</span>, <span class="highlight-keyword">ClickUp</span>.</p>' +
            '<p>Web and mobile layouts across devices and browsers.</p>' +
            '<p>Checklists, test cases, bug reports.</p>' +
            '<p>Close work with PMs, analysts, designers, and developers.</p>',
        what_title: 'What I am looking for',
        what_p1: 'Remote work on a product where I can apply my web and mobile QA experience.',
        what_p2: 'A team that values collaboration, knowledge sharing, and solving hard problems together.',
        what_p3: 'Room to grow test automation and modern tooling, and to help improve QA processes.',
        what_p4: 'I am fine joining teams with gaps in structure, requirements, or process — and helping fix documentation, workflows, and quality.',
        what_p5: 'An environment where I can deliver real user value, gather feedback, and improve the product with data.',
        why_title: 'Why hire me',
        why_p1:
            '<strong>Middle / Senior</strong> level: 4+ years in QA across product companies and startups. I treat testing as a core part of the lifecycle, not a last-minute gate.',
        why_p2:
            'I can <strong>stand up QA from scratch</strong>: strategy and plans, checklists and metrics, consistent bug format and statuses, clear comms with dev and product — so quality is predictable, not luck.',
        why_p3:
            '<strong>Automation with intent</strong>: I prioritize critical paths, cover API on <span class="highlight-keyword">Node.js</span>, UI on <span class="highlight-keyword">Python Playwright</span>, hook runs into <span class="highlight-keyword">CI/CD</span> — regression and smoke signal fast in the pipeline and cut busywork.',
        why_p4:
            'Same stack as below: <span class="highlight-keyword">Node.js</span> for API, <span class="highlight-keyword">Playwright</span> for UI, <span class="highlight-keyword">Postman</span> for contracts, <span class="highlight-keyword">SQL</span> and <span class="highlight-keyword">MySQL</span> for data checks. I deepen <span class="highlight-keyword">TypeScript</span> with tests; <span class="highlight-keyword">Cypress</span> is a comparable swap to Playwright — I can pick it up for your stack.',
        why_p5:
            'Web and mobile, <span class="highlight-keyword">API</span> and databases — from contract alignment to UI and DB regression.',
        why_p6:
            '<span class="highlight-keyword">Agile</span> and <span class="highlight-keyword">Scrum</span>, two-week sprints; I keep test docs current, review automation, and tune the pipeline for stable runs.',
        why_p7:
            'I help teammates adopt QA and automation practices, reduce flakiness and duplication so the team can rely on tests day to day.',
        why_p8:
            'Responsible and detail-focused; I push for quality and advocate for users in discussion with the team.',
        skills_title: 'Skills and tools',
        skills_p1: 'Manual testing: functional, regression, UI/UX',
        skills_p2:
            'Automation: <span class="highlight-keyword">Node.js</span> (API), <span class="highlight-keyword">Python Playwright</span> (UI)',
        skills_p3:
            'Tools: <span class="highlight-keyword">YouTrack</span>, <span class="highlight-keyword">KaiTen</span>, <span class="highlight-keyword">Postman</span>, <span class="highlight-keyword">MySQL</span>, <span class="highlight-keyword">Figma</span>, <span class="highlight-keyword">Confluence</span>',
        skills_p4:
            'Methods: <span class="highlight-keyword">Agile</span>, <span class="highlight-keyword">Scrum</span>, two-week sprints',
        skills_p5: 'Documentation: checklists, test cases, bug reports',
        skills_p6: 'Strong collaboration with developers, analysts, and product.',
        auto_title: 'Automation stack',
        auto_p1:
            'Stack: <span class="highlight-keyword">Node.js</span> for API, <span class="highlight-keyword">Python Playwright</span> for UI, <span class="highlight-keyword">Postman</span> for contracts, <span class="highlight-keyword">SQL</span> and <span class="highlight-keyword">MySQL</span>. Tests run in <span class="highlight-keyword">CI/CD</span> — regression and smoke give fast signal in the pipeline.',
        auto_p2:
            '<span class="highlight-keyword">TypeScript</span> with tests and typing. <span class="highlight-keyword">Cypress</span> sits at the same abstraction as Playwright — I can onboard quickly for your stack.',
        auto_p3:
            '<strong>Debugging:</strong> In Postman I replay requests and compare status codes, headers, and bodies to specs and logs — separating contract bugs from data issues and narrowing root cause.',
        auto_p4:
            '<strong>Debugging:</strong> In the browser I use <span class="highlight-keyword">DevTools</span>: Network for the request chain, Console for front-end errors — before escalating to devs.',
        auto_p5:
            '<strong>Debugging:</strong> I use app logs and targeted SQL to verify data state and catch UI vs server mismatches before filing.',
        auto_p6:
            'At <strong>Middle / Senior</strong> level I shape test architecture and reusable layers; review test code; tune pipelines for stable runs and fewer flakes; and bring colleagues along with solid test docs.',
        cases_title: 'Case studies',
        case1_title: 'Case 1: Building QA from scratch (White rainbow)',
        case1_preview:
            'When I joined White rainbow, testing was not yet a structured process…',
        case1_content:
            '<p>When I joined White rainbow, testing was not yet a structured process. Checks were ad hoc, there was no single source of test documentation, and requirements often arrived verbally or incomplete.</p>' +
            '<p>My job was to build a clear, workable QA process from zero, tuned to how the team and product actually operated.</p>' +
            '<p><strong>First I assessed the situation:</strong></p>' +
            '<ul>' +
            '<li>Learned the product and core user journeys.</li>' +
            '<li>Identified business-critical areas and risk hotspots.</li>' +
            '<li>Set up regular communication with engineering and product.</li>' +
            '</ul>' +
            '<p><strong>Then I rolled it out step by step:</strong></p>' +
            '<ul>' +
            '<li>Documented a test strategy and agreed minimum quality standards with the team.</li>' +
            '<li>Started capturing checklists and cases in Confluence — not perfect, but it gave one place for knowledge and visibility.</li>' +
            '<li>Standardized bug reports: structure, priority, and “ready to fix” criteria.</li>' +
            '<li>Introduced regression before releases.</li>' +
            '<li>Joined requirements discussions early to catch issues before build.</li>' +
            '</ul>' +
            '<p><strong>Tools I relied on:</strong></p>' +
            '<ul>' +
            '<li><strong>Confluence</strong> for test docs, checklists, and process notes.</li>' +
            '<li><strong>Jira / YouTrack</strong> for work items and defects.</li>' +
            '<li><strong>DevTools</strong> for client-side checks and network calls.</li>' +
            '<li><strong>Postman</strong> for API testing.</li>' +
            '<li><strong>SQL</strong> to validate data.</li>' +
            '</ul>' +
            '<p>Over time the process became predictable for everyone. Critical production defects dropped, releases stabilized, and the team shared a clear bar for “done.”</p>' +
            '<p>Testing became part of development — not a final hurdle before release.</p>',
        case2_title: 'Case 2: Fewer defects in scheduling via API tests (White rainbow)',
        case2_preview: 'Incoming bugs showed scheduling issues tied to backend and API…',
        case2_content:
            '<p>Bug analysis showed scheduling problems rooted in backend and API behavior.</p>' +
            '<p>I prioritized critical flows and wrote <span class="highlight-keyword">Node.js</span> API tests covering create/update/delete, conflicts, and validation.</p>' +
            '<p><strong>Outcome:</strong> fewer regression defects, more stable releases, and a scheduling module the business could trust.</p>',
        case3_title: 'Case 3: Faster regression with UI automation (White rainbow)',
        case3_preview: 'I prioritized critical regression paths and shipped UI tests in Python Playwright…',
        case3_content:
            '<p>I prioritized critical regression paths and implemented UI tests with <span class="highlight-keyword">Python Playwright</span>.</p>' +
            '<p>Coverage included login, core business flows, and screen stability.</p>' +
            '<p><strong>Outcome:</strong> shorter regression cycles, faster feedback, lower risk of critical defects.</p>',
        case4_title: 'Case 4: Mobile app localization for the Middle East (For You)',
        case4_preview:
            'For You startup — Arabic market launch: localization, RTL, iOS and Android…',
        case4_content:
            '<p>At For You, a face-massage mobile app on iOS and Android, we expanded into the Arabic market. That meant full Arabic localization and UX tuned to the region.</p>' +
            '<p>Arabic is not just copy: RTL changes layout, navigation, and flows. The main challenge was validating RTL behavior end to end.</p>' +
            '<p>As QA, I owned quality of localization and post-change behavior.</p>' +
            '<p><strong>What I did:</strong></p>' +
            '<ul>' +
            '<li>Verified all user-facing copy, notifications, onboarding, and paywall.</li>' +
            '<li>Found RTL layout issues: misaligned controls, icons, and spacing.</li>' +
            '<li>Checked gestures and navigation with mirrored UI.</li>' +
            '<li>Tested across devices and OS versions on iOS and Android.</li>' +
            '</ul>' +
            '<p><strong>Tooling:</strong></p>' +
            '<ul>' +
            '<li><strong>TestFlight</strong> and <strong>Google Play Console</strong> for builds.</li>' +
            '<li><strong>Android Studio Emulator</strong> and <strong>Xcode Simulator</strong> for screen configs.</li>' +
            '<li><strong>BrowserStack</strong> for real devices.</li>' +
            '<li><strong>Charles Proxy</strong> for localized payloads from the server.</li>' +
            '<li>Localization and cross-platform checklists.</li>' +
            '</ul>' +
            '<p>I logged critical issues: clipped text, bad line breaks, context-mismatched translations, and UI glitches when switching language without restart.</p>' +
            '<p>Defects went to the tracker with clear steps, screenshots, and screen recordings. After fixes I ran regression and confirmed stable Arabic builds on both platforms.</p>' +
            '<p>We launched successfully in Arabic, with reusable checklists for future locales.</p>',
        case5_title: 'Case 5: Ring size bug in a custom jewelry builder (Conversion Advocates)',
        case5_preview:
            'Luxury e-commerce: investigating wrong ring size from a custom product builder…',
        case5_content:
            '<p>At Conversion Advocates, a long-term client — a high-end jewelry e-commerce site — saw more support tickets. Buyers said ring sizes did not match what they picked in the custom builder.</p>' +
            '<p>The site uses a configurator: users pick model, size, metal, stones, and extras, then add to cart.</p>' +
            '<p>My lead asked me to investigate root cause.</p>' +
            '<p><strong>What I did:</strong></p>' +
            '<ul>' +
            '<li>Reviewed tickets and analytics (GA, funnel events, order data).</li>' +
            '<li>Mapped complaints to specific builder combinations.</li>' +
            '<li>Explored the builder manually across parameter sets.</li>' +
            '<li>Used DevTools on “add to cart” requests.</li>' +
            '<li>Checked front-end vs back-end data flow.</li>' +
            '</ul>' +
            '<p>I found that with certain decorative add-ons, after “Add to cart” the selected size silently stepped up by one. It only happened on specific combinations, so it stayed hidden for a long time.</p>' +
            '<p>I filed a detailed bug with steps, expected vs actual, screenshots, and request details, plus a short impact note for dev and business.</p>' +
            '<p><strong>After the fix I:</strong></p>' +
            '<ul>' +
            '<li>Retested all customization paths.</li>' +
            '<li>Confirmed size persisted from builder through checkout.</li>' +
            '<li>Verified the production rollout.</li>' +
            '</ul>' +
            '<p>Support volume for that issue dropped, and stakeholders had a clear explanation and confidence in the flow.</p>',
        final_quote:
            'If you want a solid product and users who enjoy using it — I would love to help you get there.',
        final_btn: 'Thanks for your time — any questions?',
    };

    var cached = false;

    function cacheDomRu() {
        if (cached) return;
        var nodes = document.querySelectorAll('[data-i18n]');
        for (var i = 0; i < nodes.length; i++) {
            var el = nodes[i];
            if (el.hasAttribute('data-i18n-html')) {
                el.setAttribute('data-ru-html', el.innerHTML);
            } else {
                el.setAttribute('data-ru', el.textContent);
            }
        }
        cached = true;
    }

    function applyLanguage(lang) {
        cacheDomRu();
        var isEn = lang === 'en';
        document.documentElement.lang = isEn ? 'en' : 'ru';

        var nodes = document.querySelectorAll('[data-i18n]');
        for (var i = 0; i < nodes.length; i++) {
            var el = nodes[i];
            var key = el.getAttribute('data-i18n');
            if (!key) continue;

            if (isEn) {
                var text = STRINGS_EN[key];
                if (text === undefined) continue;
                if (el.tagName === 'TITLE') {
                    el.textContent = text;
                    document.title = text;
                } else if (el.hasAttribute('data-i18n-html')) {
                    el.innerHTML = text;
                } else {
                    el.textContent = text;
                }
            } else {
                if (el.tagName === 'TITLE') {
                    var ruTitle = el.getAttribute('data-ru');
                    if (ruTitle !== null) {
                        el.textContent = ruTitle;
                        document.title = ruTitle;
                    }
                } else if (el.hasAttribute('data-i18n-html')) {
                    var ruHtml = el.getAttribute('data-ru-html');
                    if (ruHtml !== null) el.innerHTML = ruHtml;
                } else {
                    var ru = el.getAttribute('data-ru');
                    if (ru !== null) el.textContent = ru;
                }
            }
        }

        var toggle = document.getElementById('lang-toggle');
        if (toggle) {
            toggle.textContent = isEn ? 'Rus' : 'Eng';
            toggle.setAttribute('aria-label', isEn ? 'Switch to Russian' : 'Switch to English');
        }

        window.dispatchEvent(new CustomEvent('presentationLangChanged', { detail: { lang: lang } }));
    }

    function getStoredLang() {
        try {
            return localStorage.getItem(STORAGE_KEY) === 'en' ? 'en' : 'ru';
        } catch (e) {
            return 'ru';
        }
    }

    function setStoredLang(lang) {
        try {
            if (lang === 'en') localStorage.setItem(STORAGE_KEY, 'en');
            else localStorage.removeItem(STORAGE_KEY);
        } catch (e) { /* ignore */ }
    }

    function initLangToggle() {
        var btn = document.getElementById('lang-toggle');
        if (!btn) return;
        btn.addEventListener('click', function () {
            var next = getStoredLang() === 'en' ? 'ru' : 'en';
            setStoredLang(next);
            applyLanguage(next);
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        applyLanguage(getStoredLang());
        initLangToggle();
    });

    window.getPresentationLang = getStoredLang;
    window.applyPresentationLanguage = applyLanguage;
})();
