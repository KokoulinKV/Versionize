from main.models import Project


def active_project_info(request):
    # При новой сессии ключ 'active_project_id' отсутствует
    # TODO откорректировать с учётом прав доступа
    if 'active_project_id' not in request.session.keys():
        first_project = Project.objects.first()
        request.session['active_project_id'] = first_project.id
    project = Project.objects.filter(
        id=request.session['active_project_id']).first()
    request.session['active_project_id'] = project.id

    return {
        'active_project_id': project.id,
        'active_project_code': project.code,
        'active_project_name': project.name,
        'active_project_exp_date': project.exp_date,
        'active_project_next_upload': project.next_upload,
    }