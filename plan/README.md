# Weekly one page plan (OnMind)

Template: onmind_plan_template.html (A4, Russian, Onest fonts in fonts/).
Each Monday run: copy the template, replace the week number, dates, numbers, the groups table,
the day plan and the team asks with this week's facts, then render:

    python3 - <<'PY'
    from playwright.sync_api import sync_playwright; import os
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page()
        pg.goto('file://'+os.path.abspath('plan.html'), wait_until='load'); pg.evaluate('document.fonts.ready')
        print(pg.evaluate('document.body.lastElementChild.getBoundingClientRect().bottom'))  # must be under 1123
        pg.pdf(path='OnMind_plan_YYWW.pdf', format='A4', print_background=True, prefer_css_page_size=True); b.close()
    PY

If the bottom value is above 1123 px the page overflows: shorten text, never let it spill to page 2.
Commit the PDF here as plan/OnMind_plan_YYWW.pdf and send it with SendUserFile.
