# MessageReflector

## 概述
`MessageReflector` 是一个用于处理消息反射组件。它允许应用程序将服务端的消息发送给客户端，再有客户端原样返回，以避免服务端直接处理消息时卡主UI。

## 功能
- **消息处理**: 将服务端的消息发送给客户端，再有客户端原样返回

## 发布
1. 进入frontent执行npm run build
2. 进入setup.py目录执行 python setup.py sdist bdist_wheel
3. 执行运行 Upload PiPy Task

## 安装
使用 npm 或 yarn 安装组件：
```bash
npm install message_reflector
# 或者
yarn add message_reflector
```

## 使用示例
if message:= message_reflector(st.session_state["message"], delay_ms=10000):
    st.write(f"Received message: {message}")
else:
    st.write("No message")  


## 贡献
欢迎任何形式的贡献！请查看 [贡献指南](CONTRIBUTING.md) 以获取更多信息。

## 许可证
该项目遵循 MIT 许可证。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。