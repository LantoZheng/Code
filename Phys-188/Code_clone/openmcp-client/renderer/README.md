## dev

如果想要部署到公网中，想要通过密码认证才能进入，进行如下步骤：

```bash
touch .env.website.local
```

写入：

```toml
VITE_USE_AUTH=true
VITE_WEBSOCKET_URL=wss://<IP>/<路径>
```

使用 `npm run serve:website` 进行测试（服务端使用 ts-node src/server.ts）

使用 `npm run build:website` 进行打包