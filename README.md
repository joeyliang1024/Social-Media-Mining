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
- smm: 我們的作業package
    - `SingleBookProcessor`: 單一書籍爬蟲程式碼
    - `MutiThreadProcessor`: 多線程主程式碼
```python
from law_processer.crawer import MutiThreadProcessor
processor = MutiThreadProcessor("明實錄.json")
processor.muti_thread_crawling()
```
### To Do:
- 4/5 以前完成爬蟲程式並跑完，應該是有標`TODO`的地方 (Done)
## HomeWork2: Unknown
