import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右排版助手", layout="wide")

st.title("🎨 公众号专属排版工具")
st.info("填写下方信息，右侧将自动生成符合视觉规范的排版代码。")

# 侧边栏样式微调
with st.sidebar:
    st.header("🎨 样式配置")
    color_header = "#79B9D9"  # 浅蓝色头部
    color_title = "#4A90E2"   # 标题深蓝色
    color_author = "#47B04B"  # 作者绿色背景
    line_height = st.slider("行间距", 1.5, 2.5, 1.8)

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🖋️ 内容填充")
    section_name = st.text_input("栏目名称", value="内容节选")
    section_desc = st.text_input("栏目说明", value="本文为基于节目录音的口述稿，仅对语法与用词做部分修改。")
    
    main_title_head = st.text_input("标题括号内文字", value="边币")
    main_title_tail = st.text_input("标题剩余文字", value="信用的建立三阶段：稳健发行、服务财政与配套改革")
    
    author_name = st.text_input("作者姓名", value="刘愿")
    
    main_content = st.text_area("正文内容", placeholder="在此粘贴正文...", height=300)

# 核心 HTML 模板 (内联样式兼容微信)
html_output = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif; padding: 20px; color: #333;">
    
    <section style="margin-bottom: 40px;">
        <h2 style="color: {color_header}; font-size: 28px; font-weight: 400; margin-bottom: 8px;">{section_name}</h2>
        <p style="color: #BBB; font-size: 14px; margin: 0;">{section_desc}</p>
    </section>

    <section style="text-align: center; margin: 60px 0;">
        <h3 style="color: {color_title}; font-size: 19px; font-weight: bold; letter-spacing: 1px;">
            「{main_title_head}」{main_title_tail}
        </h3>
    </section>

    <section style="line-height: {line_height}; letter-spacing: 0.5px; font-size: 16px;">
        <p style="margin-bottom: 20px;">
            <span style="background-color: {color_author}; color: white; padding: 2px 6px; font-size: 13px; font-weight: bold; border-radius: 2px; margin-right: 8px;">
                {author_name}
            </span>
        </p>
        <div style="color: #3F3F3F; text-align: justify;">
            {main_content.replace('\\n', '<br><br>')}
        </div>
    </section>

</div>
"""

with col2:
    st.subheader("👁️ 实时预览")
    # 预览窗口
    st.components.v1.html(html_output, height=600, scrolling=True)
    
    # 复制区域
    st.subheader("📋 复制 HTML 代码")
    st.code(html_output, language="html")
    st.caption("注：点击代码框右上角的图标即可全选复制。")
