# 仓库文件结构与维护约定

## 目录总览

```text
RoutoWrt/
├── AGENTS.md                          # 仓库协作、提交、同步及增量构建约定
├── README.md                          # 项目概览、当前进度和常用入口
├── .gitattributes                     # 文本文件 LF 换行规则
├── .gitignore                         # 凭证、产物、缓存和本地记录排除规则
├── contracts/
│   ├── v1.md                          # 配置模型与 RPC 契约
│   └── fixtures/                      # 合成配置、订阅输入样本
├── firmware/
│   ├── README.md                      # 固定构建输入、集成步骤和限制
│   ├── openwrt/
│   │   ├── evaluation.config          # OpenWrt 配置 seed
│   │   ├── 99-routowrt-management   # 基础管理入口首启脚本
│   │   ├── patches/                   # 针对固定上游版本的补丁
│   │   ├── routowrt-core/           # 外部 sing-box 核心的打包配方
│   │   ├── routowrt-manager/        # ucode 管理后端、RPC、ACL 与服务脚本
│   │   ├── routowrt-forwarding/     # LAN 透明转发适配器及打包配方
│   │   └── luci-app-routowrt/        # LuCI 页面、公共模块、样式与菜单
│   └── tools/                         # 在构建主机 使用的构建监督及镜像检查工具
├── scripts/
│   └── sync-rock.sh                   # 通用源码同步入口，默认 dry-run
├── tests/
│   ├── README.md                      # 测试入口、环境和覆盖范围
│   ├── manager/                       # 模型、订阅、事务、下载及超时检查
│   ├── integration/                   # 接口边界、转发、首启与运行时检查
│   └── ui/                            # Node 测试与离线页面预览
└── docs/
    ├── README.md                      # 完整文档导航及阅读顺序
    ├── repository-structure.md         # 本文件：目录职责与维护约定
    ├── requirements.md                # 持续维护的需求与验收标准
    ├── implementation-plan.md         # 当前实施方案
    ├── development-workflow.md        # 电脑源码与 构建主机 构建工作流
    ├── devices/                       # 持续维护的设备与网络记录
    ├── proposals/                     # 可行性分析、候选方案与历史提案
    └── reports/                       # 按日期归档的执行、构建和验证报告
```

此树展示主要目录和入口，没有展开全部包内文件。`.git/` 是 Git 元数据，不属于项目源码。

## 源码与工具职责

| 位置 | 保存内容 | 维护时同时关注 |
| --- | --- | --- |
| `contracts/v1.md`、`contracts/fixtures/` | 管理模型、接口约定及合成样本 | 前后端实现、权限和对应测试 |
| `firmware/openwrt/routowrt-core/Makefile` | 外部核心 ELF、来源信息与许可证的安装配方 | 外部输入哈希及增量构建依赖 |
| `firmware/openwrt/routowrt-manager/files/usr/share/ucode/routowrt/` | `model.uc`、`subscription.uc`、`store.uc`：模型生成、订阅解析与配置事务 | `contracts/`、`tests/manager/` |
| `firmware/openwrt/routowrt-manager/files/usr/share/rpcd/` | RPC 实现和 `acl.d/` 权限 | 前端 `api.js` 与接口边界检查 |
| `firmware/openwrt/routowrt-manager/files/usr/libexec/`、`files/etc/` | 后台作业、下载、启动恢复、定时更新及 init 集成 | 事务、下载许可、超时和重启恢复验证 |
| `firmware/openwrt/routowrt-forwarding/files/` | nftables／策略路由适配脚本 | 隔离转发测试和实机网络验证 |
| `firmware/openwrt/luci-app-routowrt/htdocs/luci-static/resources/` | `view/routowrt/app.js` 页面及 `routowrt/` 下 API、模型和样式 | 契约、Node 检查及浏览器预览 |
| `firmware/openwrt/luci-app-routowrt/root/` | LuCI 菜单等安装文件 | rpcd ACL 与页面入口绑定 |
| `firmware/tools/` | `run-native-build.py` 构建监督、`inspect-image.py` 镜像检查 | 固定 构建主机 路径、版本、哈希及检查配置 |
| `scripts/` | 跨组件开发工作流，目前为 `sync-rock.sh` | 同步白名单、排除项和目标路径 |

包内的 `files/`、`root/` 和 `htdocs/` 沿用对应安装布局；最终设备路径和权限以各包 `Makefile` 为准。后端细节见[管理包说明](../firmware/openwrt/routowrt-manager/README.md)，构建集成见[固件说明](../firmware/README.md)。

## 本地环境资料

实际环境资料保存在被 Git 忽略的 `.local/lab/`，不属于项目默认配置。

## 新文件放置与变更规则

1. 新功能代码放入对应 OpenWrt 包；新增独立包时在 `firmware/openwrt/` 下按包名建目录，并同步维护构建说明及配置 seed。
2. 接口或配置语义写入 `contracts/`；可共享样本放入 `contracts/fixtures/`，使用合成域名和身份值，不保存真实订阅或节点凭证。
3. 测试按 `manager/`、`integration/`、`ui/` 归属存放；测试桩与预览模拟器保留在 `tests/`，不混入生产包。
4. 与固件构建、镜像检查直接相关的工具放入 `firmware/tools/`；跨组件工作流脚本放入 `scripts/`；一次性本机诊断文件放入 `.local/`，复用前再审查归档。
5. 文档按[文档导航中的维护规则](README.md#维护规则)归档；根目录保留项目入口和仓库级规则。
6. 改名或移动前检查全部引用，特别是测试中的仓库相对路径、包安装路径和文档链接。源码同步不使用 `--delete`，构建主机 残留旧文件必须单独审查处理。
7. 完成修改后运行与改动相称的检查，按 `AGENTS.md` 创建中文 Conventional Commit；不同目的分开提交，远程推送需用户在当前请求中明确要求。

本次整理将完整文档导航集中到 `docs/README.md`，补充本结构说明及测试入口；现有源码、包布局、脚本和历史报告路径保持原位，便于沿用已有构建和测试引用。
