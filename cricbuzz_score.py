from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launch Chrome using installed browser executable to bypass anti-bot blocks
    browser = p.chromium.launch(
        channel="chrome",
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 768}
    )

    page = context.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    print("Navigating to Cricbuzz...")
    page.goto("https://www.cricbuzz.com/", wait_until="domcontentloaded")

    # Generic selectors to locate active match cards or header score elements
    selectors = [
        ".cb-mat-mnu",
        ".cb-hm-scg-blk",
        ".cb-mtch-crd-hdr",
        "header",
        "nav"
    ]

    score_found = False

    for selector in selectors:
        try:
            # Short wait for any visible score container
            page.wait_for_selector(selector, timeout=3000)
            element = page.query_selector(selector)
            
            if element:
                text = element.inner_text().strip()
                if text:
                    # Format output into clean lines
                    clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
                    formatted_score = "\n".join(clean_lines[:6])
                    
                    print("\n--- Live Cricket Scorecard ---")
                    print(formatted_score)
                    print("------------------------------\n")
                    score_found = True
                    break
        except Exception:
            continue

    if not score_found:
        print("No live match card located, extracted page title:")
        print(page.title())

    # Save screenshot required by assignment
    page.screenshot(path="score.png")
    print("saved score.png")

    browser.close()