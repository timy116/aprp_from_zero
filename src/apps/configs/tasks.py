from celery.task import task


@task(name="testing")
def test_celery():
    print('testing celery task')


@task(name="testing2")
def test_celery():
    print('testing celery task2')
