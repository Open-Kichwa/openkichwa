from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_babel import gettext, lazy_gettext
from sqlalchemy import func

from .models import User, AccessCode, AccessCodeTypes

pw_fieldname = lazy_gettext("Password")
class RegisterForm(FlaskForm):
    email = EmailField(
        lazy_gettext("Email"), validators=[DataRequired(), Email(message=None), Length(min=4, max=40)]
    )
    password = PasswordField(
        pw_fieldname, validators=[DataRequired(), Length(min=6, max=30)]
    )
    confirm = PasswordField(
        lazy_gettext("Repeat Password"),
        validators=[
            DataRequired(),
            EqualTo('password', message=lazy_gettext("Password must match")),
        ],
    )
    terms = BooleanField(lazy_gettext("Terms"), validators=[DataRequired()])
    beta_code = StringField(lazy_gettext("Beta code"), validators=[DataRequired()])
    username = StringField(lazy_gettext("Username"), validators=[DataRequired()])
    community = SelectField(lazy_gettext("Community"), validators=[DataRequired()],
                            choices=
                            [
                                ("Cañari", "Cañari"),
                                ("Caranqui", "Caranqui"),
                                ("Cayambi", "Cayambi"),
                                ("Chibuleo", "Chibuleo"),
                                ("Guaranga", "Guaranga"),
                                ("Natabuela", "Natabuela"),
                                ("Otavalo", "Otavalo"),
                                ("Panzaleo", "Panzaleo"),
                                ("Puruhá", "Puruhá"),
                                ("Quisapincha", "Quisapincha"),
                                ("Salasaca", "Salasaca"),
                                ("Saraguro", "Saraguro"),
                                ("Tomabela", "Tomabela"),
                                ("Quichuas del Napo", "Quichuas del Napo"),
                                ("Quichuas de Pastaza", "Quichuas de Pastaza")
                            ]
                            )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate()
        result = True
        if not initial_validation:
            result = False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(lazy_gettext("Email has already been registered"))
            result = False
        if self.password.data != self.confirm.data:
            self.password.errors.append(lazy_gettext("Passwords must match"))
            result = False
        if not self.terms.data:
            self.terms.errors.append(lazy_gettext("You need to agree to our terms and conditions"))
            result = False
        acode: AccessCode = AccessCode.query.filter_by(code=self.beta_code.data.upper()).first()
        if not acode:
            self.beta_code.errors.append(lazy_gettext("Invalid code, please check spelling"))
            result = False
        else:
            if acode.claimed:
                self.beta_code.errors.append(lazy_gettext("Code has already been claimed"))
                result = False
            if acode.ctype != AccessCodeTypes.BETA:
                self.beta_code.errors.append(lazy_gettext("Wrong type of code"))
                result = False
        return result

class LoginForm(FlaskForm):
    email = EmailField(lazy_gettext("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(lazy_gettext("Password"), validators=[DataRequired()])
