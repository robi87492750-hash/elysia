# 爱莉希雅桌面宠物

基于 `dsh-pet-upstream` 的桌面宠物功能，为爱莉希雅角色包单独运行。支持透明桌面窗口、托盘控制、丰富互动、动画行为、菜单与设置；本项目使用独立配置目录，不读取或修改原 dsh-pet 的设置。

## 一键启动

需要 Windows 和 Python 3.10 或更新版本。下载仓库 ZIP 并解压后，双击 `run.bat` 启动。第一次运行会创建项目专用环境并安装依赖（需要网络，耗时可能较长）；之后会直接在后台启动桌宠，不显示控制台窗口。也可以先双击 `setup.bat` 完成安装，再运行 `run.bat`。本仓库不是免安装的独立 EXE，下载后仍需先安装 Python。

退出：桌宠上右键 →「退出」，或在系统托盘图标菜单中选择退出。

## 已接入的桌宠功能

- 桌面交互：透明无边框、置顶、拖动、锁定位置、鼠标穿透、屏幕边界与多屏位置管理、拖拽物理和抛掷。
- 行为与彩蛋：自动待机/移动/转身/随机动作、点击反馈、边缘探头、黄金回旋、撞飞彩蛋、拖文件触发互动。
- 托盘与桌面控制：显示/隐藏、设置、角色选择、开机启动、快捷菜单、退出；隐藏桌宠后可从托盘恢复。
- 外观与动画：角色素材包、动画速度与缩放、透明度、可配置右键菜单、菜单主题与布局、播放性能/省电选项。
- 提醒与气泡：自言自语、气泡文字与配图、待办与到期提醒、语音报时、节日提醒、天气。
- 可选联动：AI 对话与快速对话、文件解读、屏幕理解、音乐与歌词、DSH Agent 联动，以及灵动岛。

联网天气、语音服务、AI 模型和 DSH 联动需要相应网络、密钥或服务配置；未配置时，不影响基本桌宠操作。各项功能可在桌宠右键菜单和「桌宠设置」中管理。

## 爱莉希雅动画素材

随仓库提供的人物包位于 `characters/elysia/`，默认使用女仆装爱莉希雅。服装参考《崩坏3》「粉色甜心小姐♪」：粉发、精灵耳、蓝紫色眼睛、白色发饰、黑紫色裙身与白色花边；头身比参考“大肥鱼”桌宠的圆头短身造型。项目提供者说明原画和跑步图由 GPT 生成；`Q版女仆爱莉希雅.png`、图标和 WebM 动画由本项目素材脚本基于这些图制作。运行时播放待机、转身、行走、拖拽、点击和挥手互动的透明 WebM 动画。角色包通过 `manifest.json` 声明动作文件与身体/头部区域；要重建动画，可在项目环境运行 `python tools/build_fairy_elysia_assets.py`。

这是非官方、非商业的《崩坏3》同人项目，与米哈游/HoYoverse 无官方合作或授权关系。程序代码与人物素材适用不同的权利说明；根目录 MIT 许可不授予《崩坏3》角色形象的使用权。详见 [人物素材说明](characters/elysia/README.md) 和 [第三方声明](THIRD_PARTY_NOTICES.md)。

可以在 `characters/elysia/videos/` 下按 `idle`、`turn`、`move`、`click`、`drag`、`random` 子目录添加透明 WebM 素材。更多完整功能使用说明见 [UPSTREAM_README.md](UPSTREAM_README.md)。

## 项目结构

```text
main.py                     Elysia 版本启动入口
pet/                        移植的桌宠主程序、设置、动画、托盘与联动功能
characters/elysia/          主程序识别的角色包
integrations/               可选 DSH bridge
resources/                  上游桌面辅助资源
setup.bat / run.bat         安装和一键启动
```

## 许可与来源

桌宠功能代码及上游依赖声明见 [LICENSE](LICENSE) 与 [UPSTREAM_THIRD_PARTY_NOTICES.md](UPSTREAM_THIRD_PARTY_NOTICES.md)。人物素材的非商业同人说明见 [characters/elysia/README.md](characters/elysia/README.md) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

