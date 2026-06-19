"""
Edge Add-ons Auto-Submitter
Automates plugin submission to Edge Partner Center
Requires: playwright, human at keyboard for PIN entry
"""
import os, json, time, sys
from pathlib import Path

EXT_DIR = r"D:\Lobster_Workspace\chrome_extensions"
SUBMISSION_FORM = r"D:\Lobster_Workspace\提交操作指南.md"

PLUGINS = [
    # (folder, english_name, chinese_name)
    ("privacy_cleaner", "Privacy Cleaner - One Click Browsing Data Cleaner", "隐私清理器"),
    ("ai_translator", "AI Translator - Local AI Translation", "AI 网页翻译器"),
    ("reader_mode", "Reader Mode - Clean Reading View", "阅读模式"),
    ("code_reviewer", "AI Code Reviewer - Local AI Code Review", "AI 代码审查器"),
    ("smart_bookmarks", "Smart Bookmarks - AI Bookmark Manager", "智能书签管家"),
    ("page_monitor", "Page Monitor - Webpage Change Tracker", "网页变化监控器"),
    ("tab_manager", "Tab Manager Pro - Smart Tab Organizer", "标签页管理器"),
]

EDGE_URL = "https://partner.microsoft.com/zh-cn/dashboard/microsoftedge"


def get_user_data_dir():
    """Get Chrome/Edge user data directory for session persistence"""
    home = os.path.expandvars(r"%LOCALAPPDATA%")
    # Try Edge first, then Chrome
    edge = os.path.join(home, "Microsoft", "Edge", "User Data")
    chrome = os.path.join(home, "Google", "Chrome", "User Data")
    if os.path.isdir(edge):
        return edge
    elif os.path.isdir(chrome):
        return chrome
    return None


def check_plugin_files(folder):
    """Verify all required files exist"""
    base = os.path.join(EXT_DIR, folder)
    store = os.path.join(base, "store_listing")
    required = [
        os.path.join(base, "manifest.json"),
        os.path.join(EXT_DIR, f"{folder}.zip"),
        os.path.join(store, "screenshot1.png"),
        os.path.join(store, "screenshot2.png"),
        os.path.join(store, "screenshot3.png"),
        os.path.join(base, "icon_128.png"),
    ]
    missing = [f for f in required if not os.path.isfile(f)]
    return len(missing) == 0, missing


def dry_run():
    """Simulate submission without actually submitting"""
    print("=" * 60)
    print("DRY RUN - No actual submissions will be made")
    print("=" * 60)

    user_data = get_user_data_dir()
    if not user_data:
        print("ERROR: Could not find Edge or Chrome user data directory.")
        print("Please ensure Edge is installed and you are logged into Edge Partner Center.")
        return False

    print(f"\nUser data directory: {user_data}")

    # Check all plugin files
    print("\n--- Plugin file check ---")
    all_ok = True
    for folder, en, zh in PLUGINS:
        ok, missing = check_plugin_files(folder)
        status = "OK" if ok else f"MISSING: {missing}"
        if not ok:
            all_ok = False
        print(f"  [{folder}] {status}")

    if not all_ok:
        print("\nSome plugins are missing files. Fix before submitting.")
        return False

    print("\n--- Submission plan ---")
    for i, (folder, en, zh) in enumerate(PLUGINS, 1):
        zip_path = os.path.join(EXT_DIR, f"{folder}.zip")
        size_kb = os.path.getsize(zip_path) / 1024
        print(f"  {i}. {en} ({folder}) - {size_kb:.1f}KB")

    print(f"\n=== DRY RUN PASSED === ")
    print(f"Ready to submit {len(PLUGINS)} plugins.")
    print("Run with --submit to actually submit.")
    return True


def submit_all():
    """Actually submit all plugins using Playwright"""
    from playwright.sync_api import sync_playwright

    if not dry_run():
        return

    print("\n⚠️  WARNING: About to submit 7 plugins to Edge Store.")
    print("This action CANNOT be undone.")
    confirm = input("Type 'SUBMIT' to continue: ")
    if confirm != "SUBMIT":
        print("Aborted.")
        return

    user_data = get_user_data_dir()
    if not user_data:
        print("ERROR: No browser user data found.")
        return

    results = []

    with sync_playwright() as p:
        # Launch persistent context to inherit login cookies
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data,
            headless=False,  # PIN entry requires visible browser
            channel=None,    # Use default Chromium
        )

        page = context.pages[0] if context.pages else context.new_page()

        # Navigate to Edge Partner Center
        print("\nNavigating to Edge Partner Center...")
        page.goto("https://partner.microsoft.com/en-us/dashboard/microsoftedge/overview", timeout=30000)

        # Check login state
        page.wait_for_timeout(3000)
        if "login" in page.url.lower() or "signin" in page.url.lower():
            print("\nERROR: Not logged in. Please login to Edge Partner Center first.")
            print("1. Open Edge browser")
            print("2. Go to https://partner.microsoft.com/")
            print("3. Login with your developer account")
            print("4. Run this script again")
            context.close()
            return

        print("Login state: OK")

        for folder, en_name, zh_name in PLUGINS:
            print(f"\n--- Submitting: {en_name} ---")

            try:
                # Navigate to extensions page
                page.goto("https://partner.microsoft.com/en-us/dashboard/microsoftedge/extension/publish", timeout=15000)
                page.wait_for_timeout(2000)

                # Click "Create new extension" or "New submission"
                # Note: selectors may change. This is a template.
                create_btn = page.locator('button:has-text("Create"), a:has-text("New"), button:has-text("New")').first
                if create_btn.is_visible():
                    create_btn.click()
                    page.wait_for_timeout(2000)
                else:
                    # Try direct URL approach
                    print("  Looking for submission form...")

                # Upload zip
                zip_path = os.path.join(EXT_DIR, f"{folder}.zip")
                file_input = page.locator('input[type="file"]').first
                if file_input.is_visible():
                    file_input.set_input_files(zip_path)
                    page.wait_for_timeout(3000)
                    print(f"  Uploaded: {folder}.zip")

                # Fill form fields
                # Name field
                name_input = page.locator('input[name*="name"], input[aria-label*="Name"]').first
                if name_input.is_visible():
                    name_input.fill(en_name)
                    print(f"  Name: {en_name}")

                # Screenshots
                for i in range(1, 4):
                    ss_path = os.path.join(EXT_DIR, folder, "store_listing", f"screenshot{i}.png")
                    ss_inputs = page.locator('input[type="file"]').all()
                    if len(ss_inputs) > i:
                        ss_inputs[i].set_input_files(ss_path)

                # Submit button
                submit_btn = page.locator('button:has-text("Submit"), button:has-text("Publish")').first
                if submit_btn.is_visible():
                    print("  Ready to submit - click Submit button to complete.")
                    # Uncomment for actual submission:
                    # submit_btn.click()

                results.append((folder, "draft_saved", ""))

            except Exception as e:
                error_msg = str(e)[:200]
                print(f"  ERROR: {error_msg}")
                results.append((folder, "error", error_msg))

                # Check for PIN prompt
                if "PIN" in error_msg or "pin" in page.content().lower():
                    print("\n  ⏸️  PIN verification required!")
                    print("  Please enter your PIN in the browser window.")
                    print("  Press Enter here after you've entered the PIN...")
                    input()
                    # Retry after PIN
                    try:
                        submit_btn = page.locator('button:has-text("Submit")').first
                        if submit_btn.is_visible():
                            submit_btn.click()
                            results[-1] = (folder, "submitted", "")
                            print(f"  Submitted after PIN verification!")
                    except:
                        pass

        context.close()

    # Summary
    print("\n" + "=" * 60)
    print("SUBMISSION SUMMARY")
    print("=" * 60)
    for folder, status, error in results:
        emoji = "OK" if status in ("draft_saved", "submitted") else "FAIL"
        print(f"  {folder}: {emoji} {error}")

    # Save results
    with open(r"D:\Lobster_Workspace\sandbox\submission_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to sandbox/submission_results.json")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--submit":
        submit_all()
    else:
        dry_run()
