import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右·对话排版助手", layout="wide")

st.title("🎙️ 播客内容排版助手")
st.markdown("只需输入标题和对话文稿，自动生成带色块标签的公众号排版。")

# 侧边栏：预设人名颜色（你可以自己改）
with st.sidebar:
    st.header("🎨 标签颜色配置")
    color_guest = st.color_picker("嘉宾（如：刘愿）颜色", "#47B04B") # 绿色
    color_host = st.color_picker("主持（如：程衍樑）颜色", "#79B9D9") # 蓝色
    line_spacing = st.slider("段落间距", 10, 50, 30)

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题", value="「边币」信用的建立三阶段")
    
    st.markdown("---")
    st.caption("提示：每行格式为 `人名：内容`。多个段落请直接换行。")
    raw_script = st.text_area("对话文稿输入", placeholder="刘愿：这里是内容...\n\n程衍樑：这里是追问...", height=400)

# 解析逻辑：将纯文本转为带样式的 HTML
def parse_script(text):
    blocks = text.split('\n')
    html_result = ""
    
    for line in blocks:
        if not line.strip(): # 处理空行
            html_result += f'<div style="height: {line_spacing}px;"></div>'
            continue
            
        if "：" in line or ":" in line:
            # 拆分人名和内容
            sep = "：" if "：" in line else ":"
            name, content = line.split(sep, 1)
            name = name.strip()
            
            # 根据人名判断颜色
            bg_color = color_host if "程" in name or "主" in name else color_guest
            
            # 生成人名标签块
            html_result += f"""
            <p style="margin-bottom: 15px;">
                <span style="background-color: {bg_color}; color: white; padding: 4px 10px; font-size: 14px; font-weight: bold; border-radius: 2px;">
                    {name}
                </span>
            </p>
            <div style="font-size: 16px; line-height: 1.8; color: #3F3F3F; text-align: justify; margin-bottom: 25px;">
                {content.strip()}
            </div>
            """
        else:
            # 如果这行没名字，当作上一段的延续
            html_result += f"""
            <div style="font-size: 16px; line-height: 1.8; color: #3F3F3F; text-align: justify; margin-bottom: 25px;">
                {line.strip()}
            </div>
            """
    return html_result

# 构建最终输出
final_html = f"""
<div style="font-family: -apple-system, sans-serif; padding: 20px; max-width: 677px; margin: auto;">
    <div style="text-align: center; margin: 40px 0 60px 0;">
        <h3 style="color: #4A90E2; font-size: 20px; font-weight: bold; letter-spacing: 1px;">
            {main_title}
        </h3>
    </div>

    {parse_script(raw_script)}
</div>
"""

with col2:
    st.subheader("👁️ 预览")
    st.components.v1.html(final_html, height=700, scrolling=True)
    
    st.subheader("📋 复制 HTML 代码")
    st.code(final_html, language="html")
