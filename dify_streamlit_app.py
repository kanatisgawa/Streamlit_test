import requests
import streamlit as st

dify_api_key = st.secrets["DIFY_API_KEY"]
url = 'http://localhost:11434/v1/chat-messages'  # ポートをcurlと合わせる

st.title('カラスのお悩み相談室')

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("カラスに何か質問してみよう")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        headers = {
            'Authorization': f'Bearer {dify_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "inputs": {},
            "query": prompt,
            # "response_mode": "blocking",
            "user": "alex-123"
            # "files": []
        }
        if st.session_state.conversation_id:
            payload["conversation_id"] = st.session_state.conversation_id

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            full_response = response_data.get("answer", "")
            st.session_state.conversation_id = response_data.get("conversation_id", st.session_state.conversation_id)
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTPエラー: {e.response.status_code} - {e.response.text}")
            full_response = "応答を取得中にエラーが発生しました。"
        except requests.exceptions.RequestException as e:
            st.error(f"接続エラー: {e}")
            full_response = "応答を取得中にエラーが発生しました。"

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
