# SMM
## HomeWork1: Crawler
### Installation:
- selenium
- requests
- tqdm
if not install:
```bash
pip install selenium requests tqdm
```
### Package:
- smm: 我們的作業package~
    - `SingleBookProcessor`: 單一書籍爬蟲程式碼
    - `MutiThreadProcessor`: 多線程主程式碼
```python
from law_processer.crawer import MutiThreadProcessor
processor = MutiThreadProcessor("明實錄.json")
processor.muti_thread_crawling()
```
- law_processor: 其他網頁的多線程程式
```python
from law_processer.crawer import MutiThreadLawProcessor
init_url = "https://law.moj.gov.tw/Law/LawSearchJudge.aspx"
processor = MutiThreadLawProcessor(init_url, "司法解釋.json")
processor.muti_thread_crawling()
```
### To Do:
- 4/5 以前完成爬蟲程式並跑完，應該是有標`TODO`的地方
    - `SingleBookProcessor.click_next_page()`
    - `SingleBookProcessor.get_element_content()`
    - `SingleBookProcessor.crawling()`
    - 範例參考 law_processor 應該就沒問題了？
## HomeWork2: Unknown
