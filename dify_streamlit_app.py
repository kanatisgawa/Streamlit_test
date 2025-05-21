import requests
import streamlit as st

# シークレットからAPIキーを取得
dify_api_key = st.secrets["DIFY_API_KEY"]
url = 'http://localhost/v1/chat-messages'

st.title('カラスのお悩み相談室')

# セッション状態の初期化
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力を取得
prompt = st.chat_input("カラスに何か質問してみよう")

if prompt:
    # ユーザーメッセージを表示・保存
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # アシスタントの応答プレースホルダー
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        headers = {
            'Authorization': f'Bearer {dify_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "inputs": {},  # 空オブジェクトでOK
            "query": prompt,
            "response_mode": "blocking",
            "conversation_id": st.session_state.conversation_id,
            "user": "alex-123",
            "files": []
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            full_response = response_data.get("answer", "")
            new_conversation_id = response_data.get("conversation_id", st.session_state.conversation_id)
            st.session_state.conversation_id = new_conversation_id
        except requests.exceptions.RequestException as e:
            st.error(f"エラーが発生しました: {e}")
            full_response = "応答を取得中にエラーが発生しました。"

        # 応答を表示・保存
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
