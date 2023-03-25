# tcaptcha_tool

* 该库仅能完成tcaptcha的***体验模式***和***可疑模式***的缺口识别及滑动
* 核心的缺口识别使用图鉴完成
* 依托于selenium框架完成
* 因背景和缺口图基于浏览器请求来获取url，故使用该库的爬虫必须使用selenium-wire来创建浏览器实例，如有相关修改方案请提出 issus


---

### create env

```shell
pip install -r requirements.txt
```

* selenium: 框架
* webdriver_manager: 浏览器驱动包集中管理
* selenium-wire: 请求拦截