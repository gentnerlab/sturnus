from fabric.api import local

def prepare_deployment(branch_name):
    local('python manage.py test sturnus')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branchname)

 def deploy():
    with lcd('/path/to/my/prod/area/'):
        local('git pull /my/path/to/dev/area/')
        local('python manage.py migrate myapp')
        local('python manage.py test myapp')
        local('/my/command/to/restart/webserver')