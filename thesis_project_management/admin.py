from django.contrib import admin
from .models import *

admin.site.register(Team)
admin.site.register(TeamStudentMap)
admin.site.register(TeamSupervisorMap)
admin.site.register(TeamTeacherMap)
admin.site.register(TeamProgress)
admin.site.register(Arrangement)
admin.site.register(TeamParticipation)
