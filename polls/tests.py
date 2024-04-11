import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() trả về False cho các câu hỏi có pub_date
        là trong tương lai.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        """ was_published_recently() trả về False cho các câu hỏi có pub_date
        lớn hơn 1 ngày.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() trả về True cho các câu hỏi có pub_date
        là trong ngày cuối cùng.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
        
def create_question(question_text, days):
        """
        Tạo một câu hỏi với 'question_text' đã cho và xuất bản
        Số 'ngày' được bù đắp cho đến bây giờ.
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)
    
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Nếu không có câu hỏi nào tồn tại, một thông báo thích hợp sẽ được hiển thị.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Các câu hỏi có pub_date trong quá khứ được hiển thị trên
        trang chỉ mục.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Các câu hỏi có pub_date trong tương lai sẽ không hiển thị trên
        trang chỉ mục.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Ngay cả khi cả câu hỏi quá khứ và tương lai đều tồn tại, chỉ những câu hỏi trong quá khứ
        đều được hiển thị.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        Trang chỉ mục câu hỏi có thể hiển thị nhiều câu hỏi.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        Chế độ xem chi tiết của một câu hỏi có pub_date trong tương lai
        Trả về 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Chế độ xem chi tiết của một câu hỏi có pub_date trong quá khứ
        Hiển thị văn bản của câu hỏi.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)