# ITHome RSS Scraper

这是一个使用 Python 编写的命令行工具，用于抓取 [IT之家 (ITHome)](https://www.ithome.com) 的 RSS 订阅内容。它可以根据指定的时间范围过滤新闻，并将结果输出为易于人类阅读或供大语言模型（LLM）进一步总结的纯文本格式。

## 功能特性

*   **实时抓取**：直接解析 IT 之家的 RSS feed。
*   **灵活时间过滤**：支持任意时间范围，如分钟数（30m、40m、60m）、小时数（1h、1.5h、2h）、自然日（1d、yesterday）。
*   **清晰排版**：输出格式包含新闻的时间、标题、链接和摘要，结构清晰，方便复制用于 AI 总结。

## 环境依赖

本项目使用 [uv](https://github.com/astral-sh/uv) 进行 Python 环境和依赖管理。主要依赖如下：

*   `feedparser` (解析 RSS 订阅)
*   `requests`

在使用前，请确保你已经安装了 `uv`。如果没有安装，可以参考官方文档或者运行（Windows PowerShell）：

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

或者在 macOS / Linux 下运行：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 使用方法

克隆或下载本项目后，进入项目根目录：

```bash
cd ithome
```

使用 `uv run` 命令直接运行主程序，并通过 `--time` 参数指定需要抓取的时间范围。由于 `uv` 会自动处理虚拟环境和依赖的安装，你不需要手动执行 `pip install`。

### 参数说明

`--time` 参数支持以下灵活格式：

#### 分钟格式（Xm）
指定过去 X 分钟内的新闻，支持任意正整数。
*   `5m`：过去 5 分钟
*   `30m`：过去 30 分钟
*   `40m`：过去 40 分钟
*   `120m`：过去 120 分钟（2小时）

#### 小时格式（Xh）
指定过去 X 小时内的新闻，支持整数和小数。
*   `1h`：过去 1 小时
*   `2h`：过去 2 小时
*   `1.5h`：过去 1.5 小时（90分钟）
*   `0.5h`：过去 0.5 小时（30分钟）

#### 自然日格式
*   `1d`：抓取 **今天（当前自然日）** 从 00:00:00 到 23:59:59 发布的所有新闻。
*   `yesterday`：抓取 **昨天（前一个自然日）** 从 00:00:00 到 23:59:59 发布的所有新闻。

### 运行示例

#### 分钟格式示例

**获取过去 30 分钟的新闻**
```bash
uv run main.py --time 30m
```

**获取过去 40 分钟的新闻**
```bash
uv run main.py --time 40m
```

#### 小时格式示例

**获取过去 1 小时的新闻**
```bash
uv run main.py --time 1h
```

**获取过去 1.5 小时（90分钟）的新闻**
```bash
uv run main.py --time 1.5h
```

**获取过去 2 小时的新闻**
```bash
uv run main.py --time 2h
```

#### 自然日示例

**获取今天一整天的新闻**
```bash
uv run main.py --time 1d
```

**获取前一天全部的新闻**
```bash
uv run main.py --time yesterday
```

## 输出示例

```text
Scraping ITHome news for parameter: '30m'
[2026-03-18 11:22:02] 日本乐天 AI 模型被指“套壳”DeepSeek V3
Link: https://www.ithome.com/0/930/150.htm
Summary: 3 月 18 日消息，日本乐天集团近期推出的一款AI模型......
------------------------------------------------------------
...
...
Total: 4 news items found.
```
