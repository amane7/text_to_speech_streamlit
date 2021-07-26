import os
from google.cloud import texttospeech
import io
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret.json'

def synthesize_speech(text,lang='日本語',gender='default'):
    gender_type = {
        'default':texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male':texttospeech.SsmlVoiceGender.MALE,
        'female':texttospeech.SsmlVoiceGender.FEMALE,
        'neutral':texttospeech.SsmlVoiceGender.NEUTRAL
    }


    lang_code = {
        '英語':'en-US',
        '日本語':'ja-JP',
        '中国語':'zh',
        'フランス語':'fr-FR',
        'ドイツ語':'de-DE',
        'イタリア語':'it-IT',
        'ポルトガル語':'pt-PT',
        'スペイン語':'es-ES',
        'ロシア語':'ru-RU'
    }



    client = texttospeech.TextToSpeechClient()

    #出力するテキストを指示
    input_text = texttospeech.SynthesisInput(text=input_data)

    voice = texttospeech.VoiceSelectionParams(
        language_code = lang_code[lang],
        ssml_gender = gender_type[gender],
        )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
        )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )
    return response

st.title('テキスト自動読み上げアプリ')

st.markdown('### データ準備')

input_option = st.selectbox(
    '入力データの選択',
    ('直接入力','テキストファイル')
)

input_data = None

if input_option == '直接入力':
    input_data = st.text_area('↓にテキストを直接入力して下さい','音声出力サンプル文になります。')
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードして下さい',['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode()

if input_data is not None:
    st.write('入力データ')
    st.write(input_data)
    st.markdown('### パラメータ設定')
    st.subheader('言語 と 話者の性別')

    lang = st.selectbox(
        '言語を選択して下さい',
        ('英語','日本語','中国語','フランス語','ドイツ語','イタリア語','ポルトガル語','スペイン語','ロシア語')
    )

    gender = st.selectbox(
        '話者の性別を選択して下さい',
        ('default', 'male', 'female', 'neutral')
    )
    
    st.markdown('### 音声合成')
    st.write('『入力データ』の内容で音声を出力しますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始します')
        response = synthesize_speech(input_data, lang = lang, gender = gender)
        st.audio(response.audio_content)
        comment.write('完了しました')