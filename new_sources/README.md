# 新发现的 GitHub 订阅源

本次新增验证 21 个订阅地址。按 URL 排除了当前 config.json 中的订阅。

只接受仓库 README 明确发布的 Raw 链接或 GitHub API 返回的规则目录文件；跳过 fork 和归档仓库。下载成功及存在支持规则不等于已经验证无误杀；仓库更新时间不等于规则文件更新时间。

新增候选配置默认禁用，没有改动现有 config.json。没有把整个含例外的过滤列表当作白名单。

| 名称 / 文件 | 订阅 | 仓库证据 | 支持的 DNS 规则 | 放行例外 | 跳过条目 |
| --- | --- | --- | ---: | ---: | ---: |
| [blocklistproject/Lists / abuse-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/abuse-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 435051 | 0 | 68 |
| [blocklistproject/Lists / ads-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ads-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 233991 | 0 | 34 |
| [blocklistproject/Lists / crypto-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/crypto-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 1272 | 0 | 0 |
| [blocklistproject/Lists / fraud-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/fraud-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 256184 | 0 | 84 |
| [blocklistproject/Lists / phishing-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/phishing-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 190191 | 0 | 24 |
| [blocklistproject/Lists / ransomware-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ransomware-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 1904 | 0 | 0 |
| [blocklistproject/Lists / redirect-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/redirect-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 108682 | 0 | 3 |
| [blocklistproject/Lists / scam-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/scam-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 8527 | 0 | 0 |
| [blocklistproject/Lists / smart-tv-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/smart-tv-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 77 | 0 | 0 |
| [blocklistproject/Lists / tracking-ags.txt](https://github.com/blocklistproject/Lists) | [Raw](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/tracking-ags.txt) | [证据](https://api.github.com/repos/blocklistproject/Lists/contents/adguard?ref=main) | 143866 | 0 | 10 |
| [anudeepND/blacklist / adservers.txt](https://github.com/anudeepND/blacklist) | [Raw](https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt) | [证据](https://github.com/anudeepND/blacklist/blob/master/README.md) | 42343 | 0 | 15 |
| [anudeepND/blacklist / facebook.txt](https://github.com/anudeepND/blacklist) | [Raw](https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt) | [证据](https://github.com/anudeepND/blacklist/blob/master/README.md) | 3995 | 0 | 1 |
| [anudeepND/blacklist / CoinMiner.txt](https://github.com/anudeepND/blacklist) | [Raw](https://raw.githubusercontent.com/anudeepND/blacklist/master/CoinMiner.txt) | [证据](https://github.com/anudeepND/blacklist/blob/master/README.md) | 5830 | 0 | 0 |
| [crazy-max/WindowsSpyBlocker / spy.txt](https://github.com/crazy-max/WindowsSpyBlocker) | [Raw](https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt) | [证据](https://api.github.com/repos/crazy-max/WindowsSpyBlocker/contents/data/hosts?ref=master) | 347 | 0 | 0 |
| [jerryn70/GoodbyeAds / GoodbyeAds.txt](https://github.com/jerryn70/GoodbyeAds) | [Raw](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt) | [证据](https://github.com/jerryn70/GoodbyeAds/blob/master/README.md) | 277744 | 0 | 98 |
| [jerryn70/GoodbyeAds / GoodbyeAds-AdBlock-Filter.txt](https://github.com/jerryn70/GoodbyeAds) | [Raw](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-AdBlock-Filter.txt) | [证据](https://github.com/jerryn70/GoodbyeAds/blob/master/README.md) | 277714 | 0 | 117 |
| [jerryn70/GoodbyeAds / GoodbyeAds-Xiaomi-Extension.txt](https://github.com/jerryn70/GoodbyeAds) | [Raw](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Xiaomi-Extension.txt) | [证据](https://github.com/jerryn70/GoodbyeAds/blob/master/README.md) | 278 | 0 | 0 |
| [jerryn70/GoodbyeAds / GoodbyeAds-Samsung-AdBlock.txt](https://github.com/jerryn70/GoodbyeAds) | [Raw](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Samsung-AdBlock.txt) | [证据](https://github.com/jerryn70/GoodbyeAds/blob/master/README.md) | 101 | 0 | 0 |
| [jerryn70/GoodbyeAds / GoodbyeAds-Spotify-AdBlock.txt](https://github.com/jerryn70/GoodbyeAds) | [Raw](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Spotify-AdBlock.txt) | [证据](https://github.com/jerryn70/GoodbyeAds/blob/master/README.md) | 3780 | 0 | 0 |
| [jerryn70/GoodbyeAds / GoodbyeAds-YouTube-AdBlock.txt](https://github.com/jerryn70/GoodbyeAds) | [Raw](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-YouTube-AdBlock.txt) | [证据](https://github.com/jerryn70/GoodbyeAds/blob/master/README.md) | 97645 | 0 | 0 |
| [jerryn70/GoodbyeAds / GoodbyeAds-YouTube-AdBlock-Filter.txt](https://github.com/jerryn70/GoodbyeAds) | [Raw](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-YouTube-AdBlock-Filter.txt) | [证据](https://github.com/jerryn70/GoodbyeAds/blob/master/README.md) | 97645 | 0 | 0 |

## 文件

- [新增订阅地址](subscription_links.txt)
- [候选配置条目](config_candidates.json)
- [核验与跳过记录](audit.json)

不同分类列表可能相互重叠；例如 crypto 主要针对加密挖矿，smart-tv 针对电视设备。使用前按需求选择分类。上游许可及贡献者信息以各仓库说明为准。

## 跳过记录

- [blocklistproject/Lists / malware-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/malware-ags.txt): Source exceeds 32 MiB limit
- [anudeepND/blacklist / blacklist-logo.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/blacklist-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [anudeepND/blacklist / nextdns-logo.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/nextdns-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [anudeepND/blacklist / hblock-logo.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/hblock-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [anudeepND/blacklist / filterlists-logo.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/filterlists-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [anudeepND/blacklist / oisd.nl-logo.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/oisd.nl-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [anudeepND/blacklist / energized-protection-logo.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/energized-protection-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [anudeepND/blacklist / blokada-logo.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/blokada-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [anudeepND/blacklist / paypal.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/paypal.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [anudeepND/blacklist / upi.png](https://raw.githubusercontent.com/anudeepND/blacklist/master/images/upi.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [jerryn70/GoodbyeAds / GoodbyeAds_New_logo_Trans.png](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/GoodbyeAds_New_logo_Trans.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [jerryn70/GoodbyeAds / nextdns-logo.png](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/nextdns-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [jerryn70/GoodbyeAds / ControlD.jpeg](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/ControlD.jpeg): 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
- [jerryn70/GoodbyeAds / AhaDNS.jpeg](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/AhaDNS.jpeg): 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
- [jerryn70/GoodbyeAds / PersonalDNSfilter.jpeg](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/PersonalDNSfilter.jpeg): 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
- [jerryn70/GoodbyeAds / keweon.png](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/keweon.png): 'utf-8' codec can't decode byte 0xf8 in position 16: invalid start byte
- [jerryn70/GoodbyeAds / RethinkDNS.jpeg](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/RethinkDNS.jpeg): 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
- [jerryn70/GoodbyeAds / blokada-logo.png](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/blokada-logo.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
- [jerryn70/GoodbyeAds / Paypal.png](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Images/Paypal.png): 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
