import streamlit as st
import numpy as np
import math


def simplify_fraction_good(numerator, denominator):
    # 분자와 분모의 최대공약수를 찾아서 약분합니다.
    gcd = math.gcd(numerator, denominator)
    numerator_simplified = numerator // gcd
    denominator_simplified = denominator // gcd

    # 분모가 1인 경우는 분수 형태를 사용하지 않습니다.
    if denominator_simplified == 1:
        if numerator_simplified == 1:
            return r"\pi"
        elif numerator_simplified == -1:
            return r"-\pi"
        else:
            return f"{numerator_simplified}\pi"
    else:
        # 분자가 1 또는 -1인 경우, 분자에 pi를 포함시키지 않고 분수 형태를 간소화합니다.
        if numerator_simplified == 1:
            return rf"\frac{{\pi}}{{{denominator_simplified}}}"
        elif numerator_simplified == -1:
            return rf"-\frac{{\pi}}{{{denominator_simplified}}}"
        else:
            return rf"\frac{{{numerator_simplified}\pi}}{{{denominator_simplified}}}"

def generate_problem():
    angle_type = np.random.choice(['6', '4'])
    function_type = np.random.choice(['\sin', '\cos', '\\tan'])

    # tan 함수일 때, 정의되지 않는 각도를 피하기 위한 n의 범위 조정
    if function_type == '\tan' and angle_type == '4':
        # tan 함수와 angle_type이 '4'일 때, n = ±2를 피합니다.
        n_choices = [i for i in range(-12, 13) if abs(i) != 2]
        n = np.random.choice(n_choices)
    elif function_type == '\tan' and angle_type == '2':
        # angle_type '2'는 이제 선택되지 않으므로, 여기에 대한 조건은 제거합니다.
        n = np.random.choice(range(-12, 13))
    else:
        # sin, cos 함수 또는 다른 angle_type일 때, n의 전체 범위를 사용합니다.
        n = np.random.choice(range(-12, 13))

    # 약분 로직을 적용하여 각도를 간소화합니다.
    simplified_angle = simplify_fraction_good(n, int(angle_type))

    # 문제 문자열을 생성합니다.
    problem = rf"{function_type}\left({simplified_angle}\right)"
    angle_radians = np.radians(n * (30 if angle_type == '6' else 45))
    
    # 각 함수 유형에 따른 정답 계산
    if function_type == '\sin':
        answer = np.sin(angle_radians)
    elif function_type == '\cos':
        answer = np.cos(angle_radians)
    else:  # '\tan'
        answer = np.tan(angle_radians)
        # tan 함수의 경우, 정의되지 않는 값에 대한 추가 처리는 더 이상 필요하지 않습니다.

    return problem, answer


# Streamlit UI 초기화 및 문제/정답 설정
if 'problem' not in st.session_state or 'correct_answer' not in st.session_state:
    st.session_state.problem, st.session_state.correct_answer = generate_problem()

st.header('📐삼각함수의 값 계산하기 연습')

# '새로운 문제 풀기' 버튼
if st.button('새로운 문제 풀기', type="primary"):
    st.session_state.problem, st.session_state.correct_answer = generate_problem()

# 문제 표시
st.write("다음 삼각함수의 값을 구하시오.")
st.latex(st.session_state.problem)


# 답안 변환 및 정답 확인 로직에 \displaystyle 추가
answers_options_latex = {
    '1': 1, 
    r'\displaystyle \frac{\sqrt{3}}{2}': np.sqrt(3)/2, 
    r'\displaystyle \frac{\sqrt{2}}{2}': np.sqrt(2)/2,
    r'\displaystyle \frac{1}{2}': 1/2, 
    r'\displaystyle \sqrt{3}': np.sqrt(3), 
    r'\displaystyle \frac{\sqrt{3}}{3}': np.sqrt(3)/3, 
    '0': 0,
    '-1': -1, 
    r'\displaystyle -\frac{\sqrt{3}}{2}': -np.sqrt(3)/2, 
    r'\displaystyle -\frac{\sqrt{2}}{2}': -np.sqrt(2)/2,
    r'\displaystyle -\frac{1}{2}': -1/2, 
    r'\displaystyle -\sqrt{3}': -np.sqrt(3), 
    r'\displaystyle -\frac{\sqrt{3}}{3}': -np.sqrt(3)/3
}

# 라디오 버튼을 통해 답안 선택, 이미 \displaystyle을 적용했으므로 별도의 수정 필요 없음
selected_answer = st.radio("답안을 선택하세요:", sorted(answers_options_latex.keys(), key=lambda x: answers_options_latex[x]), format_func=lambda x: f"${x}$")

# 실제 숫자 값으로 변환, \displaystyle 처리 필요 없으므로 이 부분도 변경 없음
selected_answer_value = answers_options_latex.get(selected_answer, None)
# 정답 확인 버튼 및 로직
if st.button('정답 확인'):
    # 사용자가 선택한 답안의 실제 값을 얻음
    selected_answer_value = answers_options_latex.get(selected_answer.replace(r'\displaystyle ', ''), None)
    # 사용자가 선택한 답안이 실제 정답과 일치하는지 확인
    if selected_answer_value is not None and np.isclose(selected_answer_value, st.session_state.correct_answer, atol=0.01):
        st.success('정답입니다!')
        st.balloons()

    else:
        st.title('')
        st.error('🥹 틀렸습니다. 🥲')


with st.expander("힌트 : 그래프 보기"):
    st.image('images/tri.png')

# import streamlit.components.v1 as components

# with st.expander("힌트 보기"):
#     desmos_calculator = """
#     <div class="dcg-wrapper">
#         <iframe src="https://www.desmos.com/calculator/z7p7kwpe7f" width="600" height="350" style="border: 1px solid #ccc" frameborder=0></iframe>
#     </div>
#     """
#     components.html(desmos_calculator, height=400)



# 응원의 메시지 추가
st.markdown("""
---
<p style="text-align: center; color: gray; font-size: 15px;">항상 노력하는 여러분을 응원합니다! </>
<p style="text-align: center; color: gray; font-size: 15px;">💡Copyright &copy; 반포고 황수빈 선생님</>
""", unsafe_allow_html=True)
