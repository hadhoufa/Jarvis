import json
import re
from pathlib import Path
from collections import Counter

STOP_WORDS = {"the", "and", "is", "in", "it", "to", "of", "for", "on", "with", "as", "at", "by", "an", "be", "this", "that", "from", "or", "are", "was", "were", "will", "can"}

def analyze_text(text):
    if not text:
        return "No text available."
    
    # 1. Extract Keywords
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered_words = [w for w in words if w not in STOP_WORDS]
    top_keywords = Counter(filtered_words).most_common(5)
    
    # 2. Summary (First 2 sentences)
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = " ".join(sentences[:2]) if sentences else "No sentences."
    
    # 3. Complexity
    word_count = len(words)
    sentence_count = len(sentences) if sentences else 1
    avg_words_per_sentence = round(word_count / sentence_count, 1)
    
    return {
        "keywords": top_keywords,
        "summary": summary[:200] + "..." if len(summary) > 200 else summary,
        "complexity": avg_words_per_sentence
    }

def analyze_results():
    data_file = Path("data/results.json")
    if not data_file.exists():
        print("[-] No data found. Run the spider first: python main.py <url>")
        return

    try:
        data = json.loads(data_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[-] Error reading file: {e}")
        return

    print("🤖 Jarvis Local Intelligence: Analyzing Spider Data...\n")
    print(f"[+] Found {len(data)} pages.\n")
    
    for i, page in enumerate(data, 1):
        title = page.get('title', 'No Title')
        url = page.get('url', '')
        text = page.get('text', '')
        
        analysis = analyze_text(text)
        
        print(f"[{i}] {title}")
        print(f"    URL: {url}")
        if isinstance(analysis, dict):
            print(f"    🔑 Top Keywords: {', '.join([k for k, v in analysis['keywords']])}")
            print(f"    📝 Summary: {analysis['summary']}")
            print(f"    📊 Complexity: {analysis['complexity']} words/sentence")
        else:
            print(f"    {analysis}")
        print("-" * 60)

if __name__ == "__main__":
    analyze_results()
