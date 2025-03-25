# 人工智能测试与评估

AITE 是一个面向人工智能算法、模型、软件进行测试与评估的基础库。

# 目录
- [简介](#简介)
- [安装](#安装)

# 简介
人工智能算法、模型、软件测试与评估主要包括：
- 功能验证
- 性能测试
- 可靠性评估
- 安全性评估
- 可解释性分析
- 数据质量度量

# 部署

1. docker-compose部署
2. 本地部署

## 1. docker部署

### 1. 下载pip依赖

```
mkdir pkgs
pip download -r requirements.txt -d ./pkgs
```

### 2. 构建镜像

```
docker-compose build
```

### 3. 启动容器

```
docker-compose up -d
```

默认是80端口


