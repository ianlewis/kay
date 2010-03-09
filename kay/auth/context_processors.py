
from kay.auth.forms import LoginBoxForm

def login_box(request):
  form = LoginBoxForm()
  return {'login_box_form': form.as_widget()}
