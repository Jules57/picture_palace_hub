from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from picture_palace_hub import settings
import datetime


class LogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_staff or not request.user.is_superuser:
            now = datetime.datetime.now()
            last_action_not_found = request.session.get('last_action')
            if last_action_not_found:
                last_action = datetime.datetime.strptime(last_action_not_found, "%H-%M-%S %d/%m/%y")
                if (now - last_action).seconds > settings.TIME_SINCE_LAST_ACTION:
                    logout(request)
            request.session['last_action'] = datetime.datetime.now().strftime("%H-%M-%S %d/%m/%y")
