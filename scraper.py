import datetime
import nltk
from newspaper import Article, build, hot
import os

nltk.download('punkt')
nltk.download('punkt_tab')

def get_news_articles(company):
    """Builds a source for a given company on MarketWatch and returns article objects."""
    print(f"Building source for {company} on MarketWatch...")
    source = build(f"https://www.marketwatch.com/investing/stock/{company.lower()}", memoize_articles=False)
    return source.articles

def summarize_article(article):
    """Summarizes a single news article."""
    try:
        article.download()
        article.parse()
        article.nlp()
        return article.summary
    except Exception as e:
        return f"Could not summarize article: {e}"

def run_news_scraping(companies):
    """Scrapes, summarizes, and returns news for a given list of companies."""
    today = datetime.date.today().strftime("%m%d%Y")
    output_filename = os.path.join("files", f"NewsSummary_{today}.txt")

    all_news_summary = []

    news_sources = ['cnbc.com', 'reuters.com', 'bloomberg.com', 'wsj.com']
    hot_articles = []
    for source in news_sources:
        print(f"Getting hot articles from {source}...")
        paper = build(f'http://{source}', memoize_articles=False)
        hot_articles.extend(paper.articles)

    for company in companies:
        print(f"Searching for financial news on {company}...")
        company_articles = []
        for article in hot_articles:
            if (company.lower() in article.url.lower()) or (article.title and company.lower() in article.title.lower()):
                company_articles.append(article)

        if company_articles:
            print(f"Found {len(company_articles)} potential articles for {company}. Summarizing top 3...")
            for i, article in enumerate(company_articles[:3]):
                print(f"Summarizing article {i+1}: {article.url}")
                summary = summarize_article(article)
                all_news_summary.append(f"--- Summary for article {i+1} about {company} ---\n{summary}\n")
        else:
            all_news_summary.append(f"--- News for {company} ---\nNo financial news found.\n")

    return all_news_summary, output_filename

if __name__ == "__main__":
    default_companies = ["AMZN", "GOOGL", "AAPL", "NVDA", "INTC"]
    news_summary_content, filename = run_news_scraping(default_companies)
    with open(filename, "w", encoding='utf-8') as f:
        f.write("\n".join(news_summary_content))
    print(f"News summary saved to {filename}")
