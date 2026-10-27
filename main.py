import sys
import asyncio
import json
from pathlib import Path
from spider.core import Spider
from jarvis_bridge import analyze_text

def main():
    print("🕷️ Spider & Jarvis Integration System Ready")
    
    # 1. Get URLs from command line
    urls = sys.argv[1:] if len(sys.argv) > 1 else ["https://example.com"]
    print(f"🚀 Crawling: {urls}")
    
    # 2. Run the Spider
    spider = Spider(urls, max_pages=5)
    results = asyncio.run(spider.crawl())
    
    # 3. Save Raw Data
    out = Path("data")
    out.mkdir(exist_ok=True)
    (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Done: {len(results)} pages saved to data/results.json")
    
    # 4. Trigger Jarvis Analysis
    print("\n🤖 Jarvis: Analyzing results...")
    for i, page in enumerate(results, 1):
        title = page.get('title', 'No Title')
        text = page.get('text', '')
        analysis = analyze_text(text)
        
        if isinstance(analysis, dict):
            print(f"[{i}] {title}")
            print(f"    🔑 Keywords: {', '.join([k for k, v in analysis['keywords']])}")
            print(f"    📊 Complexity: {analysis['complexity']} words/sentence")
            print("-" * 40)

if __name__ == "__main__":
    main()
