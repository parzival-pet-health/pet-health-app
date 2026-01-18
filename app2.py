import streamlit as st
import pandas as pd
import os

# ========== 页面设置 ==========
st.set_page_config(
    page_title="🐾 专业宠物健康助手",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 样式美化 ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4B9CD3;
        text-align: center;
        margin-bottom: 1rem;
    }
    .emergency-box {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .developer-info {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4B9CD3;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ========== 疾病数据库 ==========
DISEASES = {
    "狗": {
        "消化不良": {"症状": ["呕吐", "食欲不振", "轻微腹泻", "腹胀"], "紧急度": "🟢 低"},
        "犬瘟热": {"症状": ["发烧", "咳嗽", "眼鼻分泌物", "腹泻", "抽搐"], "紧急度": "🔴 高"},
        "犬细小病毒": {"症状": ["呕吐", "腹泻(带血)", "发烧", "精神不振", "脱水"], "紧急度": "🔴 高"},
        "皮肤病": {"症状": ["瘙痒", "脱毛", "皮肤红肿", "皮屑"], "紧急度": "🟡 中"},
    },
    "猫": {
        "毛球症": {"症状": ["呕吐(含毛)", "食欲不振", "便秘"], "紧急度": "🟢 低"},
        "猫瘟": {"症状": ["呕吐", "腹泻", "发烧", "脱水", "精神萎靡"], "紧急度": "🔴 高"},
        "猫鼻支": {"症状": ["打喷嚏", "流鼻涕", "眼分泌物", "咳嗽"], "紧急度": "🟡 中"},
        "尿路感染": {"症状": ["频繁如厕", "排尿困难", "尿血"], "紧急度": "🟡 中"},
    }
}

# ========== 主程序 ==========
def main():
    # 侧边栏信息
    with st.sidebar:
        # ===== 开发者信息卡片 =====
        st.markdown('<div class="developer-info">', unsafe_allow_html=True)
        st.markdown("#### 🧑‍⚕️ 开发者信息")
        st.markdown("**姓名：** 毛梓帆")
        st.markdown("**专业：** 动物医学 (大二)")
        st.markdown("**院校：** 江苏农牧科技职业学院")
        st.markdown("**版本：** 专业版 v1.1")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---") # 分隔线
        
        # 检查是否在Streamlit Cloud
        if os.environ.get("STREAMLIT_CLOUD"):
            st.success("🌐 公网部署版")
            st.info("""
            **✅ 随时访问**
            - 任何设备可用
            - 无需同一网络
            - 永久在线
            """)
        else:
            st.info("🔧 本地测试版")
        
        st.markdown("---")
        st.markdown("### 🚨 紧急情况")
        emergency = st.checkbox("呼吸困难/窒息")
        emergency = emergency or st.checkbox("严重出血不止")
        emergency = emergency or st.checkbox("昏迷/抽搐")
        
        if emergency:
            st.markdown('<div class="emergency-box">', unsafe_allow_html=True)
            st.error("### 立即就医！")
            st.write("**急救热线: 400-000-0000**")
            st.write("1. 保持宠物安静")
            st.write("2. 准备就医")
            st.write("3. 记录症状")
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()
    
    # 主界面
    st.markdown('<h1 class="main-header">🐾 专业宠物健康助手</h1>', unsafe_allow_html=True)
    st.write("**专业建议，贴心守护。请根据以下指南，为爱宠的健康把好第一关。**")
    
    # 宠物信息
    st.header("📝 宠物基本信息")
    col1, col2 = st.columns(2)
    with col1:
        pet_type = st.selectbox("宠物种类", ["狗", "猫", "兔子", "仓鼠", "其他"])
        age = st.number_input("年龄(月)", min_value=1, max_value=300, value=12)
    with col2:
        weight = st.number_input("体重(kg)", min_value=0.1, max_value=100.0, value=5.0)
        vaccinated = st.radio("疫苗接种", ["已完成", "未完成", "不确定"])
    
    # 症状选择
    st.header("🔍 症状选择")
    symptoms = st.multiselect(
        "选择所有出现的症状（可多选）",
        ["呕吐", "腹泻", "食欲不振", "发烧", "咳嗽", 
         "精神不振", "瘙痒", "脱毛", "打喷嚏", "呼吸急促",
         "排尿困难", "眼鼻分泌物", "抽搐", "腹胀", "体重下降"]
    )
    
    # 症状持续时间
    duration = st.select_slider(
        "症状持续时间",
        options=["几小时", "1-2天", "3-7天", "1-2周", "2周以上"]
    )
    
    # 分析按钮
    if st.button("🤖 开始智能分析", type="primary", use_container_width=True):
        if not symptoms:
            st.warning("请至少选择一个症状")
            return
        
        # 分析症状
        results = []
        if pet_type in ["狗", "猫"]:
            for disease, info in DISEASES[pet_type].items():
                matches = [s for s in symptoms if s in info["症状"]]
                if matches:
                    match_rate = len(matches) / len(info["症状"])
                    results.append({
                        "疾病": disease,
                        "匹配症状": matches,
                        "匹配度": match_rate,
                        "紧急度": info["紧急度"]
                    })
        
        # 显示结果
        st.header("📊 分析结果")
        
        if not results:
            st.info("未找到高度匹配的疾病")
            st.write("**建议：**")
            st.write("1. 观察24小时，记录症状变化")
            st.write("2. 如症状持续，请咨询专业兽医")
            st.write("3. 注意宠物的饮食和排泄情况")
        else:
            results.sort(key=lambda x: x["匹配度"], reverse=True)
            
            for i, result in enumerate(results[:3], 1):
                with st.expander(
                    f"{i}. {result['疾病']} "
                    f"(匹配度:{result['匹配度']:.0%}) "
                    f"{result['紧急度']}",
                    expanded=i==1
                ):
                    st.write(f"**匹配症状:** {', '.join(result['匹配症状'])}")
                    
                    if "🔴" in result['紧急度']:
                        st.error("**立即就医！**")
                        st.write("请尽快联系宠物医院")
                    elif "🟡" in result['紧急度']:
                        st.warning("**建议就医检查**")
                        st.write("建议预约兽医进行检查")
                    else:
                        st.success("**可先家庭护理**")
                        st.write("密切观察，如有加重请就医")
            
            # 就医建议
            st.header("💡 就医准备建议")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**📋 准备材料：**")
                st.write("- 宠物年龄、品种")
                st.write("- 疫苗和驱虫记录")
                st.write("- 症状开始时间")
                st.write("- 饮食变化记录")
            
            with col2:
                st.write("**📸 拍照记录：**")
                st.write("- 异常部位照片")
                st.write("- 呕吐物/排泄物")
                st.write("- 异常行为视频")
                st.write("- 饮食和饮水情况")
    
    # 底部信息
    st.divider()
    st.markdown("""
    ### ⚠️ 重要声明
    1. 本工具由**江苏农牧科技职业学院 动物医学专业**学生开发，数据来源于专业教材与资料，仅供参考。
    2. 不能替代专业兽医诊断。
    3. 紧急情况请立即联系宠物医院。
    4. 数据会不断更新完善。

    **开发团队**：动物医学专业 × AI技术  
    **版本**：专业版 v1.1 | **更新日期**：2024年  

    **🌐 公网部署**：此应用已部署至Streamlit Cloud，可永久访问。
    """)

if __name__ == "__main__":
    main()
