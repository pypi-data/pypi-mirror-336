from ..utils.env_initializer import EnvStore


class GenerateLink:
    @staticmethod
    def __get_base_url(courseOfferingId: str) -> str:
        __environment: str = EnvStore().environment.removesuffix("-api")
        __domain: str = EnvStore().domain
        __base_url = (
            f"https://{__environment}{__domain}/learning-center/{courseOfferingId}"
        )
        return __base_url

    @classmethod
    def get_quiz_link(
        cls,
        courseOfferingId: str,
        quizId: str,
    ) -> str:
        baseUrl = cls.__get_base_url(courseOfferingId)
        quizUrl = f"/quiz/quiz-learner/quiz-attempt-start/initialize-quiz/{quizId}"
        return baseUrl + quizUrl

    @classmethod
    def get_quiz_report_link(
        cls, courseOfferingId: str, quizId: str, attemptId: str
    ) -> str:
        baseUrl = cls.__get_base_url(courseOfferingId)
        quizReportUrl = f"/quiz/quiz-learner/quiz-report/{attemptId}/{quizId}"
        return baseUrl + quizReportUrl

    @classmethod
    def get_live_class_room_link(
        cls, courseOfferingId: str, liveClassRoomId: str
    ) -> str:
        baseUrl = cls.__get_base_url(courseOfferingId)
        liveClassroomUrl = f"/live-classroom-sessions/details/{liveClassRoomId}"
        return baseUrl + liveClassroomUrl

    @classmethod
    def get_programming_env_link(cls, courseOfferingId: str, elementId: str) -> str:
        baseUrl = cls.__get_base_url(courseOfferingId)
        programming_env_link = f"/unext-labs/{elementId}/view-exercise"
        return baseUrl + programming_env_link
