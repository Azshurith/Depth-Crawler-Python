# Depth Crawler (Python)

A simple yet powerful **Python** web crawler that explores a given domain up to a specified depth and outputs a JSON sitemap of URLs and page titles.

## 🚀 Features

- Crawls recursively within a domain up to your chosen depth  
- Records each page’s URL and its HTML `<title>`  
- Outputs results as a JSON file  
- Displays crawl stats: pages visited, links found, total & average time per link

## 🔧 Requirements

- Python 3.x  
- `requests` – for HTTP requests  
- `beautifulsoup4` – for parsing HTML

## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Azshurith/Depth-Crawler-Python.git
cd Depth-Crawler-Python
make install
```

## 🛠 Makefile Commands

The project includes a simple `Makefile` with the following commands:

- **Install dependencies**  
  ```bash
  make install
  ```

- **Run the crawler**  
  ```bash
  make build
  ```

This will execute `python ./src/Main.py`.

## 🎯 Usage

Run the crawler:
```bash
make build
```

- You’ll be prompted to enter the target URL (e.g., `https://example.com`) and crawl depth.
- A file called `sitemap.json` will be generated with the results.

## 📊 Output Format

```json
[
  {
    "url": "https://example.com",
    "title": "Example Domain",
    "links": ["https://example.com/page1", ...]
  },
  ...
]
```

## 📈 Crawl Report

After the run, you'll see a summary showing:

- Total pages visited  
- Total links gathered  
- Max depth reached  
- Total time taken  
- Average time per link

## ✅ How to Contribute

- Fork the repo and submit PRs for improvements  
- Open issues for bugs or feature suggestions

## 📝 License

Add your license info here (e.g., MIT)

## 👤 Author

Your name or GitHub profile link here

---

**Happy crawling!**
