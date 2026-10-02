import os

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="مدیریت پروژه هوشمند", layout="wide")
st.title("مدیریت پروژه هوشمند")
st.caption("نسخه MVP پژوهشی، متصل به Backend")

with st.sidebar:
    st.header("اجرای گردش‌کار")
    project_id = st.text_input("شناسه پروژه", value="demo-project")
    title = st.text_input("عنوان پروژه", value="سامانه مدیریت وظایف")
    description = st.text_area(
        "شرح پروژه",
        value="سامانه‌ای برای برنامه‌ریزی، تخصیص و پیگیری وظایف تیم نرم‌افزاری.",
    )
    approval = st.selectbox("وضعیت تأیید انسانی", ["pending", "approved"])
    run = st.button("اجرای تحلیل", type="primary")

if run:
    payload = {
        "project_id": project_id,
        "project": {
            "title": title,
            "description": description,
            "goals": ["تبدیل نیازمندی به وظیفه", "پیگیری پیشرفت"],
        },
        "approval_status": approval,
        "team_members": [],
    }
    try:
        response = httpx.post(
            f"{API_URL}/api/v1/projects/{project_id}/run-workflow",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        st.success(f"مرحله فعلی: {result['current_stage']}")
        if result.get("analysis"):
            st.subheader("تحلیل ساختاریافته")
            st.json(result["analysis"])
        if result.get("allocation_proposals"):
            st.subheader("پیشنهادهای تخصیص")
            st.dataframe(result["allocation_proposals"], use_container_width=True)
        if result.get("schedule"):
            st.subheader("زمان‌بندی قطعی")
            st.json(result["schedule"])
    except httpx.HTTPError as error:
        st.error(f"ارتباط با Backend برقرار نشد: {error}")
