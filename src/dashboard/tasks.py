from celery.task import task


@task(name="Beat")
def beat(params):
    print(params)
