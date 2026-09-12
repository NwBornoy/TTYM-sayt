from django.core.exceptions import ValidationError


class UzbekMinimumLengthValidator:
    def __init__(self, min_length=10):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"Parol juda qisqa. Kamida {self.min_length} ta belgidan iborat bo'lishi kerak.",
                code='password_too_short',
            )

    def get_help_text(self):
        return f"Parolingiz kamida {self.min_length} ta belgidan iborat bo'lishi kerak."


class UzbekCommonPasswordValidator:
    def validate(self, password, user=None):
        from django.contrib.auth.password_validation import CommonPasswordValidator
        try:
            CommonPasswordValidator().validate(password, user)
        except ValidationError:
            raise ValidationError(
                "Bu parol juda oddiy va tez topiladigan parollar ro'yxatida bor.",
                code='password_too_common',
            )

    def get_help_text(self):
        return "Parolingiz keng tarqalgan bo'lmasligi kerak."


class UzbekNumericPasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                "Parol faqat raqamlardan iborat bo'lmasligi kerak.",
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return "Parolingiz faqat raqamlardan iborat bo'lmasligi kerak."


class UzbekUserAttributeSimilarityValidator:
    def validate(self, password, user=None):
        from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
        try:
            UserAttributeSimilarityValidator().validate(password, user)
        except ValidationError:
            raise ValidationError(
                "Parolingiz shaxsiy ma'lumotlaringizga (ism, login va h.k.) juda o'xshab ketmasligi kerak.",
                code='password_too_similar',
            )

    def get_help_text(self):
        return "Parolingiz shaxsiy ma'lumotlaringizga o'xshamasligi kerak."