# OriDNS

自用 DNS 记录管理工具，目前仅支持 DNSPod 和 Cloudflare。

## 用法

> 前端需要自行打包部署到任意 Web 服务器上，服务端地址配置在 `src/config/index.ts` 文件中

1. 按照 `config.example.json` 格式填写配置并保存为 `config.json` 文件

2. 填写 `docker-compose.yml` 文件内的环境变量等配置，使用 `docker compose up -d` 启动
