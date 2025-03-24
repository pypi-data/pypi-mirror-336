# Webdriver Manager Mirrored for Python

[README_EN](./README_EN.md)

------

这是 webdriver_manager 的一个分支版本, 主要改进是替换了原始仓库中的境外软件源, 使其更适合中国大陆用户使用。

## 主要特点

- 完全兼容原版 webdriver_manager 的所有功能
- 替换了 Chrome、Firefox 等浏览器驱动的下载源为国内镜像
- 无需科学上网即可正常使用
- 支持 Selenium 4.x 及以下版本

## 支持的浏览器驱动

- ChromeDriver
- GeckoDriver (Firefox)
- OperaDriver

## 安装

```bash
pip install webdriver-manager-mirrored
```
 
## 主要改动

相比原版本,本项目主要改动如下:

- 将 ChromeDriver 下载源替换为淘宝镜像
- 将 GeckoDriver 下载源替换为国内镜像
- 其他驱动下载源也尽可能使用国内镜像
- 移除了对 GitHub API 的依赖

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 许可证

本项目采用与原版 webdriver_manager 相同的开源协议。
