# tests/test_quiz_admin_api.py
import pytest

# 요구사항 1-1: 관리자만 퀴즈 생성 가능
@pytest.mark.parametrize("user_id, expected_status", [(1, 201), (2, 403)])
def test_create_quiz_authorization(client, user_id, expected_status):
    response = client.post(
        "/quizzes",
        headers={"X-User-Id": str(user_id)},
        json={
            "title": "테스트 퀴즈",
            "question_count": 2,
            "is_question_order_random": True,
            "is_option_order_random": True,
            "questions": [
                {
                    "text": "질문 1",
                    "options": [
                        {"text": "1", "is_correct": False},
                        {"text": "2", "is_correct": True},
                        {"text": "3", "is_correct": False},
                    ]
                },
                {
                    "text": "질문 2",
                    "options": [
                        {"text": "a", "is_correct": False},
                        {"text": "b", "is_correct": True},
                        {"text": "c", "is_correct": False},
                    ]
                },
            ]
        }
    )
    assert response.status_code == expected_status

# 요구사항 1-2: 퀴즈 생성시 하나의 퀴즈가 여러 문제를 포함할 수 있음 + n+2지선다 확인
# 요구사항 1-3: 각 문제는 반드시 정답이 하나
# (위의 케이스에서 이미 테스트됨)

# 요구사항 1-4: 정답이 1개 아닌 경우 실패해야 함
def test_create_quiz_invalid_correct_answers(client):
    response = client.post(
        "/quizzes",
        headers={"X-User-Id": "1"},
        json={
            "title": "정답여러개",
            "question_count": 1,
            "is_question_order_random": False,
            "is_option_order_random": False,
            "questions": [
                {
                    "text": "질문",
                    "options": [
                        {"text": "1", "is_correct": True},
                        {"text": "2", "is_correct": True},
                        {"text": "3", "is_correct": False},
                    ]
                }
            ]
        }
    )
    assert response.status_code == 422 or response.status_code == 400

# 요구사항 1-5: 퀴즈 수정
def test_update_quiz(client):
    response = client.put(
        "/quizzes/1",
        headers={"X-User-Id": "1"},
        json={
            "title": "수정된 퀴즈 제목",
            "question_count": 1,
            "is_question_order_random": False,
            "is_option_order_random": False,
            "questions": [
                {
                    "text": "수정된 질문",
                    "options": [
                        {"text": "수정 A", "is_correct": True},
                        {"text": "수정 B", "is_correct": False},
                        {"text": "수정 C", "is_correct": False},
                    ]
                }
            ]
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "수정된 퀴즈 제목"
    assert response.json()["question_count"] == 1

# 요구사항 1-6: 퀴즈 삭제
def test_delete_quiz(client):
    response = client.delete(
        "/quizzes/2",
        headers={"X-User-Id": "1"}
    )
    assert response.status_code == 200

    # 삭제 후 재조회 시 404
    get_response = client.get("/quizzes/2", headers={"X-User-Id": "1"})
    assert get_response.status_code == 404


# 요구사항 1-7: 잘못된 필드 타입 (예: question_count 문자열) → 422 반환
def test_create_quiz_invalid_field_type(client):
    response = client.post(
        "/quizzes",
        headeㅋs={"X-User-Id": "1"},
        json={
            "title": "타입 에러 테스트",
            "question_count": "두 개",  # 문자열
            "is_question_order_random": True,
            "is_option_order_random": True,
            "questions": []
        }
    )
    assert response.status_code == 422

# 요구사항 1-8: questions가 비어있으면 실패
# def test_create_quiz_with_no_questions(client):
#     response = client.post(
#         "/quizzes",
#         headers={"X-User-Id": "1"},
#         json={
#             "title": "빈 질문 퀴즈",
#             "question_count": 2,
#             "is_question_order_random": True,
#             "is_option_order_random": True,
#             "questi"
#             ""
#             "ons": []
#         }
#     )
#     print(response.json())
#     assert response.status_code == 422 or response.status_code == 400
#
# # 요구사항 1-9: 문제에 옵션이 3개 미만일 경우 실패
# def test_create_quiz_question_with_few_options(client):
#     response = client.post(
#         "/quizzes",
#         headers={"X-User-Id": "1"},
#         json={
#             "title": "옵션 부족",
#             "question_count": 1,
#             "is_question_order_random": False,
#             "is_option_order_random": False,
#             "questions": [
#                 {
#                     "text": "질문",
#                     "options": [
#                         {"text": "1", "is_correct": True},  # 1개만 제공
#                     ]
#                 }
#             ]
#         }
#     )
#     assert response.status_code in (400, 422)
#
# # 요구사항 1-10: 존재하지 않는 퀴즈 수정 요청 시 404
# def test_update_nonexistent_quiz(client):
#     response = client.put(
#         "/quizzes/9999",
#         headers={"X-User-Id": "1"},
#         json={"title": "없는 퀴즈 수정"}
#     )
#     assert response.status_code == 404
#
# # 요구사항 1-11: 존재하지 않는 퀴즈 삭제 요청 시 404
# def test_delete_nonexistent_quiz(client):
#     response = client.delete(
#         "/quizzes/9999",
#         headers={"X-User-Id": "1"}
#     )
#     assert response.status_code == 404
#
# # 요구사항 1-12: 일반 사용자가 퀴즈 수정 시도 시 403
# def test_update_quiz_as_non_admin(client):
#     response = client.put(
#         "/quizzes/1",
#         headers={"X-User-Id": "2"},
#         json={"title": "권한 없음 수정"}
#     )
#     assert response.status_code == 403
#
# # 요구사항 2-1: 관리자 - 전체 퀴즈 목록 조회 가능
# def test_get_quiz_list_as_admin(client):
#     response = client.get("/quizzes", headers={"X-User-Id": "1"})
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#
# # 요구사항 2-2: 사용자 - 퀴즈 목록 조회 시 응시 여부 포함
# def test_get_quiz_list_as_user(client):
#     response = client.get("/quizzes", headers={"X-User-Id": "2"})
#     assert response.status_code == 200
#     for quiz in response.json():
#         assert "has_taken" in quiz  # 응시 여부 포함 여부 확인
#
# # 요구사항 2-3: 퀴즈 상세 조회 (페이징 포함)
# def test_get_quiz_detail_with_pagination(client):
#     response = client.get("/quizzes/1?page=1", headers={"X-User-Id": "2"})
#     assert response.status_code == 200
#     assert "questions" in response.json()
#
# # 요구사항 2-4: 퀴즈 상세 조회 시 설정한 question_count만큼 랜덤으로 문제 제공
# def test_get_quiz_detail_random_question_count(client):
#     response = client.get("/quizzes/1", headers={"X-User-Id": "2"})
#     assert response.status_code == 200
#     assert len(response.json()["questions"]) <= response.json()["question_count"]
#
# # 요구사항 2-5: 퀴즈 문제 및 선택지 랜덤 배치 (응답마다 순서 달라짐)
# def test_get_quiz_detail_randomization(client):
#     res1 = client.get("/quizzes/1", headers={"X-User-Id": "2"}).json()
#     res2 = client.get("/quizzes/1", headers={"X-User-Id": "2"}).json()
#     assert res1["questions"] != res2["questions"]
#
# # 요구사항 2-6: 존재하지 않는 퀴즈 조회 시 404
# def test_get_nonexistent_quiz(client):
#     response = client.get("/quizzes/9999", headers={"X-User-Id": "1"})
#     assert response.status_code == 404
#
# # 요구사항 2-7: 페이지 넘버가 잘못된 경우 기본값 또는 빈 리스트 반환
# def test_get_quiz_invalid_page(client):
#     response = client.get("/quizzes/1?page=100", headers={"X-User-Id": "2"})
#     assert response.status_code == 200
#     assert isinstance(response.json()["questions"], list)
#
#
# # 요구사항 2-8: 사용자별 문제/보기 배치가 다르게 나타나는지 확인
# def test_question_and_option_randomization_per_user(client):
#     user1 = client.get("/quizzes/1", headers={"X-User-Id": "2"}).json()
#     user2 = client.get("/quizzes/1", headers={"X-User-Id": "3"}).json()
#     assert user1["questions"] != user2["questions"]  # 순서 또는 내용 달라야 함
#
# # 요구사항 2-9: 퀴즈 목록 페이징 처리 - 페이지 크기 및 개수 확인
# def test_quiz_list_pagination(client):
#     response = client.get("/quizzes?page=1&size=2", headers={"X-User-Id": "1"})
#     assert response.status_code == 200
#     assert len(response.json()) <= 2
#
# # 요구사항 2-10: 퀴즈 상세 조회 시 페이지 넘버 생략 시 기본 페이지 1 반환
# def test_quiz_detail_default_page(client):
#     no_page = client.get("/quizzes/1", headers={"X-User-Id": "2"}).json()
#     page_1 = client.get("/quizzes/1?page=1", headers={"X-User-Id": "2"}).json()
#     assert no_page["questions"] == page_1["questions"]
#
# # 요구사항 2-11: 퀴즈 상세 조회 시 questions가 실제로 페이징 단위로 제한되는지 확인
# def test_quiz_question_pagination_limit(client):
#     response = client.get("/quizzes/2?page=1", headers={"X-User-Id": "2"})
#     assert response.status_code == 200
#     assert len(response.json()["questions"]) <= response.json()["question_count"]
#
# # 요구사항 2-12: 응시 여부가 반영되어야 함 (사용자가 아직 응시하지 않은 경우)
# def test_quiz_has_taken_false_initial(client):
#     response = client.get("/quizzes", headers={"X-User-Id": "3"})
#     for quiz in response.json():
#         assert "has_taken" in quiz
#         assert quiz["has_taken"] is False or quiz["has_taken"] is True  # 일관성 확인
#
# # 요구사항 2-13: 질문 개수보다 출제할 문제 수가 많은 경우 잘리는지 확인
# def test_get_quiz_limited_by_question_count(client):
#     # 퀴즈 1은 question_count=3 이지만 실제 질문이 더 많을 수 있음
#     res = client.get("/quizzes/1", headers={"X-User-Id": "2"}).json()
#     assert len(res["questions"]) <= res["question_count"]
#
#
# # 요구사항 3-1: 사용자 응시 - 정상 제출
# def test_submit_quiz_answers_success(client):
#     # 퀴즈 1 가져오기
#     quiz_res = client.get("/quizzes/1", headers={"X-User-Id": "2"}).json()
#     questions = quiz_res["questions"]
#
#     # 첫 번째 질문들에 대해 첫 번째 보기 선택
#     answers = []
#     for q in questions:
#         answers.append({
#             "question_id": q["id"],
#             "selected_option_id": q["options"][0]["id"]
#         })
#
#     submit_res = client.post(
#         "/quizzes/1/submit",
#         headers={"X-User-Id": "2"},
#         json={"answers": answers}
#     )
#     assert submit_res.status_code == 200
#     assert "score" in submit_res.json()
#
#
# # 요구사항 3-2: 응시 중 새로고침 → 기존 문제/보기 그대로 유지됨
# def test_consistent_quiz_on_refresh(client):
#     quiz1 = client.get("/quizzes/1", headers={"X-User-Id": "2"}).json()
#     quiz2 = client.get("/quizzes/1", headers={"X-User-Id": "2"}).json()
#     assert quiz1["questions"] == quiz2["questions"]
#
#
# # 요구사항 3-3: 제출된 답안 저장 여부 확인 (score 포함)
# def test_quiz_submission_persists_answers(client):
#     quiz_res = client.get("/quizzes/2", headers={"X-User-Id": "3"}).json()
#     questions = quiz_res["questions"]
#     answers = [
#         {"question_id": q["id"], "selected_option_id": q["options"][0]["id"]}
#         for q in questions
#     ]
#
#     res = client.post(
#         "/quizzes/2/submit",
#         headers={"X-User-Id": "3"},
#         json={"answers": answers}
#     )
#     assert res.status_code == 200
#     assert "score" in res.json()
#     assert res.json()["score"] >= 0
#
#
# # 요구사항 3-4: 선택한 보기 수가 부족할 경우 → 422
# def test_quiz_submit_with_missing_answers(client):
#     quiz_res = client.get("/quizzes/3", headers={"X-User-Id": "2"}).json()
#     questions = quiz_res["questions"]
#
#     # 일부 질문에 대해서만 답변 제출
#     answers = [
#         {"question_id": questions[0]["id"], "selected_option_id": questions[0]["options"][0]["id"]}
#     ]
#
#     res = client.post(
#         "/quizzes/3/submit",
#         headers={"X-User-Id": "2"},
#         json={"answers": answers}
#     )
#     assert res.status_code == 422 or res.status_code == 400
#
#
# # 요구사항 3-5: 존재하지 않는 퀴즈에 제출 → 404
# def test_quiz_submit_nonexistent_quiz(client):
#     res = client.post(
#         "/quizzes/9999/submit",
#         headers={"X-User-Id": "2"},
#         json={"answers": []}
#     )
#     assert res.status_code == 404
#
#
# # 요구사항 3-6: 일반 사용자가 아닌 ID → 401 또는 403
# def test_quiz_submit_invalid_user(client):
#     res = client.post(
#         "/quizzes/1/submit",
#         headers={"X-User-Id": "999"},
#         json={"answers": []}
#     )
#     assert res.status_code in (401, 403, 404)